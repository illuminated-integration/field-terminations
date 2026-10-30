"""Checks data/devices.json so a typo can't break the live site."""
import json
import os
import re
import sys

CATEGORIES = {"Audio", "Lighting", "Network", "Fiber", "Video/RF", "Control"}
REQUIRED = ["id", "title", "manufacturer", "model", "category", "connector", "pins", "source"]
IMAGE_EXT = (".jpg", ".jpeg", ".png", ".webp")
WARN_MB = 10

try:
    with open("data/devices.json", encoding="utf-8") as f:
        devices = json.load(f)
except json.JSONDecodeError as e:
    sys.exit(f"devices.json is not valid JSON: line {e.lineno}, column {e.colno}: {e.msg}\n"
             "Usually a missing comma, or a comma after the last item in a list.")

errors, warnings, seen = [], [], set()


def check_file(name, path, kinds):
    if not path.startswith("media/"):
        errors.append(f"{name}: '{path}' should be inside media/")
    elif not os.path.isfile(path):
        errors.append(f"{name}: file not found: {path} (check spelling and capital letters)")
    elif not path.lower().endswith(kinds):
        errors.append(f"{name}: unexpected file type: {path}")
    elif os.path.getsize(path) > WARN_MB * 1024 * 1024:
        warnings.append(f"{name}: {path} is over {WARN_MB} MB; consider a smaller copy")


for i, d in enumerate(devices):
    name = d.get("id", f"entry #{i + 1}")
    for key in REQUIRED:
        if not d.get(key):
            errors.append(f"{name}: missing '{key}'")
    if d.get("id"):
        if not re.fullmatch(r"[a-z0-9-]+", d["id"]):
            errors.append(f"{name}: id may only use lowercase letters, numbers and dashes")
        if d["id"] in seen:
            errors.append(f"{name}: id is used twice")
        seen.add(d["id"])
    if d.get("category") and d["category"] not in CATEGORIES:
        errors.append(f"{name}: category must be one of {sorted(CATEGORIES)}")
    for p in d.get("pins", []):
        if "pin" not in p or "signal" not in p:
            errors.append(f"{name}: every pin needs 'pin' and 'signal'")
    for im in d.get("images", []):
        if not im.get("file"):
            errors.append(f"{name}: every image needs 'file'")
        else:
            check_file(name, im["file"], IMAGE_EXT)
    for m in d.get("manuals", []):
        if not m.get("file") and not m.get("url"):
            errors.append(f"{name}: a manual needs 'file', 'url', or both")
        if m.get("file"):
            check_file(name, m["file"], (".pdf",))
        if m.get("url") and not re.match(r"https?://", m["url"]):
            errors.append(f"{name}: manual url must start with http:// or https://")

for w in warnings:
    print("Warning:", w)
if errors:
    sys.exit("Problems found:\n- " + "\n- ".join(errors))
print(f"OK: {len(devices)} devices checked.")
