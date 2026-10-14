from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
from urllib.parse import unquote

root = Path(__file__).resolve().parent
assert (root / "AGENTS.md").read_bytes() == (root / "CLAUDE.md").read_bytes(), "Instruction mirrors differ"
records = json.loads((root / "provenance.json").read_text())
sample = next(r for r in records if r.get("kind") == "runnable sample")
assert hashlib.sha256((root / sample["public_path"]).read_bytes()).hexdigest() == sample["sample_sha256"], "Original sample changed; update provenance explicitly"
patterns = [r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", r"(?:github_pat_|ghp_)[A-Za-z0-9_]{20,}", r"\bsk-(?:proj-)?[A-Za-z0-9_-]{25,}", r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}", r"\bAIza[A-Za-z0-9_-]{30,}", r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"]
for path in root.rglob("*"):
    if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts: continue
    if path.suffix == ".pyc": continue
    rel = path.relative_to(root)
    assert not path.is_symlink(), "Symlink in publication"
    assert not (path.name.startswith(".env") or path.name.startswith("cloudbuild") or "clients" in rel.parts or (".github" in rel.parts and "workflows" in rel.parts)), "Operational file in portfolio"
    text = path.read_text(errors="replace")
    assert not any(re.search(rx,text) for rx in patterns), "Credential-shaped value in " + str(rel)
    if path.suffix != ".md": continue
    visible=[]; fence=None
    for line in text.splitlines():
        mark=re.match(r"^\s*(`{3,}|~{3,})",line)
        if mark:
            run=mark.group(1)
            if fence is None: fence=run
            elif run[0]==fence[0] and len(run)>=len(fence): fence=None
            continue
        if fence is None: visible.append(line)
    for target in re.findall(r"\]\(([^)]+)\)","\n".join(visible)):
        if target.startswith(("http:","https:","mailto:","#")):continue
        target=unquote(target.split("#",1)[0])
        assert (path.parent/target).resolve().is_relative_to(root), "Local link escapes repository"
        assert (path.parent/target).exists(), "Broken local link: " + target
result=subprocess.run([sys.executable,"-I",str(root/"demo.py")],check=True,capture_output=True,text=True)
receipt=json.loads(result.stdout)
expected=json.loads((root/"verification.json").read_text())
assert receipt==expected, "Published receipt no longer matches execution"
print(json.dumps({"local_links":"passed","instruction_parity":"passed","source_hash":"passed","credential_pattern_scan":"passed","offline_checks":receipt["passed"]}))
