import os, base64, json, urllib.request, glob

def load_env(path):
    d={}
    if os.path.exists(path):
        for line in open(path):
            line=line.strip()
            if line and not line.startswith('#') and '=' in line:
                k,v=line.split('=',1); d[k.strip()]=v.strip()
    return d
env=load_env("/opt/data/profiles/xy/home/.catalog2site.env")
key=env.get('DASHSCOPE_API_KEY',''); model=env.get('VISION_MODEL','qwen-vl-max')

def ask(b64):
    url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    p={"model":model,"messages":[{"role":"user","content":[
        {"type":"image_url","image_url":{"url":f"data:image/png;base64,{b64}"}},
        {"type":"text","text":"这是电池公司官网首页候选横版大图。请只返回JSON：{\"主体\":\"\",\"是否适合作为全宽hero背景\":\"yes/no\",\"透明度遮罩后文字可读性\":\"好/中/差\",\"构图\":\"\",\"画面是否干净\":\"yes/no\",\"配色氛围\":\"\"}。不要臆测，基于画面。只返回JSON。"}]}]}
    req=urllib.request.Request(url, data=json.dumps(p).encode(), headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: return json.loads(r.read().decode())
    except urllib.error.HTTPError as e: return {"err":e.code,"body":e.read().decode()[:200]}

# candidate hero images
cands={}
for jpg in sorted(glob.glob("/opt/data/battery-site/incoming/*.jpg")):
    cands["jpg_"+os.path.basename(jpg)[:10]]=jpg
for p in [4,1,2,9]:
    fp=f"/opt/data/battery-site/incoming/pdf_assets/pages/page{p}.png"
    if os.path.exists(fp): cands[f"page{p}"]=fp

results={}
for name,p in cands.items():
    try:
        b=base64.b64encode(open(p,'rb').read()).decode()
        r=ask(b)
        if "choices" in r: results[name]=r["choices"][0]["message"]["content"]
        else: results[name]=str(r)[:200]
        print(f"\n### {name}\n{results[name][:500]}")
    except Exception as e:
        print(f"\n### {name} EXC {e}")

json.dump(results, open("/opt/data/battery-site/hero_eval.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nSAVED hero_eval.json")
