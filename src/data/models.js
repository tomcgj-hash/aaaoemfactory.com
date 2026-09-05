// 型号总览 — [型号名, 详情页slug(null=on request), 产品图]
// 优先使用拆解画册里的对应型号真实图(catalog/model-*.jpg)；无画册图的用产品净图或通用占位
const BTN='/images/products/__btn.png';
export const buttonLines = [
  { line: 'Lithium Coin Cells (CR)', models: [
    ['CR2032','cr2032','/images/catalog/model-CR2032.jpg'],['CR2450','cr2450','/images/catalog/model-CR2450.jpg'],
    ['CR2025','cr2025','/images/catalog/model-CR2025.jpg'],['CR2016','cr2016','/images/catalog/model-CR2016.jpg'],
    ['CR1220',null,BTN],['CR1025','cr1025','/images/catalog/model-CR1025.jpg'],['CR927',null,'/images/catalog/model-CR927.jpg'],
    ['CR1632',null,'/images/catalog/model-CR1632.jpg'],['CR1625',null,'/images/catalog/model-CR1625.jpg'],
    ['CR1620',null,'/images/catalog/model-CR1620.jpg'],['CR1616',null,'/images/catalog/model-CR1616.jpg'],
    ['CR1216',null,'/images/catalog/model-CR1216.jpg'],['CR1212',null,'/images/catalog/model-CR1212.jpg']
  ]},
  { line: 'Alkaline Button Cells (LR / AG)', models: [
    ['LR44','lr44','/images/products/lr44.png'],['LR41','lr41','/images/catalog/model-LR41.jpg'],
    ['LR626','lr626','/images/catalog/model-LR626.jpg'],['LR754','lr754','/images/products/lr754.png'],
    ['LR1130','lr1130','/images/catalog/model-LR1130.jpg'],['LR521','lr521','/images/catalog/model-LR521.jpg'],
    ['LR621','lr621','/images/catalog/model-LR621.jpg'],['LR726','lr726','/images/catalog/model-LR726.jpg'],
    ['LR920','lr920','/images/catalog/model-LR920.jpg'],['LR927','lr927','/images/catalog/model-LR927.jpg'],
    ['LR936','lr936','/images/catalog/model-LR936.jpg'],['LR721','lr721','/images/catalog/model-LR721.jpg'],
    ['LR43','lr43','/images/catalog/model-LR43.jpg'],['LR1120','lr1120','/images/products/lr1120.png']
  ]},
];
const AA='/images/catalog/aa-pack.jpg', AAA='/images/catalog/aaa-pack.jpg', DP='/images/catalog/d-pack.jpg';
export const aaLine = [ { line: 'AA Cylindrical (LR6 / R6)', models: [
  ['LR6','lr6','/images/catalog/model-LR6.jpg'],['R6P','r6p','/images/catalog/model-R6P.jpg'],
  ['LR6 2BP',null,AA],['LR6 4BP',null,AA],['LR6 8BP',null,AA]
] } ];
export const aaaLine = [ { line: 'AAA Cylindrical (LR03 / R03)', models: [
  ['LR03','lr03','/images/catalog/model-LR03.jpg'],['R03','r03','/images/catalog/model-R03.jpg'],
  ['LR03 2BP',null,AAA],['LR03 4BP',null,AAA]
] } ];
export const dLine = [ { line: 'C & D Cylindrical (LR14 / LR20)', models: [
  ['LR20',null,'/images/catalog/model-LR20.jpg'],['LR14',null,DP]
] } ];
export const nineVoltLine = [ { line: '9V (6LR61 / 6F22)', models: [
  ['6LR61','6lr61','/images/products/6lr61.png'],['6F22','6f22','/images/catalog/model-6F22.jpg']
] } ];
