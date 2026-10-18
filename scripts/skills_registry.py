"""Maintain the canonical Codex skills registry and its verified E: backup.

Reconciliation reads installed skills; it never installs, updates, or removes one.
The managed change workflow runs reconciliation after an approved change.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from skills_registry_inventory import (
    discover_plugins,
    discover_skills,
    frontmatter,
    git_value,
    load_json,
    sha256_file,
    sha256_folder,
)


CATALOG = "CODEX_SKILLS_REGISTRY.md"
MANIFEST = "skills-manifest.json"
METADATA = "skills-metadata.json"
BACKUP_DIR = "codex-skills-backup"
OWN_SKILLS = ("dev-assistant", "security-audit", "seo-audit", "product-ui-design-consistency")
EVENT_LABELS = {"install": "instalação", "update": "atualização", "remove": "remoção", "reconcile": "reconciliação"}
SECRET_FILE = re.compile(r"(^|/)(\.env($|\.)|id_rsa|id_ed25519|.*\.(pem|p12|pfx|key)$|credentials?\.(json|txt)$)", re.I)
SECRET_CONTENT = re.compile(rb"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|ghp_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def atomic_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_text(path: Path, text: str) -> None:
    atomic_bytes(path, text.encode("utf-8"))


def json_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def esc(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").replace("<", "&lt;").replace(">", "&gt;")


def load_events(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def render_catalog(entries: list[dict], plugins: list[dict], metadata: dict, events: list[dict], warnings: list[str], timestamp: str) -> str:
    lines = [
        "# Catálogo central de Agent Skills do Codex",
        "",
        f"**Última reconciliação com alterações:** {timestamp}  ",
        "**Fonte principal:** `C:\\Users\\ventu\\.codex\\skills-registry\\CODEX_SKILLS_REGISTRY.md`  ",
        "**Espelho:** `E:\\utilitarios\\CODEX_SKILLS_REGISTRY.md`",
        "",
        "Este catálogo regista o que foi observado no disco. Uma entrada em cache, um plugin instalado e uma skill exposta numa sessão são estados distintos. A seleção cabe à `dev-assistant`, às instruções do repositório e ao pedido atual; o catálogo não autoriza instalação, execução remota ou acesso a produção.",
        "",
        "## Skills encontradas",
        "",
        "| Skill / âmbito | Descrição | Origem / material auditado | Versão / commit / datas | Localização / SHA-256 | Categoria / tecnologias / projetos | Ativação / exclusões | Licença / dependências / auditoria |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in entries:
        url = item["skill_url"]
        origin = f"[{esc(item['source'])}]({url})" if url != "não declarado" else esc(item["source"])
        lines.append(
            "| " + " | ".join([
                f"`{esc(item['name'])}` / {esc(item['scope'])}",
                esc(item["description"] or "sem descrição"),
                origin,
                f"{esc(item['version'])}; `{esc(item['commit'])}`; instalação {esc(item['installed_at'])}; atualização {esc(item['updated_at'])}",
                f"`{esc(item['path'])}`; `{item['sha256'][:16]}…`",
                f"{esc(item['category'])}; {esc(item['technologies'])}; {esc(item['projects'])}",
                f"{esc(item['trigger'])}; {esc(item['exclusions'])}",
                f"{esc(item['license'])}; {esc(item['dependencies'])}; **{esc(item['audit'])}**",
            ]) + " |"
        )
    lines += ["", f"**Total em disco:** {len(entries)}. `review-agent` ou outra skill presente em disco só deve ser chamada se também for exposta pela sessão Codex.", "", "## Plugins instalados (CLI local)", "", "| Plugin | Versão | Ativo | Origem local |", "| --- | --- | --- | --- |"]
    for item in plugins:
        lines.append(f"| `{esc(item['id'])}` | {esc(item['version'])} | {'sim' if item['enabled'] else 'não'} | `{esc(item['source'])}` |")
    if not plugins:
        lines.append("| Não verificado | — | — | CLI indisponível ou sem instalações confirmadas |")
    lines += ["", "## Candidatas ainda não instaladas ou não promovidas", "", "| Nome proposto | Estado / razão |", "| --- | --- |"]
    for candidate in metadata.get("candidates", []):
        lines.append(f"| `{esc(candidate['name'])}` | {esc(candidate['status'])}: {esc(candidate['reason'])} |")
    if not metadata.get("candidates"):
        lines.append("| — | Sem candidatas registadas |")
    lines += [
        "", "## Regras de gestão e reconciliação", "",
        "- O ficheiro em C: é a fonte principal. O processo normal só copia C: para E:; nunca repõe automaticamente C: a partir de E:.",
        "- Após uma instalação, atualização ou remoção aprovada, executar `skills_registry.py reconcile`; o processo gerido inclui esse passo e guarda manifesto, espelho e histórico sem edição manual da tabela.",
        "- No início de um projeto ou após mudança material, a `dev-assistant` consulta este catálogo. Se a última verificação tiver mais de sete dias, executa reconciliação; tarefas pequenas reutilizam a seleção atual.",
        "- Instalações feitas fora deste processo são detetadas na reconciliação. Entradas novas ficam `por auditar` até revisão da origem, licença, dependências, scripts e risco.",
        "- Para instalar ou atualizar, auditar a revisão exata, fixar commit quando possível, verificar scripts e dependências, validar descoberta em nova sessão e só então alterar a instalação. A reconciliação não é um instalador.",
        "- Para remover, confirmar o âmbito e dependências, preservar um manifesto da versão retirada, remover pela ferramenta adequada e reconciliar. Não remover skills de sistema ou plugins através deste catálogo.",
        "- Para recuperar, verificar SHA-256 do snapshot e respetivo manifesto, preservar o estado atual, pedir explicitamente `restore --apply --expected-sha256` e reconciliar contra o disco antes de tratar a cópia recuperada como atual.",
        "- Manifestos, snapshots e arquivos das skills próprias estão em `E:\\utilitarios\\codex-skills-backup`; consultar `RESTORE.md` nessa pasta. Nunca guardar credenciais, chaves privadas ou ficheiros `.env` nos arquivos.",
        "", "## Avisos de reconciliação", "",
    ]
    lines += [f"- {esc(warning)}" for warning in warnings] if warnings else ["- Nenhum aviso nesta leitura."]
    lines += ["", "## Histórico de alterações", "", "| Data UTC | Evento | Skills | Plugins |", "| --- | --- | ---: | ---: |"]
    for event in events[-30:]:
        lines.append(f"| {esc(event['at'])} | {esc(event['kind'])} | {event['skills']} | {event['plugins']} |")
    return "\n".join(lines) + "\n"


def archive_catalog(catalog: Path, manifest: Path, history: Path) -> Path | None:
    if not catalog.is_file():
        return None
    content = catalog.read_bytes()
    digest = digest_bytes(content)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = f"{stamp}-{digest[:12]}"
    target = history / f"{stem}.md"
    if target.exists():
        if sha256_file(target) != digest:
            raise RuntimeError(f"Historical snapshot changed: {target}")
        return target
    history.mkdir(parents=True, exist_ok=True)
    atomic_bytes(target, content)
    atomic_text(history / f"{stem}.sha256", digest + "\n")
    if manifest.is_file():
        atomic_bytes(history / f"{stem}.manifest.json", manifest.read_bytes())
    return target


def validate_primary(catalog: Path, manifest: Path) -> dict:
    if not catalog.exists() and not manifest.exists():
        return {}
    if not catalog.is_file() or not manifest.is_file():
        raise RuntimeError("Catálogo/manifesto principal incompleto; não substituir automaticamente")
    data = load_json(manifest)
    if data.get("catalog_sha256") != sha256_file(catalog):
        raise RuntimeError("Catálogo principal divergiu do manifesto; preservar e rever antes de reconciliar")
    return data


def sync_mirror(catalog: Path, manifest: Path, utilities: Path, backup: Path) -> None:
    mirror = utilities / CATALOG
    if mirror.is_file() and sha256_file(mirror) != sha256_file(catalog):
        quarantine = backup / "mirror-drift"
        quarantine.mkdir(parents=True, exist_ok=True)
        digest = sha256_file(mirror)
        target = quarantine / f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{digest[:12]}.md"
        if not target.exists():
            atomic_bytes(target, mirror.read_bytes())
            atomic_text(target.with_suffix(".sha256"), digest + "\n")
    atomic_bytes(mirror, catalog.read_bytes())
    atomic_bytes(backup / "current" / MANIFEST, manifest.read_bytes())
    if sha256_file(mirror) != sha256_file(catalog):
        raise RuntimeError("Falha de integridade do espelho em E:")


def archive_owned_sources(utilities: Path, backup: Path) -> list[str]:
    warnings: list[str] = []
    target_root = backup / "owned-sources"
    index: list[dict] = []
    for name in OWN_SKILLS:
        repo = utilities / name
        if not (repo / ".git").exists():
            warnings.append(f"Fonte própria ausente: {repo}")
            continue
        commit = git_value(repo, "rev-parse", "HEAD")
        origin = git_value(repo, "remote", "get-url", "origin")
        if not re.fullmatch(r"[0-9a-f]{40}", commit):
            warnings.append(f"Commit não verificável: {name}")
            continue
        target = target_root / name / f"{commit}.zip"
        if not target.is_file():
            tree = subprocess.run(
                ["git", "-c", f"safe.directory={repo.as_posix()}", "-C", str(repo), "ls-tree", "-r", "--name-only", "HEAD"],
                capture_output=True, text=True, timeout=30, check=False,
            )
            if tree.returncode:
                warnings.append(f"Ficheiros Git não verificáveis: {name}")
                continue
            unsafe = False
            for relative in tree.stdout.splitlines():
                if SECRET_FILE.search(relative.replace("\\", "/")):
                    unsafe = True
                    break
                content = subprocess.run(
                    ["git", "-c", f"safe.directory={repo.as_posix()}", "-C", str(repo), "show", f"HEAD:{relative}"],
                    capture_output=True, timeout=30, check=False,
                )
                if content.returncode or SECRET_CONTENT.search(content.stdout):
                    unsafe = True
                    break
            if unsafe:
                warnings.append(f"Arquivo de {name} bloqueado por possível segredo; rever a origem")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_suffix(".pending")
            result = subprocess.run(
                ["git", "-c", f"safe.directory={repo.as_posix()}", "-C", str(repo), "archive", "--format=zip", "-o", str(temporary), "HEAD"],
                capture_output=True, text=True, timeout=60, check=False,
            )
            if result.returncode:
                temporary.unlink(missing_ok=True)
                warnings.append(f"Arquivo Git falhou: {name}")
                continue
            unsafe = False
            with zipfile.ZipFile(temporary) as package:
                for member in package.infolist():
                    if member.is_dir():
                        continue
                    if SECRET_FILE.search(member.filename.replace("\\", "/")) or SECRET_CONTENT.search(package.read(member)):
                        unsafe = True
                        break
            if unsafe:
                temporary.unlink(missing_ok=True)
                warnings.append(f"Arquivo de {name} bloqueado por possível segredo; rever a origem")
                continue
            os.replace(temporary, target)
            atomic_text(target.with_suffix(".sha256"), sha256_file(target) + "\n")
        digest = sha256_file(target)
        index.append({"name": name, "commit": commit, "origin": origin, "archive": str(target), "sha256": digest})
    prior = load_json(target_root / "versions.json").get("sources", [])
    by_version = {(item["name"], item["commit"]): item for item in prior}
    by_version.update({(item["name"], item["commit"]): item for item in index})
    atomic_text(target_root / "versions.json", json_text({"generated_at": now(), "sources": sorted(by_version.values(), key=lambda item: (item["name"], item["commit"]))}))
    return warnings


def setup_recovery_guide(backup: Path, script: Path) -> None:
    guide = backup / "RESTORE.md"
    if guide.exists():
        return
    atomic_text(guide, f"""# Recuperação do catálogo e das skills

O catálogo em C: é a fonte principal. `CODEX_SKILLS_REGISTRY.md` em `E:\\utilitarios` é apenas o espelho. Nunca copiar o espelho antigo sobre C: sem validar o snapshot.

1. Executar `python \"{script}\" verify` para comparar C:, E: e o manifesto.
2. Escolher um par `catalog-history/<id>.md` e `<id>.manifest.json`; conferir `<id>.sha256`.
3. Para recuperar deliberadamente: `python \"{script}\" restore --snapshot-id <id> --expected-sha256 <SHA256> --apply`. O estado atual é arquivado primeiro.
4. Executar `python \"{script}\" reconcile` para comparar a recuperação com as skills efetivamente instaladas.

`owned-sources/versions.json` identifica arquivos ZIP Git de revisões confirmadas das skills próprias, com SHA-256, commit e origem. Para reinstalar uma skill própria, escolher a entrada, executar `Get-FileHash -Algorithm SHA256 <arquivo.zip>` e comparar com o manifesto; `Expand-Archive -LiteralPath <arquivo.zip> -DestinationPath <pasta-temporária>`, inspecionar `SKILL.md` e scripts, copiar para o diretório global apropriado e reconciliar. Nunca extrair sobre uma instalação existente sem backup e revisão. Para skills externas, consultar origem e versão no manifesto; se houver commit fixo, usar `python <skill-installer>/scripts/install-skill-from-github.py --repo <owner/repo> --path <skill-path> --ref <commit> --dest <destino>` após auditar esse commit. Sem commit verificável, parar para nova auditoria. Um hash de árvore isolado não substitui o commit de origem. Skills de sistema e plugins devem ser repostas pelos respetivos runtimes, não por cópia manual deste backup.

Reconciliar na criação de projetos e após mudança material; `--if-stale-days 7` evita verificações repetidas. Uma tarefa semanal do utilizador pode executar o mesmo comando se for necessária verificação mesmo sem projetos ativos.
""")


def reconcile(args: argparse.Namespace) -> str:
    codex_home, agents_home, utilities = Path(args.codex_home), Path(args.agents_home), Path(args.utilities)
    registry = codex_home / "skills-registry"
    catalog, manifest, metadata_file = registry / CATALOG, registry / MANIFEST, registry / METADATA
    backup = utilities / BACKUP_DIR
    previous = validate_primary(catalog, manifest)
    if args.if_stale_days and previous.get("reconciled_at"):
        last = datetime.fromisoformat(previous["reconciled_at"].replace("Z", "+00:00"))
        if datetime.now(timezone.utc) - last < timedelta(days=args.if_stale_days):
            return "SKIP: registo verificado recentemente"
    if not metadata_file.is_file():
        atomic_text(metadata_file, json_text({"skills": {}, "candidates": []}))
    metadata = load_json(metadata_file)
    roots = [Path(value) for value in args.project_root]
    skills, warnings = discover_skills(codex_home, agents_home, utilities, roots, metadata)
    if args.no_plugins:
        plugins = previous.get("plugins", [])
        warnings.append("Plugins não consultados nesta execução")
    else:
        plugins, warning = discover_plugins(codex_home)
        if warning:
            plugins = previous.get("plugins", [])
            warnings.append(warning)
    fingerprint = digest_bytes(json_text({"skills": skills, "plugins": plugins, "metadata": metadata}).encode("utf-8"))
    changed = fingerprint != previous.get("inventory_sha256")
    timestamp = now()
    if changed:
        event = {"at": timestamp, "kind": EVENT_LABELS.get(args.event) if args.event else ("criação" if not previous else "reconciliação"), "skills": len(skills), "plugins": len(plugins)}
        events_path = backup / "events.jsonl"
        events = load_events(events_path) + [event]
        archive_catalog(catalog, manifest, backup / "catalog-history")
        rendered = render_catalog(skills, plugins, metadata, events, warnings, timestamp)
        catalog_hash = digest_bytes(rendered.encode("utf-8"))
        record = {"schema": 1, "reconciled_at": timestamp, "inventory_sha256": fingerprint, "catalog_sha256": catalog_hash, "skills": skills, "plugins": plugins, "warnings": warnings}
        atomic_text(catalog, rendered)
        atomic_text(manifest, json_text(record))
        archive_catalog(catalog, manifest, backup / "catalog-history")
        atomic_text(events_path, "".join(json_text(event).replace("\n", "") + "\n" for event in events))
    else:
        record = dict(previous)
        record["reconciled_at"] = timestamp
        record["warnings"] = warnings
        atomic_text(manifest, json_text(record))
    sync_mirror(catalog, manifest, utilities, backup)
    atomic_bytes(backup / "current" / METADATA, metadata_file.read_bytes())
    source_warnings = archive_owned_sources(utilities, backup)
    setup_recovery_guide(backup, Path(__file__).resolve())
    return f"OK: {len(skills)} skills, {len(plugins)} plugins; {'catálogo atualizado' if changed else 'sem alteração de inventário'}" + (f"; avisos: {'; '.join(source_warnings)}" if source_warnings else "")


def verify(args: argparse.Namespace) -> str:
    codex_home, utilities = Path(args.codex_home), Path(args.utilities)
    catalog = codex_home / "skills-registry" / CATALOG
    manifest = codex_home / "skills-registry" / MANIFEST
    data = validate_primary(catalog, manifest)
    if not data:
        raise RuntimeError("Catálogo principal ainda não existe")
    mirror = utilities / CATALOG
    mirror_manifest = utilities / BACKUP_DIR / "current" / MANIFEST
    if not mirror.is_file() or sha256_file(mirror) != sha256_file(catalog):
        raise RuntimeError("Espelho E: ausente ou diferente do catálogo principal")
    if not mirror_manifest.is_file() or mirror_manifest.read_bytes() != manifest.read_bytes():
        raise RuntimeError("Manifesto de E: ausente ou diferente de C:")
    for package in (utilities / BACKUP_DIR / "owned-sources").glob("*/*.zip"):
        sidecar = package.with_suffix(".sha256")
        if not sidecar.is_file() or sidecar.read_text(encoding="utf-8").strip() != sha256_file(package):
            raise RuntimeError(f"Arquivo de origem sem integridade: {package}")
    return f"OK: C: e E: íntegros; {len(data['skills'])} skills, {len(data['plugins'])} plugins"


def restore(args: argparse.Namespace) -> str:
    if not args.apply:
        raise RuntimeError("Recuperação exige --apply explícito")
    if not re.fullmatch(r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{12}", args.snapshot_id):
        raise RuntimeError("ID de snapshot inválido")
    codex_home, utilities = Path(args.codex_home), Path(args.utilities)
    registry = codex_home / "skills-registry"
    catalog, manifest = registry / CATALOG, registry / MANIFEST
    backup = utilities / BACKUP_DIR
    history = backup / "catalog-history"
    snapshot = history / f"{args.snapshot_id}.md"
    snapshot_manifest = history / f"{args.snapshot_id}.manifest.json"
    sidecar = history / f"{args.snapshot_id}.sha256"
    if not all(path.is_file() for path in (snapshot, snapshot_manifest, sidecar)):
        raise RuntimeError("Snapshot incompleto")
    digest = sha256_file(snapshot)
    if digest != args.expected_sha256 or digest != sidecar.read_text(encoding="utf-8").strip():
        raise RuntimeError("SHA-256 do snapshot não confere")
    restored = load_json(snapshot_manifest)
    if restored.get("catalog_sha256") != digest:
        raise RuntimeError("Manifesto histórico não corresponde ao catálogo")
    validate_primary(catalog, manifest)
    archive_catalog(catalog, manifest, history)
    atomic_bytes(catalog, snapshot.read_bytes())
    atomic_bytes(manifest, snapshot_manifest.read_bytes())
    sync_mirror(catalog, manifest, utilities, backup)
    with (backup / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"at": now(), "kind": "recuperação explícita", "skills": len(restored.get("skills", [])), "plugins": len(restored.get("plugins", []))}, ensure_ascii=False) + "\n")
    return f"OK: snapshot {args.snapshot_id} recuperado; reconciliar com o disco antes de uso"


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--codex-home", default=r"C:\Users\ventu\.codex")
    cli.add_argument("--agents-home", default=r"C:\Users\ventu\.agents")
    cli.add_argument("--utilities", default=r"E:\utilitarios")
    cli.add_argument("--project-root", action="append", default=None, help="Repetir para outras raízes de projetos")
    commands = cli.add_subparsers(dest="command", required=True)
    scan = commands.add_parser("reconcile", help="Ler disco, atualizar C: e espelhar para E:")
    scan.add_argument("--if-stale-days", type=int, default=0)
    scan.add_argument("--no-plugins", action="store_true")
    scan.add_argument("--event", choices=tuple(EVENT_LABELS))
    commands.add_parser("verify", help="Conferir C:, E: e arquivos próprios")
    recovery = commands.add_parser("restore", help="Recuperar um snapshot verificado")
    recovery.add_argument("--snapshot-id", required=True)
    recovery.add_argument("--expected-sha256", required=True)
    recovery.add_argument("--apply", action="store_true")
    return cli


def main() -> int:
    args = parser().parse_args()
    if args.project_root is None:
        args.project_root = [r"E:\projetos-vs"]
    try:
        result = {"reconcile": reconcile, "verify": verify, "restore": restore}[args.command](args)
        print(result)
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(f"ERRO: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
