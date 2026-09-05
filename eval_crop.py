import os, base64, json, urllib.request

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

def ask(b64, prompt):
    url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    p={"model":model,"messages":[{"role":"user","content":[
        {"type":"image_url","image_url":{"url":f"data:image/png;base64,{b64}"}},
        {"type":"text","text":prompt}]}]}
    req=urllib.request.Request(url, data=json.dumps(p).encode(), headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=150) as r: return json.loads(r.read().decode())
    except urllib.error.HTTPError as e: return {"err":e.code,"body":e.read().decode()[:200]}

def prep(path, maxw=1000):
    from PIL import Image
    im=Image.open(path); w,h=im.size
    if w>maxw: im=im.resize((maxw,int(h*maxw/w)))
    import io
    b=io.BytesIO(); im.save(b,"PNG"); return base64.b64encode(b.getvalue()).decode()

for name,path in [("page2 工业园","/opt/data/battery-site/incoming/pdf_assets/images/page2_0_3307x2244.png"),
                  ("page1 新能源","/opt/data/battery-site/incoming/pdf_assets/images/page1_0_3307x2244.png")]:
    b=prep(path)
    prompt="这是电池公司图册的一页。我要从里面裁剪一块最干净、无文字、大气的区域做官网首页全宽背景图（工厂/建筑/能源场景，上面会叠白色标题文字）。请问：1)图里哪里有文字（上/中/下，左/中间/右）？2)哪里是最干净、最适合做背景的画面（工厂建筑群/生产线/能源场景）？3)这个背景主体在图的哪个大致区域？4)如果只保留背景主体，建议裁掉哪些区域？请简洁回答。"
    r=ask(b,prompt)
    print(f"\n===== {name} =====")
    print(r["choices"][0]["message"]["content"] if "choices" in r else str(r)[:300])
