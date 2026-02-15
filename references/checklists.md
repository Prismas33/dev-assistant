# Checklists - Quality Gates

Checklists for different development moments.

---

## 🚀 New Project

### Initial Setup
- [ ] Structured documentation created (`doc/`)
- [ ] MEMORIA.md filled with context
- [ ] First diary entry
- [ ] .gitignore configured
- [ ] Basic README.md
- [ ] Package.json / requirements.txt configured
- [ ] Environment variables documented

### Before First Commit
- [ ] Folder structure defined
- [ ] Linter/formatter configured
- [ ] Git initialized
- [ ] .env.example created

---

## 💻 During Development

### Before Each Commit
- [ ] Code tested locally
- [ ] No `console.log` / `print` debug statements
- [ ] No hardcoded credentials
- [ ] No temporary files
- [ ] Descriptive commit message (conventional commits)

### After Significant Feature
- [ ] Diary entry needed?
- [ ] MEMORIA.md needs update?
- [ ] Components documented?
- [ ] Tests written?

### Code Review Self-Check
- [ ] Code is readable?
- [ ] Descriptive variable names?
- [ ] Small, focused functions?
- [ ] No unnecessary duplication?
- [ ] Proper error handling?

---

## 🐛 Bug Fix

### Before Fixing
- [ ] Bug reproduced locally?
- [ ] Root cause identified?
- [ ] Understood why it happened?

### After Fixing
- [ ] Fix addresses cause, not symptom?
- [ ] Original scenario tested?
- [ ] Edge cases tested?
- [ ] Documented in bugs/ or fixes/?
- [ ] Regression prevented?

### Documentation Template
```markdown
# [BUG/FIX]: Title

**Date:** YYYY-MM-DD
**Severity:** LOW/MEDIUM/HIGH/CRITICAL

## Symptoms
[What was observed]

## Root Cause
[Why it happened]

## Solution
[What was done]

## Prevention
[How to avoid in future]
```

---

## 🚨 Incident/Post-Mortem

### During Incident
- [ ] Impact evaluated
- [ ] Stakeholders notified (if applicable)
- [ ] Logs preserved
- [ ] Timeline being documented

### After Resolution
- [ ] Root cause analysis done
- [ ] Documented in incidents/
- [ ] Action items defined
- [ ] Monitoring improved?

---

## 🚀 Deploy

### Pre-Deploy Checklist
- [ ] All tests pass
- [ ] Build with no errors
- [ ] Environment variables configured
- [ ] Migrations executed (if applicable)
- [ ] Backup done (if applicable)
- [ ] Rollback plan defined

### Post-Deploy Checklist
- [ ] App accessible
- [ ] Critical features tested
- [ ] Logs without errors
- [ ] Metrics normal
- [ ] Documentation updated

---

## 📊 Weekly Review

### What to Review
- [ ] Diary is updated?
- [ ] MEMORIA.md reflects current state?
- [ ] TODOs/FIXMEs in code?
- [ ] Unresolved bugs?
- [ ] Roadmap updated?
- [ ] Technical debt identified?

---

## 🔒 Security (Quick Check)

### Basic
- [ ] Credentials in environment variables?
- [ ] Inputs validated?
- [ ] SQL injection prevented?
- [ ] XSS prevented?
- [ ] CORS configured correctly?
- [ ] Rate limiting implemented?

### Authentication
- [ ] Passwords with secure hash?
- [ ] Tokens with expiration?
- [ ] Sessions managed correctly?
- [ ] CSRF protection?

---

## 📝 End of Session

### Quick Checklist
- [ ] Code committed?
- [ ] Diary updated?
- [ ] Next steps defined?
- [ ] Nothing half-done that will be forgotten?
