import os, base64, json, urllib.request, sys

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
    except urllib.error.HTTPError as e: return {"err":e.code,"body":e.read().decode()[:300]}

# resize screenshot for vision
from PIL import Image
def prep(path, out, maxw=1200):
    if not os.path.exists(path): return None
    im=Image.open(path); w,h=im.size
    if w>maxw: im=im.resize((maxw,int(h*maxw/w)))
    im.save(out, optimize=True); return out

shot=sys.argv[1] if len(sys.argv)>1 else "/opt/data/battery-site/shot_home.png"
prepped=prep(shot,"/opt/data/battery-site/shot_vis.png")
if not prepped: print("no screenshot"); sys.exit()
b=base64.b64encode(open(prepped,'rb').read()).decode()
prompt="这是电池制造商外贸官网的整页截图（网站首页，顶部是深蓝大图+白色大标题，下面是产品卡、深蓝区块、行业应用、联系表单）。请以专业网页设计师眼光客观指出：1) 整体哪里显得奇怪/不协调/突兀？2) 具体是哪一块（顶部hero/某区块/配色/对比/排版/间距/过渡）？3) 如果能改进的1-3个具体建议。4) 整体气质是否像一个专业的电池工厂官网？直接给结论，先列最明显的问题。"
r=ask(b, prompt)
if "choices" in r:
    print("=== 视觉分析 ===")
    print(r["choices"][0]["message"]["content"])
else:
    print(json.dumps(r,ensure_ascii=False)[:500])
