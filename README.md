<p align="center">
  <img src="header.png" alt="Abraxas Labs — n8n-databricks-path-join" width="100%">
</p>

<p align="center">
  <a href="https://abraxaslabs.tech"><strong>abraxaslabs.tech</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas">github.com/abraxas</a>
  &nbsp;·&nbsp;
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas/n8n-databricks-path-join">n8n-databricks-path-join</a>
</p>

# n8n-databricks-path-join

**n8n** `2.42.0` — n8n GmbH

Unpublished n8n source finding: Databricks Genie/Vector Search/Files concatenate attacker-controlled path ids without toPathSegment. WHATWG URL normalization turns ../ into GET /api/2.0/secrets/get under the workflow workspace token. Distinct from GHSA-89p4 / GHSA-rqch, which patched other nodes' concat. LangChain VectorStoreDatabricks already uses toPathSegment.

| | |
|---|---|
| ID | Unpublished n8n source finding #2 (no CVE yet) |
| CWE | [CWE-22](https://cwe.mitre.org/data/definitions/22.html) |
| CVSS | **High: 8.6** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Product | [n8n](https://github.com/n8n-io/n8n) |
| Affected | all versions **through 2.42.0** (inclusive) |
| Patched | vendor patch — see references |
| Auth | unauthenticated (see source map) |
| License | [GNU Affero GPL v3.0](LICENSE) |
| Lab | `127.0.0.1` only · vendor/client disclosure pack, not a scanner |

---

## Advisory (from the source map)

getSpace.operation.ts 8-12 concat ${host}/api/2.0/genie/spaces/${spaceId}. vectorSearch/getIndex.operation.ts and files/downloadFile.operation.ts same class. Contrast packages/workflow/src/url.ts toPathSegment. Contrast VectorStoreDatabricks toPathSegment. GHSA-89p4 / GHSA-rqch patched other nodes' concat.

---

## Entry

- **Method:** `POST`
- **Path:** `/webhook/dbx-space`
- **Router:** Databricks Genie getSpace concatenates host + /api/2.0/genie/spaces/${spaceId} with no toPathSegment. WHATWG/undici new URL normalizes ../ and splits ? so GET becomes /api/2.0/secrets/get under the workflow token.
- **Notes:** Unauthenticated unpublished n8n #2 CWE-22 n8n@2.42.0. Needs a victim workflow with a databricksApi credential and untrusted spaceId from a public webhook. Witness: mock GET /api/2.0/secrets/get and N8N-DBX-SECRET-WITNESS in the webhook body. Not n8n host RCE. Disclose GitHub Security Advisories only, not a public GitHub issue.

### Call chain

- `POST /rest/owner/setup`
- `POST /rest/login`
- `POST /rest/credentials type=databricksApi host=mock`
- `POST /rest/workflows Webhook -&gt; Databricks Genie getSpace spaceId={{ $json.body.spaceId }}`
- `POST /rest/workflows/:id/activate`
- `POST /webhook/dbx-space {"spaceId":"../../secrets/get?scope=s&key=k"}`

### Lab preconditions

- n8n 2.42.0 (n8nio/n8n:2.42.0)
- Victim workflow with databricksApi credential bound to untrusted spaceId
- Public webhook (or chat/HTTP) that writes spaceId from JSON
- Workspace token that may GET /api/2.0/secrets/get (lab uses a loopback mock)

### Witness

N8N-DBX-SECRET-WITNESS in webhook body; mock access log GET /api/2.0/secrets/get?scope=s&key=k

### Not success

- eval/base64/system payload
- reverse shell
- n8n host RCE
- ../ stays encoded under /genie/spaces/
- request never leaves /api/2.0/genie/spaces/

---

## Patch / remediation

**Do this first:** Apply the vendor patch for **n8n**. See references.

**Verify after upgrade**

- Re-run `n8n-databricks-path-join-Abraxas-Labs.py` against the patched build: the mapped witness must **not** appear.
- Confirm the vendor advisory / changeset in the deployed tree (see references).
- A WAF signature is delay, not a patch.

**If you cannot update immediately**

- Disable or isolate the affected component.
- Hunt for the witness condition on production (new privileged users, unexpected files, injected rows — whatever this CVE's map names).

---

## Reproduction (authorized lab)

Target **only** `http://127.0.0.1:18202` (n8n) and `http://127.0.0.1:18203` (Databricks mock). Do not point this script at the internet.

Official image `n8nio/n8n:2.42.0` on loopback `:18202` plus the mock on `:18203`. Then:

```bash
cd lab
./run.sh
```

Or, with the stack already up:

```bash
python3 n8n-databricks-path-join-Abraxas-Labs.py http://127.0.0.1:18202 http://127.0.0.1:18203
```

Success is `N8N-DBX-SECRET-WITNESS` in the webhook body and mock `GET /api/2.0/secrets/get`. Generic 200 HTML is not it.

---

## Lab images

Loopback stack used to reproduce. Official images unless a `Dockerfile` in this folder builds from source.

- [`lab/docker-compose.yml`](lab/docker-compose.yml)
- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/run.sh`](lab/run.sh)
- [`lab/mock/Dockerfile`](lab/mock/Dockerfile)
- [`lab/mock/server.py`](lab/mock/server.py)

Publish nothing except `127.0.0.1`.

---

## References

- [github.com/n8n-io/n8n](https://github.com/n8n-io/n8n) tag n8n@2.42.0
- Sibling leftover: [GHSA-89p4-6h98-c7xm](https://github.com/n8n-io/n8n/security/advisories/GHSA-89p4-6h98-c7xm) · [GHSA-rqch-9jrh-cr8w](https://github.com/n8n-io/n8n/security/advisories/GHSA-rqch-9jrh-cr8w)
- Vendor intake: [GitHub Security Advisories](https://github.com/n8n-io/n8n/security/advisories/new). Do **not** open a public GitHub issue.

- Abraxas Labs: [abraxaslabs.tech](https://abraxaslabs.tech) · [github.com/abraxas](https://github.com/abraxas) · [@abraxas_null](https://x.com/abraxas_null)

---

## Records (structured)

```
# n8n unpublished #2 — Databricks path join reaches Secrets API

CWE: CWE-22
Severity: High (HTTP lab SUCCESS, 80%)

## Description

Databricks Genie `getSpace` concatenates `spaceId` into `${host}/api/2.0/genie/spaces/${spaceId}` with no `toPathSegment`. A public webhook that binds untrusted JSON into that id lets WHATWG URL normalize `../` and split `?`, so the workflow token issues `GET /api/2.0/secrets/get`. Same class as GHSA-89p4 / GHSA-rqch. LangChain VectorStoreDatabricks already encodes the index path.

## Product

n8n 2.42.0 (`n8nio/n8n:2.42.0`). Lab oracle: `N8N-DBX-SECRET-WITNESS` in the webhook body and mock `GET /api/2.0/secrets/get?scope=s&key=k`. Credential leak on the Databricks tenant, not n8n RCE.
```

---

## License

This disclosure pack is licensed under the **GNU Affero General Public License v3.0**. See [LICENSE](LICENSE).

---

## Disclaimer

This pack is for **the vendor, the site owner, and licensed labs**. The script talks to `127.0.0.1`. Using it against systems you do not own is not authorized by Abraxas Labs. No warranty.

<p align="center">
  <a href="https://abraxaslabs.tech">abraxaslabs.tech</a> ·
  <a href="https://github.com/abraxas">github.com/abraxas</a> ·
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
</p>
