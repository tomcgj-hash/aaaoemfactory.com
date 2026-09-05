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
key=env.get('DASHSCOPE_API_KEY','')
model=env.get('VISION_MODEL','qwen-vl-max')

def ask(image_b64, prompt):
    url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    payload={"model":model,"messages":[{"role":"user","content":[
        {"type":"image_url","image_url":{"url":f"data:image/png;base64,{image_b64}"}},
        {"type":"text","text":prompt}]}]}
    req=urllib.request.Request(url, data=json.dumps(payload).encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"http_error":e.code,"body":e.read().decode()[:300]}

PROMPT=("这是天球(TIANQIU)电池产品图册的单页。请只提取页面客观文字信息，返回精简JSON，不要臆测规格："
        '{"品牌":"","系列":"","型号列表":["..."],"公司名":"","型号规格(仅图上明确标注的文字)":"","其他文字":""}'
        "如果图上有标注规格数值就列出，没有就留空。只返回JSON。")

targets=[]
# pdf pages 2-10 (page1 done)
for i in range(2,11):
    p=f"/opt/data/battery-site/incoming/pdf_assets/pages/page{i}.png"
    if os.path.exists(p): targets.append((f"PDF页{i}", p))
# user-provided images
for jpg in sorted(glob.glob("/opt/data/battery-site/incoming/*.jpg")):
    targets.append((os.path.basename(jpg)[:12], jpg))

results={}
for name, path in targets:
    try:
        with open(path,'rb') as f: b64=base64.b64encode(f.read()).decode()
        res=ask(b64, PROMPT)
        if "choices" in res:
            txt=res["choices"][0]["message"]["content"]
            results[name]=txt
            print(f"\n===== {name} =====")
            print(txt[:700])
        else:
            print(f"\n===== {name} =====")
            print("ERR", str(res)[:300])
    except Exception as e:
        print(f"\n===== {name} =====")
        print("EXC", e)

with open("/opt/data/battery-site/incoming/vision_results.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\nSAVED vision_results.json")
