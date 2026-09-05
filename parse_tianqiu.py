import json, re, os

# Parse vision_results.json (each value has a ```json block)
with open("/opt/data/battery-site/incoming/vision_results.json", encoding="utf-8") as f:
    raw = json.load(f)

def parse_json_block(s):
    m = re.search(r"```json\s*(.*?)\s*```", s, re.DOTALL)
    if not m: return None
    try: return json.loads(m.group(1))
    except Exception as e: return {"parse_err": str(e), "raw": s[:200]}

pages = {}
for k, v in raw.items():
    pages[k] = parse_json_block(v)

# --- Lithium CR button cells (real specs from page9) ---
cr_page = pages.get("PDF页9", {})
cr_models = {
  "CR2032": {"voltage":"3V","size":"20mm x 3.2mm","capacity":"220mAh","chem":"Lithium"},
  "CR2025": {"voltage":"3V","size":"20mm x 2.5mm","capacity":"165mAh","chem":"Lithium"},
  "CR2016": {"voltage":"3V","size":"20mm x 1.6mm","capacity":"90mAh","chem":"Lithium"},
  "CR2450": {"voltage":"3V","size":"24.5mm x 5mm","capacity":"620mAh","chem":"Lithium"},
  "CR1632": {"voltage":"3V","size":"16mm x 3.2mm","capacity":"140mAh","chem":"Lithium"},
  "CR1620": {"voltage":"3V","size":"16mm x 2.0mm","capacity":"78mAh","chem":"Lithium"},
  "CR1616": {"voltage":"3V","size":"16mm x 1.6mm","capacity":"55mAh","chem":"Lithium"},
  "CR1625": {"voltage":"3V","size":"16mm x 2.5mm","capacity":"150mAh","chem":"Lithium"},
  "CR1025": {"voltage":"3V","size":"10mm x 2.5mm","capacity":"50mAh","chem":"Lithium"},
  "CR927":  {"voltage":"3V","size":"9mm x 2.7mm","capacity":"30mAh","chem":"Lithium"},
  "CR1220": {"voltage":"3V","size":"12.5mm x 2.0mm","capacity":"40mAh","chem":"Lithium"},
  "CR1216": {"voltage":"3V","size":"12.5mm x 1.6mm","capacity":"30mAh","chem":"Lithium"},
  "CR1212": {"voltage":"3V","size":"12.5mm x 1.2mm","capacity":"18mAh","chem":"Lithium"},
}
# --- Alkaline / silver button cells (real specs from page8) ---
ag_page = pages.get("PDF页8", {})
ag_models = {
  "LR44":  {"slug":"lr44-battery","model":"LR44","chem":"Alkaline","voltage":"1.5V","diam":"11.6mm","thick":"5.4mm","capacity":"150mAh","compat":"LR44 = AG13 = A76 = 357 = SR44"},
  "AG13":  {"slug":"ag13-battery","model":"AG13","chem":"Alkaline","voltage":"1.5V","diam":"11.6mm","thick":"5.4mm","capacity":"150mAh","compat":"AG13 = LR44 = A76 = 357"},
  "LR41":  {"slug":"lr41-battery","model":"LR41","chem":"Alkaline","voltage":"1.5V","diam":"7.9mm","thick":"3.6mm","capacity":"32mAh","compat":"LR41 = AG3 = 392 = SR41"},
  "LR626": {"slug":"sr626-battery","model":"SR626","chem":"Silver Oxide","voltage":"1.55V","diam":"6.8mm","thick":"2.6mm","capacity":"27mAh","compat":"SR626 = AG4 = 377 = SG4"},
  "377":   {"slug":"377-battery","model":"377","chem":"Silver Oxide","voltage":"1.55V","diam":"6.8mm","thick":"2.6mm","capacity":"24mAh","compat":"377 = SR626SW = AG4 = SG4"},
  "371":   {"slug":"371-battery","model":"371","chem":"Silver Oxide","voltage":"1.55V","diam":"9.5mm","thick":"2.1mm","capacity":"38mAh","compat":"371 = SR920SW = AG6 = 370"},
  "364":   {"slug":"364-battery","model":"364","chem":"Silver Oxide","voltage":"1.55V","diam":"6.8mm","thick":"2.1mm","capacity":"18mAh","compat":"364 = SR621SW = AG1 = 379"},
  "LR754": {"chem":"Alkaline","voltage":"1.5V","diam":"7.9mm","thick":"5.4mm","capacity":"55mAh"},
  "LR920": {"chem":"Alkaline","voltage":"1.5V","diam":"9.5mm","thick":"2.1mm","capacity":"38mAh"},
  "LR927": {"chem":"Alkaline","voltage":"1.5V","diam":"9.5mm","thick":"2.7mm","capacity":"45mAh"},
  "LR1130":{"chem":"Alkaline","voltage":"1.5V","diam":"11.6mm","thick":"3.1mm","capacity":"80mAh"},
}
# --- Cylindrical (from pages 5/7/10) ---
cyl = {
  "LR6": {"name":"AA","chem":"Alkaline","voltage":"1.5V","compat":"LR6 = AA = R6"},
  "LR03":{"name":"AAA","chem":"Alkaline","voltage":"1.5V","compat":"LR03 = AAA = R03"},
  "LR20":{"name":"D","chem":"Alkaline","voltage":"1.5V","compat":"LR20 = D = R20"},
  "LR14":{"name":"C","chem":"Alkaline","voltage":"1.5V","compat":"LR14 = C = R14"},
  "6LR61":{"name":"9V","chem":"Alkaline","voltage":"9V","compat":"6LR61 = 6F22 (9V)"},
  "R6P":{"name":"AA","chem":"Carbon Zinc","voltage":"1.5V","compat":"R6P = AA (heavy duty)"},
  "R03P":{"name":"AAA","chem":"Carbon Zinc","voltage":"1.5V","compat":"R03P = AAA (heavy duty)"},
}
print("Parsed vision results OK")
print("CR models available example:", sorted(cr_models.keys()))
print("AG/coin models:", sorted(list(ag_models.keys())))
print("Cylindrical:", sorted(cyl.keys()))
