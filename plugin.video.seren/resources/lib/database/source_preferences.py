import datetime
import json
import os
import threading

from resources.lib.modules.globals import g

_lock = threading.Lock()


def _path():
    return os.path.join(g.ADDON_USERDATA_PATH, "source_preferences.json")


def get_source_preference(trakt_id):
    """Return saved source dict for trakt_id, or None."""
    try:
        with _lock:
            with open(_path(), "r") as f:
                return json.load(f).get(str(trakt_id))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def set_source_preference(trakt_id, source):
    """Save source info keyed by trakt_id. Supports torrent and cloud sources."""
    source_type = source.get("type")
    if source_type == "torrent":
        required = {"type", "hash", "magnet", "debrid_provider", "release_title"}
    elif source_type == "cloud":
        required = {"type", "url", "debrid_provider", "release_title"}
    else:
        return
    if not required.issubset(source.keys()):
        return
    entry = {k: source[k] for k in required}
    entry["provider"] = source.get("provider", "")
    entry["quality"] = source.get("quality", "")
    entry["size"] = source.get("size", "")
    entry["saved_at"] = datetime.datetime.utcnow().isoformat()
    try:
        with _lock:
            try:
                with open(_path(), "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError, OSError):
                data = {}
            data[str(trakt_id)] = entry
            with open(_path(), "w") as f:
                json.dump(data, f, indent=2)
    except Exception as e:
        g.log(f"source_preferences: failed to save for trakt_id {trakt_id}: {e}", "warning")
