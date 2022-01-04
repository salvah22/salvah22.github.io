import{$ as w,S as N,F as v,a as T,C as F,V as I,t as B,T as j,O as D,b as K,c as W,I as g,d as y,M as $,e as Q,f as U,g as X,h as J,i as b,D as Z,P as S,L as C,u as ee,j as z,k as te,l as ne}from"./vendor.df98d922.js";const re=function(){const r=document.createElement("link").relList;if(r&&r.supports&&r.supports("modulepreload"))return;for(const a of document.querySelectorAll('link[rel="modulepreload"]'))o(a);new MutationObserver(a=>{for(const e of a)if(e.type==="childList")for(const l of e.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&o(l)}).observe(document,{childList:!0,subtree:!0});function t(a){const e={};return a.integrity&&(e.integrity=a.integrity),a.referrerpolicy&&(e.referrerPolicy=a.referrerpolicy),a.crossorigin==="use-credentials"?e.credentials="include":a.crossorigin==="anonymous"?e.credentials="omit":e.credentials="same-origin",e}function o(a){if(a.ep)return;a.ep=!0;const e=t(a);fetch(a.href,e)}};re();window.$=w;window.jQuery=w;var p=0,oe=new N({fill:new v({color:"rgba(255, 255, 255, 0.2)"}),stroke:new T({color:"#C800FF",width:2}),image:new F({radius:7,fill:new v({color:"#C800FF"})})}),O=new I({center:B([13.199195,55.70331],"EPSG:4326","EPSG:3857"),zoom:13});class ae extends b{constructor(r){const t=r||{},o=document.createElement("button");o.innerHTML="M";var a=t.buttonTipLabel?t.buttonTipLabel:"Open Measuring Tool";o.title=a;const e=document.createElement("div");e.className="measure ol-unselectable ol-control",e.appendChild(o);super({element:e,target:t.target});o.addEventListener("click",this.enableMeasuring.bind(this),!1)}enableMeasuring(){p==0?(alert("Measuring Tool Enabled"),p=1,i.on("pointermove",G),ge(),i.getViewport().addEventListener("mouseout",A)):(alert("measuring tool disabled"),p=0,i.un("pointermove",G),i.removeInteraction(m),i.getViewport().removeEventListener("mouseout",A),i.removeOverlay(h))}}class ie extends b{constructor(r){const t=r||{},o=document.createElement("button");o.innerHTML="C";var a=t.buttonTipLabel?t.buttonTipLabel:"Clear Map";o.title=a;const e=document.createElement("div");e.className="clear ol-unselectable ol-control",e.appendChild(o);super({element:e,target:t.target});o.addEventListener("click",this.clearAll.bind(this),!1)}clearAll(){location.reload()}}class le extends b{constructor(r){const t=r||{},o=document.createElement("button");o.innerHTML="i";var a=t.buttonTipLabel?t.buttonTipLabel:"More Information";o.title=a;const e=document.createElement("div");e.className="more ol-unselectable ol-control",e.appendChild(o);super({element:e,target:t.target});o.addEventListener("click",this.showMore.bind(this),!1)}showMore(){document.getElementById("moreinfo").style.display="block"}}function A(){c.classList.add("hidden")}const se=new j({source:new D}),x=new K,ce=new W({source:x,style:oe});var R={},P=1;R["v"+P]=ce;let f,c,h,u,L;const ue="Click to continue drawing the polygon",de="Click to continue drawing the line",G=function(n){if(n.dragging)return;let r="Click to start drawing";if(f){const t=f.getGeometry();t instanceof S?r=ue:t instanceof C&&(r=de)}c.innerHTML=r,h.setPosition(n.coordinate),c.classList.remove("hidden")};var _=new g({url:"https://geoserver.gis.lu.se/geoserver/wms",params:{LAYERS:"salvazin_dummy_data",TILED:!0},serverType:"geoserver"}),me=new y({source:_}),d={},s=1;d["salvazin"+s]=me;var M={},E=1;function k(n="none"){var r=new g({url:"https://geoserver.gis.lu.se/geoserver/wms",params:{LAYERS:"salvazin_dummy_data",TILED:!0,FILTER:"(<Filter><And><PropertyIsEqualTo><PropertyName>name</PropertyName><Literal>"+n+"</Literal></PropertyIsEqualTo></And></Filter>)",STYLES:"salvazin_selection"},serverType:"geoserver"}),t=new y({source:r});i.removeLayer(M["selection"+E]),E+=1,M["selection"+E]=t,i.addLayer(M["selection"+E])}const i=new $({controls:Q().extend([new U({units:"metric",bar:!0,steps:4,text:!1,minWidth:140}),new X({coordinateFormat:J(4),projection:"EPSG:4326",target:document.getElementById("mouse-position")}),new ae,new ie,new le]),layers:[se,R["v"+P],d["salvazin"+s]],target:"map",view:O});k();const q=document.getElementById("type");let m;const fe=function(n){const r=te(n);let t;return r>100?t=Math.round(r/1e3*100)/100+" km":t=Math.round(r*100)/100+" m",t},ve=function(n){const r=ne(n);let t;return r>1e4?t=Math.round(r/1e6*100)/100+" km<sup>2</sup>":t=Math.round(r*100)/100+" m<sup>2</sup>",t};function ge(){const n=q.value=="area"?"Polygon":"LineString";m=new Z({source:x,type:n,style:new N({fill:new v({color:"rgba(255, 255, 255, 0.2)"}),stroke:new T({color:"rgba(0, 0, 0, 0.5)",lineDash:[10,10],width:2}),image:new F({radius:5,stroke:new T({color:"rgba(0, 0, 0, 0.7)"}),fill:new v({color:"rgba(255, 255, 255, 0.2)"})})})}),i.addInteraction(m),H(),ye();let r;m.on("drawstart",function(t){f=t.feature;let o=t.coordinate;r=f.getGeometry().on("change",function(a){const e=a.target;let l;e instanceof S?(l=ve(e),o=e.getInteriorPoint().getCoordinates()):e instanceof C&&(l=fe(e),o=e.getLastCoordinate()),u.innerHTML=l,L.setPosition(o)})}),m.on("drawend",function(){u.className="ol-tooltip ol-tooltip-static",L.setOffset([0,-7]),f=null,u=null,H(),ee(r)})}function ye(){c&&c.parentNode.removeChild(c),c=document.createElement("div"),c.className="ol-tooltip hidden",h=new z({element:c,offset:[15,0],positioning:"center-left"}),i.addOverlay(h)}function H(){u&&u.parentNode.removeChild(u),u=document.createElement("div"),u.className="ol-tooltip ol-tooltip-measure v"+P,L=new z({element:u,offset:[0,-15],positioning:"bottom-center",stopEvent:!1,insertFirst:!1}),i.addOverlay(L)}function pe(){i.removeInteraction(m)}i.on("singleclick",function(n){if(p==0){var r=O.getResolution(),t=_.getFeatureInfoUrl(n.coordinate,r,"EPSG:3857",{INFO_FORMAT:"application/json"});w.get(t,function(o){var a=o.features;if(a.length>0){var e=a[0].properties;he(e)}})}});function he(n){var r=document.getElementById("infoContent"),t="",o="",a="";for(var e in n)if(!!n.hasOwnProperty(e)&&(e=="name"&&(k(n[e]),t+="<h1>"+n[e]+"</h1>"),e=="type"&&(t+="<span>"+n[e]+", <b>SEK "+a+"</b></span><p><img src='img/"+n[e]+".png' width='216'></p><p><i>"),e=="rent"&&(a=Math.round(n[e])),e=="rank"&&(o+=e+": "+n[e].toFixed(4)+"</i></p>"),e=="bbox"))var l=n[e],V=l[0],Y=l[1];r.innerHTML=t+o,be(V,Y,0)}function Le(){var n=document.getElementById("infoToggle"),r=n.checked,t="";r?t="block":t="none",document.getElementById("info").style.display=t}function Ee(){var n=document.getElementById("filtersToggle"),r=n.checked,t="";r?t="block":t="none",document.getElementById("filters").style.display=t}function we(){i.removeLayer(d["salvazin"+s]);var n="";document.filtersForm.rentMax.value!=""&&(n+="<PropertyIsLessThan><PropertyName>rent</PropertyName><Literal>"+document.filtersForm.rentMax.value+"</Literal></PropertyIsLessThan>"),document.filtersForm.rentMin.value!=""&&(n+="<PropertyIsGreaterThan><PropertyName>rent</PropertyName><Literal>"+document.filtersForm.rentMin.value+"</Literal></PropertyIsGreaterThan>"),document.filtersForm.userRank.value!=""&&(n+="<PropertyIsLessThan><PropertyName>rank</PropertyName><Literal>"+document.filtersForm.userRank.value+"</Literal></PropertyIsLessThan>");var r=document.getElementById("trailer").checked,t=document.getElementById("house").checked,o=document.getElementById("apartment").checked;r||(n+="<PropertyIsNotEqualTo><PropertyName>type</PropertyName><Literal>trailer</Literal></PropertyIsNotEqualTo>"),t||(n+="<PropertyIsNotEqualTo><PropertyName>type</PropertyName><Literal>house</Literal></PropertyIsNotEqualTo>"),o||(n+="<PropertyIsNotEqualTo><PropertyName>type</PropertyName><Literal>apartment</Literal></PropertyIsNotEqualTo>");var a=new g({url:"https://geoserver.gis.lu.se/geoserver/wms",params:{LAYERS:"salvazin_dummy_data",FILTER:"(<Filter><And>"+n+"</And></Filter>)()"},serverType:"geoserver"}),e=new y({source:a});s+=1,d["salvazin"+s]=e,i.addLayer(d["salvazin"+s]),k(document.getElementById("infoContent").innerHTML.split("h1")[1].slice(1).split("<")[0])}function Te(){document.getElementById("trailer").checked=!0,document.getElementById("house").checked=!0,document.getElementById("apartment").checked=!0,document.filtersForm.rentMax.value="",document.filtersForm.rentMin.value="",document.filtersForm.userRank.value="",i.removeLayer(d["salvazin"+s]);var n=new g({url:"https://geoserver.gis.lu.se/geoserver/wms",params:{LAYERS:"salvazin_dummy_data"},serverType:"geoserver"}),r=new y({source:n});s+=1,d["salvazin"+s]=r,i.addLayer(d["salvazin"+s])}function Ie(){document.getElementById("moreinfo").style.display="none"}function be(n=13.199195,r=55.70331,t=1){if(t==1)var o=new I({center:B([n,r],"EPSG:4326","EPSG:3857"),zoom:14});else if(t==0)var o=new I({center:[n,r],zoom:14});i.setView(o)}q.addEventListener("change",pe);document.getElementById("nav").addEventListener("click",Ie);document.getElementById("infoToggle").addEventListener("click",Le);document.getElementById("filtersToggle").addEventListener("click",Ee);document.getElementById("clear").addEventListener("click",Te);document.getElementById("filtersForm").addEventListener("change",we);
//# sourceMappingURL=index.623db17f.js.map
