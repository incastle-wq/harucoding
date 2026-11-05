const V='hc-dev';
const CORE=['./','index.html','base.css','app.css','app.js','course.js','py-worker.js','js-worker.js','manifest.webmanifest','fonts/PretendardVariable.woff2','cm/codemirror.js','cm/codemirror.css','cm/mode/python.js','cm/mode/javascript.js','cm/mode/xml.js','cm/mode/css.js','cm/mode/htmlmixed.js','cm/runmode.js','cm/closebrackets.js','cm/matchbrackets.js','icons/icon-192.png','icons/icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith('hc-')&&k!==V&&k!=='hc-py').map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);if(u.origin!==location.origin)return;
  if(u.pathname.includes('/pyodide/')){e.respondWith(caches.open('hc-py').then(c=>c.match(r).then(hit=>hit||fetch(r).then(res=>{if(res.ok)c.put(r,res.clone());return res}))));return}
  if(r.mode==='navigate'){e.respondWith(fetch(r).then(res=>{const cp=res.clone();caches.open(V).then(c=>c.put('index.html',cp));return res}).catch(()=>caches.match('index.html')));return}
  e.respondWith(caches.match(r).then(hit=>{const net=fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(V).then(c=>c.put(r,cp))}return res}).catch(()=>hit);return hit||net}))});
