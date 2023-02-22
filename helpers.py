from functools import wraps
from flask import session, redirect


def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_func


def get_msec(time_str):
    """Get seconds from time."""
    try:
        if len(time_str.split('.')) == 3:
            m, s, ms = time_str.split('.')
            return int(m) * 60000 + int(s) * 1000 + int(ms)
        elif len(time_str.split('.')) == 2:
            s, ms = time_str.split('.')
            return int(s) * 1000 + int(ms)
    except ValueError:
        return None


def format_time(time_msec):
    m = 0
    s = 0
    ms = 0
    while time_msec > 0:
        if time_msec >= 60000:
            m += 1
            time_msec -= 60000
        elif time_msec >= 1000:
            s += 1
            time_msec -= 1000
        else:
            ms = time_msec
            time_msec = 0
    if m > 0:
        return f"{m:02}:{s:02}.{ms:02}"
    else:
        return f"{s:02}.{ms:02}"
