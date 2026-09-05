from PIL import Image
import os, shutil

IN="/opt/data/battery-site/incoming/"
OUT="/opt/data/battery-site/public/images/"
os.makedirs(OUT, exist_ok=True)

# hash -> (target_name, max_width)
mapping = {
 "00ab212e90c69f3da8a1673d59da3567.jpg": ("tianqiu-energy-home-storage.jpg", 1200),
 "09031aab8728a29d75edaa333048c5c2.jpg": ("tianqiu-energy-storage-2.jpg", 1200),
 "0aabda1576d3d0d56883b94750bd0487.jpg": ("lithium-button-cell-pack.jpg", 1000),
 "4ca046fad48ba64d0acabd49ec9d90e2.jpg": ("partner-philips-mitsubishi.jpg", 1200),
 "c224765b1c0a88b112ddfa968708c783.jpg": ("stove-aa-battery.jpg", 1000),
 "e591f77983894f2926c18cd5d89577f3.jpg": ("partner-seizi-authorization.jpg", 1200),
 "f107997c6a655c202d5bc1341dcc44d8.jpg": ("tianrui-lithium-module.jpg", 1200),
 "fcf3d26d0cc7ef73683047e94256fc8c.jpg": ("philips-power-alkaline.jpg", 1200),
}
report=[]
for src, (name, mw) in mapping.items():
    sp=IN+src; fp=OUT+name
    im=Image.open(sp).convert("RGB")
    w,h=im.size
    if w>mw:
        nh=int(h*mw/w); im=im.resize((mw,nh), Image.LANCZOS)
    im.save(fp, "JPEG", quality=72, optimize=True)
    nw=os.path.getsize(fp)
    report.append((name, f"{w}x{h}", f"{nw//1024}KB"))
for r in report: print(r)
print("\nSaved to public/images/")
import glob
print("total files:", len(glob.glob(OUT+"*")))
