import fs from 'fs';
import path from 'path';
const dir='/tmp/tmmq_batteries';
const out={};
for (const f of fs.readdirSync(dir)) {
  if(!f.endsWith('.js')) continue;
  const type=f.replace('.js','');
  const src=fs.readFileSync(path.join(dir,f),'utf8');
  try{
    const window={};
    new Function('window', src)(window);
    out[type]=window.batteryConfig || {error:'no config'};
  }catch(e){
    out[type]={parse_error:e.message};
  }
}
fs.writeFileSync('/opt/data/battery-site/tools_all_battery_config.json', JSON.stringify(out,null,0));
fs.writeFileSync('/opt/data/battery-site/tools_all_battery_config.min.json', JSON.stringify(out));
console.log('parsed', Object.keys(out).length, 'types');
for(const [t,c] of Object.entries(out)){
  const en=c.localized?.en||{};
  const gi=en.generalInfoItems||[];
  const v=gi.find(i=>String(i.label||'').toLowerCase().includes('voltage'))?.value|| '';
  const cap=gi.find(i=>String(i.label||'').toLowerCase().includes('capacity'))?.value||'';
  const w=gi.find(i=>String(i.label||'').toLowerCase().includes('weight'))?.value||'';
  const cr=gi.find(i=>String(i.label||'').toLowerCase().includes('material')||String(i.label||'').toLowerCase().includes('chem'))?.value||'';
  const pt=en.perfTable||{};
  console.log(t.padEnd(9),'|',(c.shortModel||'').padEnd(9),'| V:',String(v).padEnd(7),'| cap:',String(cap).padEnd(13),'| W:',String(w).padEnd(8),'| chem:',String(cr).slice(0,26),'| perfRows:',(pt.rows?.length||0));
}
