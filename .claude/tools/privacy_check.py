#!/usr/bin/env python3
"""Block personal or secret data before it reaches the public GitHub repo.

The repo is public and watched, so every push is published for good. This checks
the commits a push would publish: their added lines, commit messages and author
emails. See docs/agents/privacy.md for the rule and what to write instead.

Usage:
  privacy_check.py                       commits on HEAD not yet on any origin branch
  privacy_check.py --range A..B          commits in a git range
  privacy_check.py --tree [REF] [PATH..] every tracked file at REF (default HEAD), for audits
  privacy_check.py --pre-push REMOTE URL git pre-push hook mode (ref lines on stdin)

A line that must keep a match (rare, e.g. a doc that quotes a pattern) can carry the
marker  privacy-ok  on the same line. Exit status: 0 clean, 1 findings, 2 usage error.
"""
import re
import subprocess
import sys

# Content of added lines and commit messages.
LINE_PATTERNS = [
    ("home path", re.compile(r"/home/(?!(?:user|username|you|me|runner)\b)[a-z_][a-z0-9_-]*")),
    ("home path", re.compile(r"(?<![\w.])/Users/(?!(?:user|username|you|Shared)\b)[A-Za-z][\w.-]*")),
    ("home path", re.compile(r"\b[A-Za-z]:[\\/]+Users[\\/]+(?!(?:user|username|you|Public)\b)[A-Za-z][\w.-]*", re.I)),
    ("Claude session link", re.compile(r"claude\.ai/(?:code|chat|project)/\S+")),
    ("Claude session id", re.compile(r"\b(?:session|cmsg|chan|user)_01[A-Za-z0-9]{16,}")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})")),
    ("API key", re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{24,}")),
    ("AWS key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[0-9A-Za-z-]{10,}")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("private IP", re.compile(r"\b(?:192\.168|10\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7]))\.\d{1,3}\.\d{1,3}\b")),
    ("email address", re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}\b")),
]
# Only in commit messages: trailers that agent harnesses may add.
MESSAGE_PATTERNS = [("session trailer", re.compile(r"^Claude-Session:", re.M))]
OK_EMAIL = re.compile(r"(?:noreply@anthropic\.com|@users\.noreply\.github\.com|^noreply@github\.com|@example\.(?:com|org)|@paradoxplaza\.com)$", re.I)
SKIP_FILES = re.compile(r"\.(?:dds|png|tga|jpg|jpeg|gif|webp|ttf|otf|fnt|mesh|anim|wav|ogg|bank|v3|pyc)$", re.I)
ALLOW_MARK = "privacy-ok"
ZERO = "0" * 40


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True, errors="replace")
    if check and r.returncode:
        sys.exit(f"privacy_check: git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def line_hits(text):
    if ALLOW_MARK in text:
        return []
    out = []
    for name, pat in LINE_PATTERNS:
        for m in pat.finditer(text):
            if name == "email address" and OK_EMAIL.search(m.group(0)):
                continue
            out.append((name, m.group(0)))
    return out


def known_emails():
    """Author emails already public in origin's history are not new exposure."""
    return set(git("log", "--remotes=origin", "--format=%ae%n%ce").split())


def scan_commits(rev_args):
    findings = []
    shas = git("rev-list", *rev_args).split()
    if not shas:
        return findings
    public = known_emails()
    for sha in shas:
        short = sha[:9]
        meta = git("show", "-s", "--format=%ae%n%ce%n%B", sha)
        ae, ce, msg = meta.split("\n", 2)
        for who, email in (("author", ae), ("committer", ce)):
            if email and not OK_EMAIL.search(email) and email not in public:
                findings.append((short, f"<{who} email>", f"{who} email", email))
        for name, pat in MESSAGE_PATTERNS:
            for m in pat.finditer(msg):
                findings.append((short, "<commit message>", name, m.group(0)))
        for ln in msg.splitlines():
            for name, hit in line_hits(ln):
                if name == "email address" and hit in public:
                    continue  # Co-Authored-By of a known contributor
                findings.append((short, "<commit message>", name, hit))
        diff = git("show", "--format=", "--no-color", "--no-ext-diff", "-U0", "--first-parent", sha)
        path = None
        for ln in diff.splitlines():
            if ln.startswith("+++ "):
                path = ln[6:] if ln.startswith("+++ b/") else None
                continue
            if path is None or not ln.startswith("+") or SKIP_FILES.search(path):
                continue
            for name, hit in line_hits(ln[1:]):
                findings.append((short, path, name, hit))
    return findings


def scan_tree(ref, paths):
    findings = []
    out = git("grep", "-I", "-n", "-E", "-e", ".", ref, "--", *paths, check=False)
    prefix = f"{ref}:"
    for ln in out.splitlines():
        if ln.startswith(prefix):
            ln = ln[len(prefix):]
        path, _, rest = ln.partition(":")
        lineno, _, text = rest.partition(":")
        if SKIP_FILES.search(path):
            continue
        for name, hit in line_hits(text):
            findings.append((ref, f"{path}:{lineno}", name, hit))
    return findings


def pre_push_revs():
    revs = []
    for ln in sys.stdin.read().splitlines():
        parts = ln.split()
        if len(parts) != 4:
            continue
        local_ref, local_sha, remote_ref, remote_sha = parts
        if local_sha == ZERO:
            continue  # deleting a remote branch publishes nothing
        if remote_sha != ZERO and git("cat-file", "-t", remote_sha, check=False).strip():
            revs.append([local_sha, f"^{remote_sha}", "--not", "--remotes=origin"])
        else:
            revs.append([local_sha, "--not", "--remotes=origin"])
    return revs


def report(findings, what):
    if not findings:
        print(f"privacy_check: {what}: clean")
        return 0
    print(f"privacy_check: {what}: {len(findings)} finding(s). Nothing personal or secret may reach the public repo.", file=sys.stderr)
    for where, path, name, hit in findings:
        print(f"  {where}  {path}  {name}: {hit[:120]}", file=sys.stderr)
    print("Fix: use $HOME or relative paths, drop session links/trailers, never commit keys. "
          "Amend or rebase the local commits, then push again. See docs/agents/privacy.md.", file=sys.stderr)
    return 1


def main(argv):
    if not argv:
        return report(scan_commits(["HEAD", "--not", "--remotes=origin"]), "unpushed commits on HEAD")
    if argv[0] == "--range" and len(argv) == 2:
        return report(scan_commits([argv[1]]), argv[1])
    if argv[0] == "--tree":
        ref = argv[1] if len(argv) > 1 else "HEAD"
        return report(scan_tree(ref, argv[2:]), f"tree {ref}")
    if argv[0] == "--pre-push":
        findings = []
        for revs in pre_push_revs():
            findings += scan_commits(revs)
        return report(findings, "push")
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
