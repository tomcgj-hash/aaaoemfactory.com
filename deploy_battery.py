#!/usr/bin/env python3
"""Deploy TIANQIU battery-site dist to Vercel as a new static project (no GitHub)."""
import hashlib, json, mimetypes, os, sys, time, urllib.request

TOKEN = open("/opt/data/vercel_token.txt").read().strip()
TEAM = "team_wo6XCZvtZuJeeWOVqHbia1n4"
PROJECT = "tianqiu-battery-oem"
SITE_DIR = "/opt/data/battery-site/dist"
API = "https://api.vercel.com"

def api(method, path, body=None, raw=False, content_type="application/json"):
    data = json.dumps(body).encode() if body is not None and not raw else body
    headers = {"Authorization": f"Bearer {TOKEN}"}
    headers["Content-Type"] = content_type if raw else "application/json"
    req = urllib.request.Request(f"{API}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try: parsed = json.loads(e.read().decode())
        except Exception: parsed = {}
        parsed["_error"] = e.code
        return parsed

def sha1_of(fp):
    h = hashlib.sha1()
    with open(fp, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    # ensure vercel.json present
    vj = os.path.join(SITE_DIR, "vercel.json")
    if not os.path.exists(vj):
        open(vj, "w").write(json.dumps({"framework":None,"buildCommand":None,"outputDirectory":".","devCommand":None,"installCommand":None,"commandForIgnoringBuildStep":None}))
    files = []
    for root, dirs, fnames in os.walk(SITE_DIR):
        for fn in sorted(fnames):
            fp = os.path.join(root, fn)
            files.append({"file": os.path.relpath(fp, SITE_DIR), "sha": sha1_of(fp), "size": os.path.getsize(fp)})
    print(f"本地文件数: {len(files)}", flush=True)
    body = {"files": files, "project": PROJECT, "target": "production", "name": PROJECT,
            "projectSettings": {"framework":None,"buildCommand":None,"outputDirectory":None,"devCommand":None,"installCommand":None,"commandForIgnoringBuildStep":None}}
    sha2fp = {f["sha"]: os.path.join(SITE_DIR, f["file"]) for f in files}
    def create(): return api("POST", f"/v13/deployments?teamId={TEAM}", body)
    r = create()
    missing = (r.get("error") or {}).get("missing") if isinstance(r.get("error"), dict) else None
    if missing:
        print(f"需上传缺失文件: {len(missing)}", flush=True)
        ok = 0
        for i, sha in enumerate(missing, 1):
            fp = sha2fp.get(sha)
            if not fp:
                print(f"  ! 未知 sha: {sha}"); continue
            data = open(fp, "rb").read()
            ct = mimetypes.guess_type(fp)[0] or "application/octet-stream"
            last_err = None
            for attempt in range(4):
                try:
                    req = urllib.request.Request(f"{API}/v2/files?teamId={TEAM}", data=data, method="POST",
                        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": ct, "x-vercel-digest": sha})
                    with urllib.request.urlopen(req, timeout=60) as rr: json.loads(rr.read().decode())
                    last_err = None; break
                except Exception as e:
                    last_err = e; time.sleep(2)
            if last_err:
                print(f"  上传失败 [{i}/{len(missing)}] {os.path.basename(fp)}: {last_err}"); return 1
            ok += 1
            if i % 50 == 0: print(f"  已上传 {i}/{len(missing)}", flush=True)
        print(f"上传完成 {ok}/{len(missing)}，重新创建 deployment...", flush=True)
        r = create()
        if "_error" in r:
            print("二次创建失败:", {k: r[k] for k in r}); return 1
    elif "_error" in r:
        print("创建 deployment 失败:", {k: r[k] for k in r}); return 1
    dep_id = r.get("id") or r.get("uid")
    url = r.get("url")
    print(f"Deployment 创建: {dep_id} | https://{url}", flush=True)
    st = None
    for i in range(30):
        time.sleep(5)
        s = api("GET", f"/v13/deployments/{dep_id}?teamId={TEAM}")
        if "_error" in s:
            print("查询状态失败:", s); break
        st = s.get("readyState") or s.get("status")
        print(f"  [{i*5}s] state={st}", flush=True)
        if st in ("READY", "ERROR", "CANCELED"): break
    if st == "READY":
        print(f"✅ 部署成功: https://{url}")
        print(f"URL=https://{url}")
        return 0
    print("❌ 部署未就绪:", st)
    print(json.dumps(s.get("error", {}))[:500])
    return 1

if __name__ == "__main__":
    sys.exit(main())
