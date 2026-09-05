import pymupdf, os, json
PDF="/opt/data/battery-site/incoming/外贸书2025版（1）.pdf"
OUT="/opt/data/battery-site/incoming/pdf_assets"
os.makedirs(OUT+"/images", exist_ok=True)
os.makedirs(OUT+"/pages", exist_ok=True)
doc=pymupdf.open(PDF)
print("PAGES:", doc.page_count)
report=[]
for pno in range(doc.page_count):
    page=doc[pno]
    # extract embedded images
    imgs=page.get_images(full=True)
    imginfos=[]
    for i,img in enumerate(imgs):
        xref=img[0]
        try:
            pix=pymupdf.Pixmap(doc,xref)
            if pix.n>4: pix=pymupdf.Pixmap(pymupdf.csRGB,pix)
            # skip tiny images (logos/icons)
            if pix.width<60 or pix.height<60: continue
            fn=f"{OUT}/images/page{pno+1}_{i}_{pix.width}x{pix.height}.png"
            pix.save(fn)
            imginfos.append(os.path.basename(fn))
        except Exception as e:
            imginfos.append(f"ERR:{e}")
    # render page full
    try:
        pmp=page.get_pixmap(dpi=120)
        pfn=f"{OUT}/pages/page{pno+1}.png"
        pmp.save(pfn)
        pagesz=(pmp.width,pmp.height)
    except Exception as e:
        pfn=None; pagesz=f"ERR:{e}"
    # text layer check
    txt=page.get_text().strip()
    report.append({"page":pno+1,"images":imginfos,"page_png":os.path.basename(pfn) if pfn else None,"page_size":pagesz,"text_chars":len(txt)})
print(json.dumps(report, ensure_ascii=False, indent=1))
