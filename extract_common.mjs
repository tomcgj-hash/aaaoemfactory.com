import fs from 'fs';
const src=fs.readFileSync('/tmp/common.js','utf8');
const window={};
const document={addEventListener:()=>{},getElementById:()=>null,querySelectorAll:()=>[]};
try{
  new Function('window','document', src + '\n;return COMMON_LANG;')(window, document);
}catch(e){ console.error('exec err',e.message); }
const get=()=>{ let r=null; const doc={addEventListener:()=>{},getElementById:()=>null,querySelectorAll:()=>[]}; const w={}; const f=new Function('window','document', src+'\n;window.__CL=COMMON_LANG;'); f(w,doc); return w.__CL; };
const CL=get();
if(!CL){ console.log('FAILED to get COMMON_LANG'); process.exit(1); }
const en=CL.en||{};
// select fields useful for detail page
const out={
  manufacturer: en.manufacturer,
  euRep: en.euRep,
  hazardousBase: en.hazardousBase,
  extinguisher: en.extinguisher,
  markingTitle: en.markingTitle,
  warning:{ title: en.warning?.title, items: en.warning?.items, caution: en.warning?.cautionItems },
  conformity: en.conformity,
  waste:{ title: en.waste?.title, html: en.waste?.html },
  relatedDocs: en.relatedDocs,
  footer: en.footer,
  symbolTexts: en.ui?.symbolTexts || [],
  docSubtitleSuffix: en.docSubtitleSuffix,
  compliancePrefix: en.compliancePrefix,
};
fs.writeFileSync('/opt/data/battery-site/src/data/eu_compliance.js',
  '// EU common compliance info (from tmmq.top common.js COMMON_LANG.en)\n'+
  'export const euCompliance = '+JSON.stringify(out,null,1)+';\n');
console.log('wrote eu_compliance.js. keys:',Object.keys(out).join(', '));
console.log('warning items:',(en.warning?.items||[]).length,'| caution:',(en.warning?.cautionItems||[]).length);
