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

def ask(b64):
    url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    p={"model":model,"messages":[{"role":"user","content":[
        {"type":"image_url","image_url":{"url":f"data:image/png;base64,{b64}"}},
        {"type":"text","text":"这是电池公司网站首页候选背景图。请只返回JSON：{\"画面文字多不多\":\"无文字/很少/较多/满屏文字\",\"主体\":\"\",\"构图\":\"\",\"画面空旷度(越空越适合做背景)\":\"高/中/低\",\"整体配色\":\"\",\"适不适合做全宽hero背景(文字会叠在图左)\":\"yes/no\"}。基于画面，不臆测。只返回JSON。"}]}]}
    req=urllib.request.Request(url, data=json.dumps(p).encode(), headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: return json.loads(r.read().decode())
    except urllib.error.HTTPError as e: return {"err":e.code,"body":e.read().decode()[:200]}

cands={
 "jpg_00ab":"/opt/data/battery-site/incoming/00ab212e90c69f3da8a1673d59da3567.jpg",
 "jpg_0903":"/opt/data/battery-site/incoming/09031aab8728a29d75edaa333048c5c2.jpg",
 "jpg_c224":"/opt/data/battery-site/incoming/c224765b1c0a88b112ddfa968708c783.jpg",
 "jpg_fcf3":"/opt/data/battery-site/incoming/fcf3d26d0cc7ef73683047e94256fc8c.jpg",
 "jpg_0aab":"/opt/data/battery-site/incoming/0aabda1576d3d0d56883b94750bd0487.jpg",
 "page1":"/opt/data/battery-site/incoming/pdf_assets/images/page1_0_3307x2244.png",
}
res={}
for n,p in cands.items():
    try:
        b=base64.b64encode(open(p,'rb').read()).decode()
        r=ask(b)
        res[n]=r["choices"][0]["message"]["content"] if "choices" in r else str(r)[:200]
        print(f"\n### {n}\n{res[n][:600]}")
    except Exception as e: print(f"\n### {n} EXC {e}")
json.dump(res,open("/opt/data/battery-site/hero_eval2.json","w"),ensure_ascii=False,indent=1)
