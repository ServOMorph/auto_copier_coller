import time
import os

_start_time = None
_log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "debug.log")

os.makedirs(os.path.dirname(_log_file), exist_ok=True)
with open(_log_file, 'w', encoding='utf-8') as f:
    f.write(f"=== Session demarree {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")


def reset_timer():
    global _start_time
    _start_time = time.time()


def _write_log(line):
    with open(_log_file, 'a', encoding='utf-8') as f:
        f.write(line + "\n")


def log(message):
    global _start_time
    if _start_time is None:
        _start_time = time.time()
    elapsed = time.time() - _start_time
    line = f"[{elapsed:7.2f}s] {message}"
    print(line)
    _write_log(line)


def log_action(action_type, detail=""):
    if detail:
        log(f"ACTION {action_type}: {detail}")
    else:
        log(f"ACTION {action_type}")


def log_click(x, y, description=""):
    if description:
        log(f"CLICK ({x}, {y}) - {description}")
    else:
        log(f"CLICK ({x}, {y})")


def log_key(key, description=""):
    if description:
        log(f"KEY [{key}] - {description}")
    else:
        log(f"KEY [{key}]")


def log_hotkey(keys, description=""):
    keys_str = "+".join(keys)
    if description:
        log(f"HOTKEY [{keys_str}] - {description}")
    else:
        log(f"HOTKEY [{keys_str}]")


def log_wait(duration, reason=""):
    if reason:
        log(f"WAIT {duration}s - {reason}")
    else:
        log(f"WAIT {duration}s")


def log_image_found(image_name, location):
    log(f"IMAGE FOUND: {image_name} at {location}")


def log_image_search(image_name):
    log(f"IMAGE SEARCH: {image_name}")
