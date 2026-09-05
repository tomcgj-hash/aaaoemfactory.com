import os, base64, json, urllib.request, re

# read key from xy catalog2site env
def load_env(path):
    d={}
    if os.path.exists(path):
        for line in open(path):
            line=line.strip()
            if line and not line.startswith('#') and '=' in line:
                k,v=line.split('=',1); d[k.strip()]=v.strip()
    return d
env=load_env("/opt/data/profiles/xy/home/.catalog2site.env")
# overlay any local defaults
env.get('MINERU_TOKEN')
key=env.get('DASHSCOPE_API_KEY','')
model=env.get('VISION_MODEL','qwen-vl-max')
print("key loaded:", bool(key), "| model:", model)

def b64_img(path):
    with open(path,'rb') as f: return base64.b64encode(f.read()).decode()

def ask(image_b64, prompt, model=model):
    url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    payload={
      "model": model,
      "messages":[{"role":"user","content":[
        {"type":"image_url","image_url":{"url":f"data:image/png;base64,{image_b64}"}},
        {"type":"text","text":prompt},
      ]}],
    }
    req=urllib.request.Request(url, data=json.dumps(payload).encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"http_error":e.code,"body":e.read().decode()[:500]}

img="/opt/data/battery-site/incoming/pdf_assets/pages/page1.png"
b64=b64_img(img)
res=ask(b64,"这是一份电池产品图册的页面。请用中文完整说出:1)页面属于什么产品/系列 2)出现的所有电池型号编号 3)每个型号的规格参数(电压/直径/厚度/容量/化学体系) 4)任何公司名/品牌名/文字内容。尽量详细列出。")
print("=== VISION RESULT page1 ===")
if "choices" in res:
    ct=res["choices"][0]["message"]["content"]
    print(ct)
else:
    print(json.dumps(res, ensure_ascii=False)[:800])
