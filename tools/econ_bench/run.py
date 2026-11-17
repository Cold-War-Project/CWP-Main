"""Launch observer games on Forge and record the economy once per in-game year.

One run = one game: take the cwp-vic lock (normal priority, first come first served), link the
worktree, launch, start a new game, switch to observer mode, unpause at max speed, then every poll
copy the newest autosave once it reaches the next sample year, extract it to JSON and delete the
copy (saves are 80-300 MB). The run ends at the end year, on a crash, when the session would
outlast the lock's hold limit, or when another thread queues for the game (development threads
have priority: we stop at the next sample and release the lock).

The menu clicks assume 1920x1080 and the 1.15.1 main menu, as in cwp-observe.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

from .save import extract, SaveError

USER = Path.home() / ".local/share/Paradox Interactive/Victoria 3"
SAVES = USER / "save games"
FORGE = Path(os.environ.get("FORGE", Path.home() / "forge"))
QUEUE = FORGE / ".vic3.queue"
HOLDER = FORGE / ".vic3.lock.holder"

# After --continuelastsave loads a saved game: close any popup, observer mode, max speed, unpause.
RESUME_STEPS = [
    ("key", ("Escape",), 2),
    ("key", ("grave",), 2),
    ("type", ("observe",), 1),
    ("key", ("Return",), 2),
    ("key", ("grave",), 2),
    ("key", ("5",), 1),
    ("key", ("space",), 1),
]

# (action, args, seconds to wait afterwards). Same clicks as cwp-observe: New Game, the first
# bookmark country, Play; then the console `observe`, max speed, unpause.
START_STEPS = [
    ("click", (266, 284), 6),
    ("click", (1086, 330), 100),
    ("click", (566, 702), 8),
    ("key", ("grave",), 2),
    ("type", ("observe",), 1),
    ("key", ("Return",), 2),
    ("key", ("grave",), 2),
    ("key", ("5",), 1),
    ("key", ("space",), 1),
]


def sh(*cmd, check=False, **kw):
    env = dict(os.environ, DISPLAY=os.environ.get("DISPLAY", ":0"))
    return subprocess.run(cmd, text=True, capture_output=True, check=check, env=env, **kw)


def log(out: Path, msg: str):
    line = f"{time.strftime('%F %T')} {msg}"
    print(line, flush=True)
    with open(out / "run.log", "a") as f:
        f.write(line + "\n")


def queue_waiting() -> list[str]:
    """Live tickets in the cwp-vic FIFO (other threads waiting for the game)."""
    out = []
    for t in sorted(QUEUE.glob("*")) if QUEUE.exists() else []:
        pid = t.name.rsplit("-", 1)[-1]
        if pid.isdigit() and Path(f"/proc/{pid}").exists():
            out.append(t.read_text().strip())
    return out


def forge_idle() -> bool:
    held = HOLDER.exists() and HOLDER.read_text().strip() and Path(f"/proc/{HOLDER.read_text().strip()}").exists()
    return not held and not queue_waiting()


def save_date(path: Path):
    with open(path, "rb") as f:
        head = f.read(4000).decode("utf-8", "replace")
    m = re.search(r"game_date=(\d+)\.(\d+)\.(\d+)", head)
    return tuple(int(x) for x in m.groups()) if m else None


def game_running() -> bool:
    return "game:    pid" in sh("cwp-vic", "status").stdout


def stage_resume(resume: Path):
    """Make `resume` the game's "last save" so --continuelastsave loads it."""
    dst = SAVES / "econ_resume.v3"
    shutil.copy2(resume, dst)
    os.utime(dst)
    (USER / "continue_game.json").write_text(json.dumps({
        "title": "econ_resume", "desc": "Observing NONE", "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "rawGameVersion": "1.15.1"}, indent="\t"))


def one_run(worktree: Path, out: Path, end_year: int, every: int, max_minutes: float,
            yield_to_queue: bool, pm_tags) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    resume = out / "resume.v3"
    resuming = resume.exists()
    done = sorted(out.glob("[0-9]*.json"))
    note = f"econ: observer economy run {out.name} to {end_year}" + (" (resume)" if resuming else "")
    r = sh("cwp-vic", "lock", "--wait", "86400", note)
    if r.returncode != 0:
        log(out, f"lock failed: {r.stderr.strip()}")
        return {"status": "no_lock"}
    t0 = time.time()
    status, last_year = "running", None
    try:
        log(out, sh("cwp-vic", "link", str(worktree)).stdout.strip())
        if resuming:
            stage_resume(resume)
            sh("cwp-vic", "launch", "--continuelastsave")
            log(out, f"launched, continuing from {resume.name}")
            time.sleep(300)
            steps = RESUME_STEPS
        else:
            sh("cwp-vic", "launch")
            log(out, "launched; waiting for the main menu")
            time.sleep(170)
            steps = START_STEPS
        started = time.time()
        for act, args, wait in steps:
            if act == "click":
                sh("vic-click", *map(str, args))
            elif act == "key":
                sh("vic-key", *args)
            elif act == "type":
                sh("vic-key", "--type", *args)
            time.sleep(wait)
        sh("vic-shot")  # leaves the latest screenshot for a human to check the start
        log(out, "game started (observer, speed 5)")
        next_year, seen = None, set()
        if done:
            last_year = int(done[-1].name[:4])
            next_year = last_year + every
        while True:
            time.sleep(60)
            if not game_running():
                status = "crash"
                log(out, "GAME NOT RUNNING (crash?)")
                break
            # only autosaves written by this session (the folder also holds other threads' games)
            saves = sorted((p for p in SAVES.glob("autosave*.v3") if p.stat().st_mtime > started),
                           key=lambda p: p.stat().st_mtime)
            if not saves and time.time() - started > 900:
                status = "no_autosave"
                log(out, "no autosave 15 min after launch: the start clicks probably missed (see vic-shot)")
                break
            if saves:
                newest = saves[-1]
                d = save_date(newest)
                if d and d not in seen and (next_year is None or d[0] >= next_year):
                    seen.add(d)
                    time.sleep(3)  # let the writer finish
                    tmp = out / "tmp.v3"
                    shutil.copy2(newest, tmp)
                    try:
                        data = extract(str(tmp), pm_tags=pm_tags)
                        name = f"{d[0]:04d}-{d[1]:02d}-{d[2]:02d}.json"
                        (out / name).write_text(json.dumps(data, separators=(",", ":")))
                        last_year = d[0]
                        next_year = d[0] + every
                        log(out, f"sampled {name}")
                    except (SaveError, Exception) as e:  # a half-written save: try the next one
                        log(out, f"extract failed on {newest.name}: {e}")
                    finally:
                        tmp.unlink(missing_ok=True)
                    if last_year is not None and last_year >= end_year:
                        status = "done"
                        break
                    if yield_to_queue and queue_waiting():
                        status = "yielded"
                        log(out, f"yielding the game to: {queue_waiting()[0]}")
                        break
            if (time.time() - t0) / 60 > max_minutes:
                status = "time_limit"
                log(out, "reached the per-session time limit")
                break
        if status in ("yielded", "time_limit"):
            saves = sorted((p for p in SAVES.glob("autosave*.v3") if p.stat().st_mtime > started),
                           key=lambda p: p.stat().st_mtime)
            if saves:
                shutil.copy2(saves[-1], resume)
                log(out, f"kept {saves[-1].name} ({save_date(resume)}) to resume from")
        elif status == "done":
            resume.unlink(missing_ok=True)
        errs = sh("cwp-vic", "errors").stdout
        with open(out / "errors.txt", "a") as f:
            f.write(errs)
    finally:
        sh("cwp-vic", "unlock")
        log(out, f"lock released; status {status}")
    meta = {"status": status, "last_year": last_year, "wall_minutes": round((time.time() - t0) / 60, 1),
            "worktree": str(worktree),
            "sha": sh("git", "-C", str(worktree), "rev-parse", "--short", "HEAD").stdout.strip()}
    (out / "meta.json").write_text(json.dumps(meta, indent=1))
    return meta


def run_batch(worktree: Path, outdir: Path, runs: int, end_year: int, every: int, max_minutes: float,
              when_idle: bool, yield_to_queue: bool, pm_tags):
    outdir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("CWP_AGENT", "econ")
    # Unfinished runs (yielded or out of time, with a resume save) continue first, then new runs,
    # until `runs` runs have reached the end year.
    sessions = 0
    while True:
        dirs = sorted(p for p in outdir.glob("run-*") if p.is_dir())
        unfinished = [d for d in dirs if (d / "resume.v3").exists()]
        finished = [d for d in dirs if (d / "meta.json").exists() and json.loads((d / "meta.json").read_text()).get("status") == "done"]
        if len(finished) >= runs:
            break
        target = unfinished[0] if unfinished else outdir / f"run-{len(dirs) + 1:03d}"
        if when_idle:
            while not forge_idle():
                time.sleep(120)
        meta = one_run(worktree, target, end_year, every, max_minutes, yield_to_queue, pm_tags)
        sessions += 1
        print(json.dumps({"run": target.name, **meta}), flush=True)
        if meta["status"] in ("no_autosave", "no_lock") or sessions > runs * 6:
            break  # the start sequence is broken (or something keeps failing); don't burn more slots
    sh("bash", "-c", "cwp-vic queue | grep -q . || game-mode off")
