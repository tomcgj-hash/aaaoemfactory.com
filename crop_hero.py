import os, base64, json, urllib.request, io
from PIL import Image

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

path="/opt/data/battery-site/incoming/pdf_assets/images/page2_0_3307x2244.png"
im=Image.open(path); W,H=im.size
s=im.resize((1000,int(H*1000/W)))
b=io.BytesIO(); s.save(b,"PNG")
r=ask(base64.b64encode(b.getvalue()).decode(),
 "这是工厂图册页。请给出图中最高级、最干净、无文字、最适合做网站全宽背景的『工厂建筑群+天空+绿化』区域的精确边界框。只输出JSON: {\"xmin\":0-1,\"ymin\":0-1,\"xmax\":0-1,\"ymax\":0-1}，坐标是相对整图(0=左/上,1=右/下)，框住那一片干净的建筑+天空+绿化背景，不要包含文字和建筑前的杂物。只返回JSON。")
txt=r["choices"][0]["message"]["content"] if "choices" in r else str(r)[:300]
print("bbox:",txt)
import re
m=re.search(r'\{[^}]*\}', txt)
box=json.loads(m.group(0)) if m else None
if box:
    x0,y0,x1,y1=box["xmin"],box["ymin"],box["xmax"],box["ymax"]
    # expand to 16:9-ish + padding, then crop from original
    import math
    # convert to px
    px0,py0,px1,py1=int(x0*W),int(y0*H),int(x1*W),int(y1*H)
    # add padding (avoid cutting subjects tight)
    pad=0.0
    px0=max(0,int(px0-(px1-px0)*pad)); px1=min(W,int(px1+(px1-px0)*pad))
    py0=max(0,int(py0-(py1-py0)*pad)); py1=min(H,int(py1+(py1-py0)*pad))
    crop=im.crop((px0,py0,px1,py1))
    cw,ch=crop.size
    # normalize to 1920x1000 (approx 16:8.4) center crop
    tw=1920; th=1000
    if cw>tw: crop=crop.resize((tw,int(ch*tw/cw)), Image.LANCZOS)
    crop.save("/opt/data/battery-site/public/images/hero-factory.jpg","JPEG",quality=80,optimize=True)
    import os as _o
    print("cropped",crop.size,"saved",_o.path.getsize("/opt/data/battery-site/public/images/hero-factory.jpg")//1024,"KB")
