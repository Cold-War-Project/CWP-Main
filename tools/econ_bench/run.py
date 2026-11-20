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
import signal
import subprocess
import sys
import time
from pathlib import Path

from .save import extract, SaveError

# Years whose sampled save is kept next to the JSON (env ECON_KEEP_YEARS="1948,1950").
KEEP_YEARS = {int(y) for y in os.environ.get("ECON_KEEP_YEARS", "").split(",") if y.strip().isdigit()}
MIN_PLAY = 30      # minutes a benchmark run plays before yielding to another benchmark run
MIN_PLAY_DEV = 15  # ... before yielding to other (non-priority) work
USER = Path.home() / ".local/share/Paradox Interactive/Victoria 3"
SAVES = USER / "save games"
FORGE = Path(os.environ.get("FORGE", Path.home() / "forge"))
QUEUE = FORGE / ".vic3.queue"
HOLDER = FORGE / ".vic3.lock.holder"

# After --continuelastsave the game opens the save in the lobby. Sometimes Observer is preselected,
# sometimes nothing is (2026-11-17), and the Observe button toggles, so: Random Country, Start, then
# the console `observe`. vic-click takes coordinates on the 1280x720 vic-shot image.
RESUME_STEPS = [
    ("click", (426, 702), 4),     # Random Country
    ("click", (1146, 696), 25),   # Start
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


def launch(out: Path, *args):
    """cwp-vic launch with output to a file: the game inherits the launcher's stdout, so a pipe
    (capture_output) would never reach EOF and the call would block until the game exits."""
    env = dict(os.environ, DISPLAY=os.environ.get("DISPLAY", ":0"))
    with open(out / "launch.out", "a") as f:
        return subprocess.run(["cwp-vic", "launch", *args], stdout=f, stderr=subprocess.STDOUT,
                              stdin=subprocess.DEVNULL, env=env, timeout=600)


def clear_popups(out: Path):
    """Close desktop popups that steal the game's clicks and keys (the GNOME "Unlock Keyring" prompt
    after a fresh login swallowed the console `observe` on 2026-11-17). Same as cwp-observe."""
    r = sh("xdotool", "search", "--name", "Unlock Keyring|Authentication required")
    for w in r.stdout.split():
        name = sh("xdotool", "getwindowname", w).stdout.strip()
        if sh("xdotool", "windowclose", w).returncode != 0:
            sh("xdotool", "windowkill", w)
        log(out, f"closed popup: {name}")


def sh(*cmd, check=False, **kw):
    env = dict(os.environ, DISPLAY=os.environ.get("DISPLAY", ":0"))
    return subprocess.run(cmd, text=True, capture_output=True, check=check, env=env, **kw)


def log(out: Path, msg: str):
    line = f"{time.strftime('%F %T')} {msg}"
    print(line, flush=True)
    with open(out / "run.log", "a") as f:
        f.write(line + "\n")


def queue_waiting(with_priority: bool = False) -> list:
    """Live tickets in the cwp-vic FIFO (other threads waiting for the game): their notes, or
    (note, is_priority) pairs. A --priority ticket's name starts with 1, a normal one with 5."""
    out = []
    for t in sorted(QUEUE.glob("*")) if QUEUE.exists() else []:
        pid = t.name.rsplit("-", 1)[-1]
        if pid.isdigit() and Path(f"/proc/{pid}").exists():
            try:
                note = t.read_text().strip()
            except FileNotFoundError:
                continue
            out.append((note, t.name.startswith("1")) if with_priority else note)
    return out


def forge_idle() -> bool:
    held = HOLDER.exists() and HOLDER.read_text().strip() and Path(f"/proc/{HOLDER.read_text().strip()}").exists()
    return not held and not queue_waiting()


def mtime(p: Path) -> float:
    try:
        return p.stat().st_mtime
    except FileNotFoundError:  # rotated away between glob and stat
        return 0.0


def save_date(path: Path):
    try:
        with open(path, "rb") as f:
            head = f.read(4000).decode("utf-8", "replace")
    except FileNotFoundError:
        return None
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
    # The note must contain CWP_AGENT: `cwp-vic unlock` refuses to release a lock whose note doesn't.
    agent = os.environ.get("CWP_AGENT", "econ")
    note = f"{agent}: econ_bench observer run {out.name} to {end_year}" + (" (resume)" if resuming else "")
    # Popen, so that if this process is stopped while waiting, the waiting `cwp-vic lock` goes too
    # (otherwise it takes the lock later for nobody and holds it for two hours).
    lock = subprocess.Popen(["cwp-vic", "lock", "--wait", "86400", "--owner-pid", str(os.getpid()), note], text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        _, err = lock.communicate()
    except BaseException:
        lock.terminate()
        try:
            lock.wait(timeout=10)
        except subprocess.TimeoutExpired:
            lock.kill()  # its queue ticket is dropped once the pid is dead
        raise
    if lock.returncode != 0:
        log(out, f"lock failed: {err.strip()}")
        return {"status": "no_lock"}
    t0 = time.time()
    status, last_year = "running", None
    try:
        log(out, sh("cwp-vic", "link", str(worktree)).stdout.strip())
        if resuming:
            stage_resume(resume)
            launch(out, "--continuelastsave")
            log(out, f"launched, continuing from {resume.name}")
            time.sleep(300)
            steps = RESUME_STEPS
        else:
            launch(out)
            log(out, "launched; waiting for the main menu")
            time.sleep(170)
            steps = START_STEPS
        started = time.time()
        for act, args, wait in steps:
            clear_popups(out)
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
            saves = sorted((p for p in SAVES.glob("autosave*.v3") if mtime(p) > started), key=mtime)
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
                    try:
                        shutil.copy2(newest, tmp)  # autosaves rotate; the file can vanish mid-copy
                        data = extract(str(tmp), pm_tags=pm_tags)
                        if d[0] in KEEP_YEARS:  # other threads asked for this save
                            shutil.copy2(tmp, out / f"{d[0]:04d}-{d[1]:02d}-{d[2]:02d}.v3")
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
                    waiting = queue_waiting(with_priority=True)
                    played = (time.time() - started) / 60
                    # Loading costs ~8 minutes, so a run plays a while before giving the game up:
                    # --priority tickets at once, other work after MIN_PLAY_DEV minutes, another
                    # benchmark run after MIN_PLAY (two runners yielding to each other after one
                    # sample each made no progress, 2026-11-17). Agreed with the coordinator 2026-11-18.
                    prio = [n for n, p in waiting if p]
                    dev = [n for n, p in waiting if not p and "econ_bench" not in n]
                    bench = [n for n, p in waiting if not p and "econ_bench" in n]
                    due = prio or (dev if played >= MIN_PLAY_DEV else []) or (bench if played >= MIN_PLAY else [])
                    if yield_to_queue and due:
                        status = "yielded"
                        log(out, f"yielding the game to: {due[0]} (after {played:.0f} min of play)")
                        break
            if (time.time() - t0) / 60 > max_minutes:
                status = "time_limit"
                log(out, "reached the per-session time limit")
                break
        if status in ("yielded", "time_limit"):
            saves = sorted((p for p in SAVES.glob("autosave*.v3") if mtime(p) > started), key=mtime)
            for cand in reversed(saves):
                try:
                    shutil.copy2(cand, resume)
                    log(out, f"kept {cand.name} ({save_date(resume)}) to resume from")
                    break
                except FileNotFoundError:
                    continue
        elif status == "done":
            resume.unlink(missing_ok=True)
        errs = sh("cwp-vic", "errors").stdout
        with open(out / "errors.txt", "a") as f:
            f.write(errs)
    finally:
        u = sh("cwp-vic", "unlock")
        if u.returncode != 0:  # never leave the game running and the lock held
            log(out, f"unlock refused ({u.stderr.strip()}); stopping our game and forcing the unlock")
            sh("cwp-vic", "stop")
            sh("cwp-vic", "unlock", "--force")
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
    # `kill` (TERM/HUP) runs the cleanup in one_run: drop the queue ticket, or stop the game and unlock.
    for sig in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, lambda *_: sys.exit(1))
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
        # A failed start leaves a fresh run with nothing to resume: something is wrong with the start
        # sequence, so stop. A failed resume keeps its save and is retried (up to the session cap).
        fresh_fail = meta["status"] == "no_autosave" and not (target / "resume.v3").exists()
        if fresh_fail or meta["status"] == "no_lock" or sessions > runs * 6:
            break  # the start sequence is broken (or something keeps failing); don't burn more slots
    sh("bash", "-c", "cwp-vic queue | grep -q . || game-mode off")
