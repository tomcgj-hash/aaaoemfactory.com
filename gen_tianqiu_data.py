import json

# ---- 15 SEO battery models -> Tianqiu real specs ----
B = [
  # model, slug, chemistry, chemEn, voltage, diameter, thickness, capacity, weight, compat, apps_en, usVol, longtail, faq
  {"model":"CR2032","slug":"cr2032-battery","chem":"Lithium","chemEn":"lithium","voltage":"3V","diam":"20mm","thick":"3.2mm","cap":"220mAh","wt":"3.0g",
   "compat":"CR2032 = 5004LC = ECR2032 = KCR2032 = DL2032",
   "apps":["Car key fobs","Motherboard CMOS","Electronic scales","Remote controls","Smart locks"],
   "usVol":"90.5K","longtail":["buy","replacement","best for key fob","bulk","vs cr2025","price"],"faq":5},
  {"model":"LR44","slug":"lr44-battery","chem":"Alkaline","chemEn":"alkaline","voltage":"1.5V","diam":"11.6mm","thick":"5.4mm","cap":"150mAh","wt":"2.0g",
   "compat":"LR44 = AG13 = A76 = 357 = SR44",
   "apps":["Calculators","Toys","Watches","Laser pointers","Electronic scales"],
   "usVol":"74.0K","longtail":["replacement","ag13 vs lr44","bulk","equivalent","price"],"faq":4},
  {"model":"CR2025","slug":"cr2025-battery","chem":"Lithium","chemEn":"lithium","voltage":"3V","diam":"20mm","thick":"2.5mm","cap":"165mAh","wt":"2.5g",
   "compat":"CR2025 = ECR2025 = 5003LC = DL2025",
   "apps":["Car key fobs","Remote controls","Motherboards"],
   "usVol":"22.2K","longtail":["replacement","vs cr2032","bulk","price"],"faq":3},
  {"model":"CR2450","slug":"cr2450-battery","chem":"Lithium","chemEn":"lithium","voltage":"3V","diam":"24.5mm","thick":"5.0mm","cap":"620mAh","wt":"6.8g",
   "compat":"CR2450 = ECR2450 = DL2450",
   "apps":["Car key fobs","Motherboards","Sports watches","RFID tags"],
   "usVol":"22.2K","longtail":["replacement","price","bulk"],"faq":2},
  {"model":"AG13","slug":"ag13-battery","chem":"Alkaline","chemEn":"alkaline","voltage":"1.5V","diam":"11.6mm","thick":"5.4mm","cap":"150mAh","wt":"2.0g",
   "compat":"AG13 = LR44 = A76 = 357 = SR44",
   "apps":["Toys","Watches","Laser pointers","Electronic scales"],
   "usVol":"18.1K","longtail":["equivalent","vs lr44","voltage","bulk"],"faq":3},
  {"model":"LR41","slug":"lr41-battery","chem":"Alkaline","chemEn":"alkaline","voltage":"1.5V","diam":"7.9mm","thick":"3.6mm","cap":"32mAh","wt":"0.7g",
   "compat":"LR41 = AG3 = 392 = SR41",
   "apps":["Watches","Thermometers","Glucose meters","Toys"],
   "usVol":"14.8K","longtail":["replacement","vs ag3","price"],"faq":2},
  {"model":"CR2016","slug":"cr2016-battery","chem":"Lithium","chemEn":"lithium","voltage":"3V","diam":"20mm","thick":"1.6mm","cap":"90mAh","wt":"1.7g",
   "compat":"CR2016 = ECR2016 = 5000LC = DL2016",
   "apps":["Car key fobs","Motherboards"],
   "usVol":"9.9K","longtail":["replacement","vs cr2032","bulk"],"faq":2},
  {"model":"CR1632","slug":"cr1632-battery","chem":"Lithium","chemEn":"lithium","voltage":"3V","diam":"16mm","thick":"3.2mm","cap":"140mAh","wt":"1.8g",
   "compat":"CR1632 = ECR1632 = DL1632",
   "apps":["Car key fobs","Remote controls","RFID tags"],
   "usVol":"9.9K","longtail":["replacement","vs cr2032","bulk"],"faq":1},
  {"model":"CR1220","slug":"cr1220-battery","chem":"Lithium","chemEn":"lithium","voltage":"3V","diam":"12.5mm","thick":"2.0mm","cap":"40mAh","wt":"0.8g",
   "compat":"CR1220 = ECR1220 = 5012LC = DL1220",
   "apps":["Motherboards","Remote controls","Small devices"],
   "usVol":"5.4K","longtail":["replacement","vs cr2032","bulk"],"faq":1},
  {"model":"SR44","slug":"sr44-battery","chem":"Silver Oxide","chemEn":"silver oxide","voltage":"1.55V","diam":"11.6mm","thick":"5.4mm","cap":"175mAh","wt":"2.1g",
   "compat":"SR44 = AG13 = LR44 = A76 = 357",
   "apps":["Watches","Calculators","Medical devices"],
   "usVol":"3.6K","longtail":["replacement","vs lr44","price"],"faq":2},
  {"model":"SR626","slug":"sr626-battery","chem":"Silver Oxide","chemEn":"silver oxide","voltage":"1.55V","diam":"6.8mm","thick":"2.6mm","cap":"27mAh","wt":"0.3g",
   "compat":"SR626 = AG4 = 377 = SG4",
   "apps":["Watches","Micro devices"],
   "usVol":"1.9K","longtail":["replacement","vs 377","price"],"faq":2},
  {"model":"LR20","slug":"lr20-battery","chem":"Alkaline","chemEn":"alkaline","voltage":"1.5V","diam":"34.2mm","thick":"61.5mm","cap":"18000mAh","wt":"139g",
   "compat":"LR20 = D cell = R20",
   "apps":["Flashlights","Radios","Industrial equipment","Emergency lighting"],
   "usVol":"1.0K","longtail":["replacement","d cell lr20","price"],"faq":2},
  {"model":"377","slug":"377-battery","chem":"Silver Oxide","chemEn":"silver oxide","voltage":"1.55V","diam":"6.8mm","thick":"2.6mm","cap":"24mAh","wt":"0.3g",
   "compat":"377 = SR626SW = AG4 = SG4",
   "apps":["Watches","Micro devices"],
   "usVol":"3.6K","longtail":["replacement","vs sr626","price"],"faq":5},
  {"model":"371","slug":"371-battery","chem":"Silver Oxide","chemEn":"silver oxide","voltage":"1.55V","diam":"9.5mm","thick":"2.1mm","cap":"38mAh","wt":"0.5g",
   "compat":"371 = SR920SW = AG6 = 370",
   "apps":["Watches","Micro devices"],
   "usVol":"1.6K","longtail":["replacement","vs 377","price"],"faq":5},
  {"model":"364","slug":"364-battery","chem":"Silver Oxide","chemEn":"silver oxide","voltage":"1.55V","diam":"6.8mm","thick":"2.1mm","cap":"18mAh","wt":"0.25g",
   "compat":"364 = SR621SW = AG1 = 379",
   "apps":["Watches","Micro devices"],
   "usVol":"1.3K","longtail":["replacement","vs 377","price"],"faq":5},
]

batteries = []
market_map={"US":None,"AE":"380","SA":"180","EG":"120","NG":"180","ZA":"240"}  # placeholder market values scaled
for b in B:
    batteries.append({
      "model":b["model"],"slug":b["slug"],"url":f"/battery-type/{b['slug']}/",
      "chemistry":b["chem"],"chemistryEn":b["chemEn"],"voltage":b["voltage"],
      "diameter":b["diam"],"thickness":b["thick"],"capacity":b["cap"],"weight":b["wt"],
      "compat":b["compat"],"compatList":[x.strip() for x in b["compat"].split("=")[1:] if x.strip()],
      "applicationsCn":b["apps"],"applicationsEn":b["apps"],"usVolume":b["usVol"],
      "markets":{"AE":"880","SA":"480","EG":"390","NG":"320","ZA":"6.1K"} if b["chem"]=="Lithium" else {"AE":"590","SA":"390","EG":"320","NG":"90","ZA":"1.3K"},
      "longtail":b["longtail"],"faqCount":b["faq"],
      "title":f"{b['model']} Battery - {b['chem']} {b['voltage']} Coin Cell | TIANQIU OEM Manufacturer",
    })

with open("/opt/data/battery-site/src/data/batteries.js","w",encoding="utf-8") as f:
    f.write("// 15 battery models — 天球 TIANQIU real specs + SEO data\n")
    f.write("// Chemistry/voltage/size = Tianqiu catalog (page 8-9). Capacity = industry standard (for reference).\n")
    f.write("export const batteries = "+json.dumps(batteries, ensure_ascii=False, indent=1)+";\n")
    f.write("\nexport function getBattery(slug){ return batteries.find(b => b.slug === slug); }\n")
print("wrote batteries.js:", len(batteries), "models")

# ---- Tianqiu product lines ----
pl = [
 {"id":"cr","name":"Lithium Button Cells","url":"/button-cell-battery/","kw":"cr2032 battery","desc":"CR lithium coin cells: CR2032, CR2025, CR2016, CR1632, CR2450, CR1220 & more. 3V, Hg-free.","img":"cr-button-cell-battery.jpg","family":"lithium"},
 {"id":"ag","name":"Alkaline Button Cells","url":"/button-cell-battery/","kw":"lr44 battery","desc":"AG alkaline button cells: LR44/AG13, LR41, LR626/377, LR754, LR920 & more. 0% mercury.","img":"ag-button-cell-battery.jpg","family":"alkaline"},
 {"id":"silver","name":"Silver Oxide Button Cells","url":"/button-cell-battery/","kw":"sr626 battery","desc":"Silver-oxide watch cells: SR626SW, SR44, 377, 371, 364. High energy for watches & medical.","img":"silver-oxide-battery.jpg","family":"silver"},
 {"id":"cyl-alk","name":"Alkaline Cylindrical","url":"/aa-battery/","kw":"aa battery","desc":"AA / AAA / C / D alkaline & 9V. Japanese Mitsubishi full-automatic line, high capacity.","img":"aa-battery-alkaline.jpg","family":"alkaline"},
 {"id":"cyl-carbon","name":"Carbon Zinc (Heavy Duty)","url":"/d-battery/","kw":"d battery","desc":"R6/R03/R20/R14 heavy-duty & 6F22 9V for affordable everyday power.","img":"carbon-zinc-battery.jpg","family":"carbon"},
 {"id":"rechargeable","name":"Rechargeable & USB","url":"/rechargeable-battery/","kw":"rechargeable battery","desc":"NiMH & rechargeable AA/AAA. Long cycle life, eco-friendly.","img":"rechargeable-battery.jpg","family":"rechargeable"},
 {"id":"hearing","name":"Zinc-Air Hearing Aid","url":"/rechargeable-battery/","kw":"hearing aid battery","desc":"Zinc-air A10/A13/A312/A675 batteries for hearing aids. High-power, long-lasting.","img":"zinc-air-battery.jpg","family":"silver"},
]
with open("/opt/data/battery-site/src/data/productLines.js","w",encoding="utf-8") as f:
    f.write("// 天球 TIANQIU product lines (real)\n")
    f.write("export const productLines = "+json.dumps(pl, ensure_ascii=False, indent=1)+";\n")
print("wrote productLines.js:", len(pl), "lines")

# ---- Company / certifications / factory / partners ----
company = {
  "factoryArea":"100,000 m²","investment":"RMB 1.5 billion","staff":"500+","history":"31+ years",
  "park":"Tianqiu Industrial Park","lines":"Japanese MITSUBISHI full-automatic lines",
  "mercury":"0% mercury alkaline button cell","products":"500+ product types",
  "certifications":["ISO 9001:2015","ISO 45001:2018","BSCI","UL","UN38.3","CE","RoHS","SGS","PONY","Maritime Certification","Air Transport Certification"],
  "partners":[
    {"name":"PHILIPS","desc":"Licensed to manufacture & sell PHILIPS batteries (MMD Hong Kong Holding)","type":"OEM License"},
    {"name":"MITSUBISHI ELECTRIC","desc":"Authorized agent & distributor for Mitsubishi batteries in China","type":"Authorized Agent"},
    {"name":"SEIZI (Japan)","desc":"Sole agent for SEIZI battery range; silver-oxide tech partner with Japan SOXEY","type":"Sole Agent"},
  ],
  "exports":["USA","Germany","Turkey","Spain","Brazil","Italy","South Korea","Dubai","Saudi Arabia","South Africa","Nigeria","Mexico","Indonesia","India","Vietnam","Russia","Poland","Thailand","Malaysia","Philippines","Argentina","Colombia"],
  "trademark":"Madrid Agreement registered in USA, Germany, Japan, Turkey, Hong Kong",
  "group":[
    {"name":"TIANQIU Energy","desc":"Home energy storage systems, smart-lock lithium batteries"},
    {"name":"TIANRUI Energy","desc":"Lithium battery modules & storage: e-bikes, UPS, energy storage cabinets, inverters"},
  ],
}
with open("/opt/data/battery-site/src/data/company.js","w",encoding="utf-8") as f:
    f.write("// 天球 TIANQIU company, certifications, partners & global network (from catalog)\n")
    f.write("export const company = "+json.dumps(company, ensure_ascii=False, indent=1)+";\n")
print("wrote company.js")
