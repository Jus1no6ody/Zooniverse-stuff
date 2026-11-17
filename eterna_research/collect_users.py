"""Bounded Eterna collector. Never treats a repeated page as a full dataset.

The public wiki documents search, but not pagination for type=users.
Default operation probes the old start/size assumption; collection is opt-in.
Even successful traversal does not establish coverage of all historical accounts.
"""
import argparse
import csv
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ENDPOINT = "https://eternagame.org/get/"
FIELDS = ["uid", "name", "points", "synths", "created", "picture"]


class CollectionError(Exception):
    pass


def validate_page(payload):
    try:
        users = payload["data"]["users"]
    except (KeyError, TypeError):
        raise CollectionError("Response is missing data.users; not an empty page.")
    if not isinstance(users, list):
        raise CollectionError("data.users must be an array.")
    ids = set()
    for user in users:
        if not isinstance(user, dict) or not str(user.get("uid") or "").strip():
            raise CollectionError("User record has no valid ID.")
        uid = str(user["uid"])
        if uid in ids:
            raise CollectionError("Duplicate user ID within a page.")
        ids.add(uid)
        try:
            datetime.strptime(user["created"], "%b %d, %Y")
        except (KeyError, TypeError, ValueError):
            raise CollectionError("Missing or invalid registration date.")
    return users


def accept_page(users, seen):
    ids = {str(user["uid"]) for user in users}
    if ids & seen:
        raise CollectionError(
            "Repeated/overlapping IDs across pages. Pagination is unsupported or unstable; stopped."
        )
    seen.update(ids)


def fetch(params, out, index, log):
    url = ENDPOINT + "?" + urlencode(params)
    request = Request(url, headers={"User-Agent": "EternaRegistrationResearch/1.0", "Accept": "application/json"})
    for attempt in range(3):
        entry = {"url": url, "requested_at_utc": datetime.now(timezone.utc).isoformat()}
        try:
            with urlopen(request, timeout=30) as response:
                raw = response.read()
                entry.update(status=response.status, sha256=hashlib.sha256(raw).hexdigest())
            name = f"page_{index:06d}.json"
            (out / name).write_bytes(raw)
            entry["response_file"] = name
            log.append(entry)
            try:
                return validate_page(json.loads(raw))
            except (json.JSONDecodeError, UnicodeDecodeError) as error:
                raise CollectionError("Server did not return valid JSON.") from error
        except HTTPError as error:
            entry["status"] = error.code
            log.append(entry)
            # Access denial/rate limiting is not an invitation to keep requesting.
            if error.code in (401, 403, 429):
                raise CollectionError(f"HTTP {error.code}: access denied or rate limited; no pages skipped.")
            if error.code < 500 or attempt == 2:
                raise CollectionError(f"HTTP {error.code}; no pages skipped.")
        except (URLError, TimeoutError) as error:
            entry["error"] = str(error)
            log.append(entry)
            if attempt == 2:
                raise CollectionError(f"Network failure: {error}; no pages skipped.")
        time.sleep(2 ** (attempt + 1))


def run(args, fetcher=fetch):
    if args.page_size < 1 or args.max_pages < 2 or args.delay < 1:
        raise ValueError("Use page-size >= 1, max-pages >= 2, delay >= 1 second.")
    out = Path(args.output) / datetime.now(timezone.utc).strftime("run_%Y%m%dT%H%M%S_%fZ")
    out.mkdir(parents=True, exist_ok=False)
    manifest = {
        "status": "started", "endpoint": ENDPOINT, "search": "",
        "offset_parameter_under_test": args.offset_param,
        "pagination_verified": False, "population_coverage_verified": False,
        "metric": "Accounts by registration date, not active users or unique people",
        "requests": [], "unique_accounts": 0,
    }
    seen = set()
    total = 0
    result = 1
    try:
        # Fresh run directory ensures a previous result is never silently reused.
        with (out / "users_partial.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS, extrasaction="ignore")
            writer.writeheader()
            limit = args.max_pages if args.collect else 2
            for index in range(limit):
                params = {"type": "users", "search": "", "size": args.page_size,
                          args.offset_param: index * args.page_size}
                users = fetcher(params, out, index, manifest["requests"])
                if not users:
                    if index < 2:
                        raise CollectionError("Insufficient nonempty pages to verify pagination.")
                    manifest["status"] = "traversal_finished_coverage_unverified"
                    result = 0
                    break
                if len(users) != args.page_size:
                    raise CollectionError("Returned page size differs from requested size; pagination unverified.")
                accept_page(users, seen)
                writer.writerows(users)
                stream.flush()
                total += len(users)
                manifest["unique_accounts"] = total
                if index == 1:
                    manifest["pagination_verified"] = True
                print(f"Page {index + 1}: {len(users)} new accounts; {total} total", flush=True)
                if index + 1 < limit:
                    time.sleep(args.delay)
            else:
                manifest["status"] = "page_limit_reached_partial" if args.collect else "probe_passed_coverage_unverified"
                result = 1 if args.collect else 0
    except (CollectionError, OSError) as error:
        manifest.update(status="stopped_incomplete", error=str(error))
        print(str(error), flush=True)
    finally:
        manifest["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"Evidence: {out}", flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(Path(__file__).parent / "runs"))
    parser.add_argument("--offset-param", default="start", choices=["start", "skip", "offset"])
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--max-pages", type=int, default=10000)
    parser.add_argument("--delay", type=float, default=1.5)
    parser.add_argument("--collect", action="store_true")
    raise SystemExit(run(parser.parse_args()))
