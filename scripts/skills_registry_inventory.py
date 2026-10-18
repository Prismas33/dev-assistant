"""Read-only discovery for the Codex skills registry."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path


SKIP_PARTS = {".git", "node_modules", "build", "dist", ".next", ".venv", "venv"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_folder(path: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(path.rglob("*"), key=lambda item: str(item).lower()):
        if file.is_symlink():
            raise ValueError(f"Symlink in skill package: {file}")
        if not file.is_file() or any(part in SKIP_PARTS for part in file.relative_to(path).parts):
            continue
        digest.update(file.relative_to(path).as_posix().encode("utf-8"))
        with file.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path, default: dict | None = None) -> dict:
    if not path.is_file():
        return {} if default is None else default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        return {"name": path.parent.name, "description": "", "version": "", "license": ""}
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {"name": path.parent.name, "description": "", "version": "", "license": ""}
    header = lines[1:end]
    values = {"name": path.parent.name, "description": "", "version": "", "license": ""}
    for index, line in enumerate(header):
        match = re.match(r"^(name|description|license):\s*(.*)$", line)
        if match:
            value = match.group(2).strip().strip("\"'")
            if not value and match.group(1) == "description":
                follow = []
                for next_line in header[index + 1 :]:
                    if next_line and not next_line[0].isspace():
                        break
                    if next_line.strip():
                        follow.append(next_line.strip())
                value = " ".join(follow)
            values[match.group(1)] = value
        version = re.match(r"^\s+version:\s*(.*)$", line)
        if version:
            values["version"] = version.group(1).strip().strip("\"'")
    return values


def git_value(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-c", f"safe.directory={repo.as_posix()}", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def _local_skill_files(project_root: Path) -> list[Path]:
    if not project_root.is_dir():
        return []
    found: list[Path] = []
    if shutil.which("rg"):
        result = subprocess.run(
            ["rg", "--files", "--hidden", "-g", "SKILL.md", "-g", "!.git", "-g", "!node_modules", "-g", "!build", str(project_root)],
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
        found = [Path(line) for line in result.stdout.splitlines()]
    if not found and (not shutil.which("rg") or result.returncode not in (0, 1)):
        for directory, dirs, files in __import__("os").walk(project_root):
            dirs[:] = [name for name in dirs if name not in SKIP_PARTS]
            if "SKILL.md" in files:
                found.append(Path(directory) / "SKILL.md")
    return [
        path for path in found
        if any(path.parent.parent.name == root and path.parent.parent.parent.name in (".agents", ".codex") for root in ("skills",))
    ]


def _skill_lock(path: Path, agents_home: Path) -> dict:
    if path.parent.parent == agents_home / "skills":
        return load_json(agents_home / ".skill-lock.json").get("skills", {}).get(path.parent.name, {})
    if path.parent.parent.name == "skills" and path.parent.parent.parent.name == ".agents":
        repo = path.parent.parent.parent.parent
        return load_json(repo / "skills-lock.json").get("skills", {}).get(path.parent.name, {})
    return {}


def discover_skills(codex_home: Path, agents_home: Path, utilities: Path, project_roots: list[Path], metadata: dict) -> tuple[list[dict], list[str]]:
    candidates: list[tuple[Path, str]] = []
    candidates.extend((p, "system") for p in (codex_home / "skills" / ".system").glob("*/SKILL.md"))
    candidates.extend((p, "global") for p in (codex_home / "skills").glob("*/SKILL.md"))
    candidates.extend((p, "global") for p in (agents_home / "skills").glob("*/SKILL.md"))
    for root in project_roots:
        candidates.extend((p, "local") for p in _local_skill_files(root))
    seen_paths: set[str] = set()
    entries: list[dict] = []
    warnings: list[str] = []
    for path, scope in candidates:
        key = str(path.resolve()).lower()
        if key in seen_paths:
            continue
        seen_paths.add(key)
        data = frontmatter(path)
        name = data["name"] or path.parent.name
        lock = _skill_lock(path, agents_home)
        policy = metadata.get("skills", {}).get(name, {})
        source = lock.get("source", "")
        source_url = lock.get("sourceUrl", "")
        commit = ""
        own_repo = utilities / name
        if own_repo.is_dir() and (own_repo / ".git").exists():
            source_commit = git_value(own_repo, "rev-parse", "HEAD")
            source_url = git_value(own_repo, "remote", "get-url", "origin") or source_url
            source = source or (source_url.removeprefix("https://github.com/").removesuffix(".git"))
            if source_commit and sha256_folder(own_repo) == sha256_folder(path.parent):
                commit = source_commit
            else:
                warnings.append(f"Fonte e instalação de {name} diferem; commit instalado não confirmado")
        if not source and scope == "system":
            source = "Codex runtime"
        if source and not source_url and "/" in source and not source.startswith("Codex"):
            source_url = f"https://github.com/{source}"
        skill_path = lock.get("skillPath", "SKILL.md")
        direct_url = (
            f"{source_url.removesuffix('.git')}/blob/{commit or 'main'}/{skill_path}"
            if source_url.startswith("https://github.com/") else ""
        )
        repo_name = path.parent.parent.parent.parent.name if scope == "local" else "Todos"
        entry = {
            "name": name,
            "scope": scope,
            "path": str(path.parent),
            "description": data["description"],
            "version": data["version"] or "não declarada",
            "license": data["license"] or policy.get("license", "não declarada"),
            "commit": commit or "não fixado",
            "installed_at": lock.get("installedAt", "não verificada"),
            "source": source or "não declarada",
            "source_url": source_url or "não declarado",
            "skill_url": direct_url or "não declarado",
            "sha256": sha256_file(path),
            "folder_sha256": sha256_folder(path.parent),
            "category": policy.get("category", "por classificar"),
            "technologies": policy.get("technologies", "por confirmar"),
            "projects": policy.get("projects", repo_name),
            "trigger": policy.get("trigger", "gatilho específico da skill"),
            "exclusions": policy.get("exclusions", "por auditar"),
            "dependencies": policy.get("dependencies", "por auditar"),
            "audit": policy.get("audit", "por auditar"),
        }
        entries.append(entry)
    entries.sort(key=lambda item: (item["scope"], item["name"], item["path"].lower()))
    names: dict[str, list[str]] = {}
    for entry in entries:
        names.setdefault(entry["name"], []).append(entry["path"])
    for name, paths in names.items():
        if len(paths) > 1:
            warnings.append(f"Nome duplicado {name}: {', '.join(paths)}")
    return entries, warnings


def discover_plugins(codex_home: Path) -> tuple[list[dict], str]:
    executable = shutil.which("codex")
    if not executable:
        return [], "CLI codex indisponível; plugins não reconciliados"
    env = __import__("os").environ.copy()
    env["CODEX_HOME"] = str(codex_home)
    try:
        result = subprocess.run([executable, "plugin", "list", "--json"], capture_output=True, text=True, timeout=35, env=env, check=False)
        if result.returncode:
            return [], "A listagem de plugins falhou; preservar o último estado verificado"
        data = json.loads(result.stdout[result.stdout.find("{") :])
        plugins = [
            {"id": item.get("pluginId", ""), "version": item.get("version", "não declarada"), "enabled": bool(item.get("enabled")), "source": item.get("source", {}).get("path", "")}
            for item in data.get("installed", []) if item.get("installed")
        ]
        return sorted(plugins, key=lambda item: item["id"]), ""
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return [], "A listagem de plugins falhou; preservar o último estado verificado"
