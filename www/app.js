(function(){
"use strict";
const APP_VER="__VER__";
const $=s=>document.querySelector(s);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const shuffle=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.random()*(i+1)|0;[a[i],a[j]]=[a[j],a[i]]}return a};
const pick=a=>a[Math.random()*a.length|0];
const MIN=6e4,DAY=864e5,IV=[0,10*MIN,DAY,3*DAY,7*DAY,16*DAY,35*DAY,90*DAY];
const now=()=>Date.now();
const dkey=d=>{d=d||new Date();return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate()};
const lsGet=k=>{try{return localStorage.getItem(k)}catch(e){return null}};
const lsSet=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}};
const RM=(()=>{try{return matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){return false}})();
const CAP=!!(window.Capacitor&&window.Capacitor.isNativePlatform&&window.Capacitor.isNativePlatform());
const plug=n=>CAP?((window.Capacitor.Plugins&&window.Capacitor.Plugins[n])||(window.Capacitor.registerPlugin&&window.Capacitor.registerPlugin(n))||null):null;
const ICON={gear:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" width="20" height="20"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/></svg>',
  play:'<svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M7 5v14l11-7z"/></svg>'};

/* ---------- 데이터 ---------- */
const CS=window.COURSES||[];const CM={},UM={},QM={},ALLQ=[];
CS.forEach(c=>{CM[c.id]=c;c.units.forEach((u,ui)=>{u.c=c;u.ui=ui;u.lang=u.lang||c.lang;UM[u.id]=u;u.q.forEach((q,i)=>{q.id=u.id+':'+i;q.u=u;QM[q.id]=q;ALLQ.push(q)})})});
const PYMSG=CAP?'파이썬 준비 중… 처음 한 번은 인터넷에서 약 10MB를 받아요':'파이썬 준비 중… (처음 한 번 몇 초 걸려요)';
const MODE={python:'python',javascript:'javascript',html:'htmlmixed'};
const LANGNAME={python:'Python',javascript:'JavaScript',html:'HTML'};

/* ---------- 저장 ---------- */
const KEY='haru-coding-v1';
const DEF_SET={len:8,goal:50,fs:15,fast:true,sfx:true,intro:true};
function normS(x){x=x&&typeof x==='object'?x:{};return {q:x.q&&typeof x.q==='object'?x.q:{},xp:+x.xp||0,streak:x.streak&&x.streak.last!=null?x.streak:{last:'',n:0},today:x.today||{d:'',xp:0},days:x.days||{},badges:x.badges||{},stat:Object.assign({lessons:0,perfect:0,bestCombo:0,runs:0,bugs:0,maxStreak:0},x.stat||{}),set:Object.assign({},DEF_SET,x.set||{}),ui:x.ui&&typeof x.ui==='object'?x.ui:{},code:x.code||{}}}
let S;try{S=normS(JSON.parse(lsGet(KEY)))}catch(e){S=normS(null)}
const save=()=>lsSet(KEY,JSON.stringify(S));
const st=id=>S.q[id];
const isLearned=id=>{const s=st(id);return !!s&&s.b>=2};
const isDue=(id,t)=>{const s=st(id);return !!s&&s.due<=t};
function grade(q,ok,o){o=o||{};let s=S.q[q.id];const first=!s;if(!s)s=S.q[q.id]={b:0,due:0,n:0,w:0};s.n++;s.last=now();let nb=s.b;
  if(ok){if(first)nb=o.hard?3:2;else if(s.due<=now())nb=Math.min(7,s.b+1);}else{s.w++;nb=s.b>=4?2:1;}
  if(nb!==s.b||!ok||first){s.b=nb;s.due=now()+IV[nb];}}
function todayXP(){return S.today.d===dkey()?S.today.xp:0}
function streakN(){const y=new Date(now()-DAY);return (S.streak.last===dkey()||S.streak.last===dkey(y))?S.streak.n:0}
function addXP(x){if(!x)return;const d=dkey();if(S.today.d!==d)S.today={d,xp:0};S.today.xp+=x;S.xp+=x;S.days[d]=(S.days[d]||0)+x;
  if(S.streak.last!==d){S.streak={last:d,n:S.streak.last===dkey(new Date(now()-DAY))?S.streak.n+1:1};}S.stat.maxStreak=Math.max(S.stat.maxStreak,S.streak.n);}
const uLearned=u=>u.q.filter(q=>isLearned(q.id)).length;
const uDue=(u,t)=>u.q.filter(q=>isDue(q.id,t)).length;
const cPct=c=>{let a=0,b=0;c.units.forEach(u=>{a+=uLearned(u);b+=u.q.length});return b?a/b:0};

/* ---------- 마스코트 버기 · 소리 · 폭죽 · 급수 · 업적 ---------- */
function mascot(mood,size){size=size||64;const W='#FFFFFF',K='#1F2A44';
  const eyes={idle:`<circle cx="43" cy="33" r="6.5" fill="${W}"/><circle cx="57" cy="33" r="6.5" fill="${W}"/><circle cx="44" cy="34" r="3.2" fill="${K}"/><circle cx="58" cy="34" r="3.2" fill="${K}"/><circle cx="45" cy="32.6" r="1" fill="${W}"/><circle cx="59" cy="32.6" r="1" fill="${W}"/>`,
    happy:`<path d="M38 35q5-6 10 0M52 35q5-6 10 0" stroke="${W}" stroke-width="3.2" fill="none" stroke-linecap="round"/>`,
    cheer:`<path d="M38 35q5-7 10 0M52 35q5-7 10 0" stroke="${W}" stroke-width="3.4" fill="none" stroke-linecap="round"/>`,
    oops:`<path d="M39 29l7 7M46 29l-7 7M54 29l7 7M61 29l-7 7" stroke="${W}" stroke-width="3" stroke-linecap="round"/>`,
    sleep:`<path d="M38 34q5 3 10 0M52 34q5 3 10 0" stroke="${W}" stroke-width="3" fill="none" stroke-linecap="round"/>`}[mood]||'';
  const mouth={idle:`<path d="M46 42q4 3 8 0" stroke="#FCA5A5" stroke-width="2.4" fill="none" stroke-linecap="round"/>`,happy:`<path d="M44 41q6 7 12 0z" fill="#F87171"/>`,cheer:`<ellipse cx="50" cy="43" rx="5.5" ry="4.5" fill="#F87171"/>`,oops:`<path d="M44 44q3-3 6 0t6 0" stroke="#FCA5A5" stroke-width="2.4" fill="none" stroke-linecap="round"/>`,sleep:`<path d="M47 43h6" stroke="#FCA5A5" stroke-width="2.4" stroke-linecap="round"/>`}[mood]||'';
  const extra=mood==='cheer'?`<g fill="#FFC93C"><path d="M10 22l2 5 5 2-5 2-2 5-2-5-5-2 5-2z"/><path d="M88 16l1.5 4 4 1.5-4 1.5-1.5 4-1.5-4-4-1.5 4-1.5z"/></g>`:mood==='sleep'?`<text x="80" y="20" font-size="13" font-weight="900" fill="#94A3B8" font-family="sans-serif">z</text>`:'';
  return `<svg class="mascot m-${mood}" width="${size}" height="${size}" viewBox="0 0 100 100" aria-hidden="true"><ellipse cx="50" cy="95" rx="26" ry="3.5" fill="rgba(0,0,0,.14)"/><g class="m-body"><g stroke="${K}" stroke-width="3.2" stroke-linecap="round"><path d="M24 62l-10-4M24 72l-11 3M26 82l-8 7M76 62l10-4M76 72l11 3M74 82l8 7"/></g><ellipse cx="50" cy="68" rx="28" ry="24" fill="#22B07D"/><path d="M50 46v45" stroke="#168A60" stroke-width="2.6"/><circle cx="38" cy="66" r="4" fill="#1A9A6C"/><circle cx="62" cy="74" r="4.5" fill="#1A9A6C"/><circle cx="40" cy="80" r="3" fill="#1A9A6C"/><path d="M40 20Q34 6 26 8M60 20Q66 6 74 8" stroke="${K}" stroke-width="3" fill="none" stroke-linecap="round"/><circle cx="25" cy="8" r="4.2" fill="#FFC93C"/><circle cx="75" cy="8" r="4.2" fill="#FFC93C"/><circle cx="50" cy="36" r="19" fill="${K}"/>${eyes}${mouth}<ellipse cx="38" cy="42" rx="3.4" ry="2" fill="#F472B6" opacity=".6"/><ellipse cx="62" cy="42" rx="3.4" ry="2" fill="#F472B6" opacity=".6"/></g>${extra}</svg>`;}
let AC=null;
function ac(){if(!AC){try{AC=new (window.AudioContext||window.webkitAudioContext)()}catch(e){AC=null}}if(AC&&AC.state==='suspended'){try{AC.resume()}catch(e){}}return AC}
function tone(f,t0,d,type,g){const a=ac();if(!a)return;const o=a.createOscillator(),v=a.createGain();o.type=type||'sine';o.frequency.value=f;const t=a.currentTime+t0;v.gain.setValueAtTime(.0001,t);v.gain.linearRampToValueAtTime(g||.12,t+.012);v.gain.exponentialRampToValueAtTime(.0001,t+d);o.connect(v);v.connect(a.destination);o.start(t);o.stop(t+d+.05)}
const SFX={ok:()=>{tone(880,0,.14,'triangle');tone(1318.5,.09,.26,'triangle')},ng:()=>{tone(233,0,.16,'square',.05);tone(174.6,.11,.26,'square',.05)},done:()=>{[523.25,659.25,783.99,1046.5].forEach((f,i)=>tone(f,i*.11,.32,'triangle'))},badge:()=>{[783.99,987.77,1174.66,1567.98].forEach((f,i)=>tone(f,i*.08,.28,'sine',.1))},combo:()=>{tone(1046.5,0,.1,'triangle',.08);tone(1568,.07,.16,'triangle',.08)},run:()=>tone(660,0,.06,'sine',.05)};
function sfx(k){if(S.set.sfx)try{SFX[k]()}catch(e){}}
function confetti(){if(RM)return;const c=document.createElement('canvas');c.className='confetti';document.body.appendChild(c);const dpr=window.devicePixelRatio||1,W=innerWidth,H=innerHeight;c.width=W*dpr;c.height=H*dpr;const x=c.getContext('2d');x.scale(dpr,dpr);
  const cols=['#4338CA','#22B07D','#FFC93C','#2F6EA8','#D9481F','#F472B6'];const P=Array.from({length:120},()=>({x:W/2+(Math.random()-.5)*120,y:H*.32,vx:(Math.random()-.5)*10,vy:-Math.random()*11-4,r:Math.random()*6+5,c:pick(cols),a:Math.random()*6,va:(Math.random()-.5)*.35}));
  const t0=performance.now();let last=t0;(function f(t){const dt=Math.min(40,t-last)/16;last=t;x.clearRect(0,0,W,H);for(const p of P){p.vy+=.33*dt;p.vx*=.992;p.x+=p.vx*dt;p.y+=p.vy*dt;p.a+=p.va*dt;x.save();x.translate(p.x,p.y);x.rotate(p.a);x.fillStyle=p.c;x.fillRect(-p.r/2,-p.r/4,p.r,p.r/2);x.restore();}if(t-t0<2400)requestAnimationFrame(f);else c.remove();})(t0);}
const RANKN=['Hello World','변수 수집가','조건 탐험가','반복 장인','리스트 정리왕','함수 설계자','버그 사냥꾼','코드 리뷰어','풀스택 견습생','시니어 개발자'];
const cumXP=n=>20*(n-1)*n;
function levelOf(xp){let L=1;while(L<20&&xp>=cumXP(L+1))L++;return L}
const rankOf=L=>RANKN[Math.floor((L-1)/2)]+(L%2?' I':' II');
function levelInfo(xp){const L=levelOf(xp),a=cumXP(L),b=L<20?cumXP(L+1):a;return {L,rank:rankOf(L),pct:L<20?(xp-a)/(b-a)*100:100,left:b-xp}}
const cDone=id=>CM[id].units.every(u=>uLearned(u)===u.q.length);
const BADGES=[
 ['first','1st','첫 레슨','레슨을 처음으로 끝냈어요',s=>s.stat.lessons>=1],
 ['run1','▶','첫 실행','코드를 처음 실행했어요',s=>s.stat.runs>=1],
 ['perfect','100','만점','레슨을 하나도 안 틀리고 끝냈어요',s=>s.stat.perfect>=1],
 ['combo10','x10','10연속','10문제를 연속으로 맞혔어요',s=>s.stat.bestCombo>=10],
 ['bug10','fix','디버거','틀린 줄 찾기를 10번 맞혔어요',s=>s.stat.bugs>=10],
 ['run50','50','실행 50번','코드를 50번 실행해 봤어요',s=>s.stat.runs>=50],
 ['s3','3d','3일 연속','3일 연속으로 공부했어요',s=>s.stat.maxStreak>=3],
 ['s7','7d','7일 연속','7일 연속으로 공부했어요',s=>s.stat.maxStreak>=7],
 ['s30','30d','30일 연속','30일 연속으로 공부했어요',s=>s.stat.maxStreak>=30],
 ['goal7','★','목표 7번','하루 목표를 7일 채웠어요',s=>Object.values(s.days).filter(v=>v>=s.set.goal).length>=7],
 ['py','Py','Python 수료','Python 단원을 모두 익혔어요',()=>cDone('py')],
 ['ht','</>','HTML·CSS 수료','HTML·CSS 단원을 모두 익혔어요',()=>cDone('ht')],
 ['js','JS','JavaScript 수료','JavaScript 단원을 모두 익혔어요',()=>cDone('js')]];
function checkBadges(){const got=[];for(const b of BADGES){if(S.badges[b[0]])continue;let ok=false;try{ok=b[4](S)}catch(e){}if(ok){S.badges[b[0]]=now();got.push(b)}}if(got.length)save();return got}
function badgeToast(got){if(!got.length)return;sfx('badge');toast('업적 달성: '+got.map(b=>b[2]).join(', '))}
const bdgHtml=(b,lock)=>`<button class="bdg ${lock?'lock':''}" data-bdg="${b[0]}" aria-label="${esc(b[2])}: ${esc(b[3])}"><b style="font-family:var(--mono);font-size:.95rem">${esc(b[1])}</b>${esc(b[2])}</button>`;

/* ---------- 코드 표시 ---------- */
function hl(code,lang){const el=document.createElement('div');try{CodeMirror.runMode(code,MODE[lang]||lang,el)}catch(e){el.textContent=code}return el.innerHTML}
function codeBlock(code,lang,opt){opt=opt||{};const lines=String(code).split('\n');
  return `<div class="code" ${opt.id?`id="${opt.id}"`:''}>${lines.map((l,i)=>{let inner=hl(l,lang);if(opt.slot&&l.includes('▢'))inner=hl(l.split('▢')[0],lang)+`<span class="slot" id="slot">${opt.slotText?esc(opt.slotText):'&nbsp;'}</span>`+hl(l.split('▢').slice(1).join('▢'),lang);
    return `<div class="ln ${opt.pick?'pick':''}" data-ln="${i}"><b>${i+1}</b><span class="t">${inner||' '}</span></div>`}).join('')}</div>`}

/* ---------- 실행기 ---------- */
const RUN={py:null,pyBoot:null,js:null,cbs:{},seq:0};
function mkWorker(file){const w=new Worker(file);w.onmessage=e=>{const cb=RUN.cbs[e.data.id];if(cb){delete RUN.cbs[e.data.id];cb(e.data)}};w.onerror=()=>{};return w}
function call(w,msg){return new Promise(res=>{const id=++RUN.seq;RUN.cbs[id]=res;w.postMessage(Object.assign({id},msg))})}
function warmPy(){if(!RUN.py)RUN.py=mkWorker('py-worker.js');if(!RUN.pyBoot)RUN.pyBoot=call(RUN.py,{warm:true}).then(r=>{if(!r.ok){RUN.pyBoot=null}return r});return RUN.pyBoot}
function withTimeout(p,ms,onTO){let t;return Promise.race([p,new Promise(res=>{t=setTimeout(()=>{onTO();res({ok:false,out:'',err:'TIMEOUT'})},ms)})]).finally(()=>clearTimeout(t))}
async function runPy(code,stdin){const w=await warmPy();if(w&&!w.ok)return {ok:false,out:'',err:'파이썬을 불러오지 못했어요. '+(CAP?'처음 한 번은 인터넷 연결이 필요해요. ':'')+(w.err||'')};
  return withTimeout(call(RUN.py,{code,stdin}),6000,()=>{try{RUN.py.terminate()}catch(e){}RUN.py=null;RUN.pyBoot=null;setTimeout(warmPy,300)})}
async function runJs(code){if(!RUN.js)RUN.js=mkWorker('js-worker.js');return withTimeout(call(RUN.js,{code}),3000,()=>{try{RUN.js.terminate()}catch(e){}RUN.js=null})}
function htmlDoc(code){const hook=`<script>(function(){var send=function(t,a){try{parent.postMessage({hc:1,t:t,m:[].map.call(a,function(x){return typeof x==='object'?JSON.stringify(x):String(x)}).join(' ')},'*')}catch(e){}};console.log=function(){send('log',arguments)};window.onerror=function(m){send('err',[m])};window.alert=function(m){send('log',['[알림] '+m])}})();<\/script><style>body{font-family:'Pretendard Variable',system-ui,sans-serif;margin:12px;color:#191F28;background:#fff}</style>`;
  return /<head[^>]*>/i.test(code)?code.replace(/<head[^>]*>/i,m=>m+hook):hook+code}
function renderHtml(frame,code){return new Promise(res=>{let done=false;const fin=()=>{if(!done){done=true;setTimeout(res,180)}};frame.onload=fin;frame.srcdoc=htmlDoc(code);setTimeout(fin,1500)})}
addEventListener('message',e=>{const d=e.data;if(!d||!d.hc)return;const c=document.querySelector('.console[data-html]');if(!c)return;if(c.dataset.fresh){c.textContent='';delete c.dataset.fresh}c.insertAdjacentHTML('beforeend',`<span class="${d.t==='err'?'err':''}">${esc(d.m)}</span>\n`)});
const norm=s=>String(s||'').replace(/\r/g,'').split('\n').map(l=>l.replace(/\s+$/,'')).join('\n').replace(/\n+$/,'').replace(/^\n+/,'');
const ERRKO={NameError:'정의되지 않은 이름을 썼어요. 변수 이름 오타나 문자열 따옴표 빠짐을 확인해 보세요.',SyntaxError:'문법이 틀렸어요. 괄호·따옴표·콜론(:)의 짝을 확인해 보세요.',IndentationError:'들여쓰기가 맞지 않아요. if·for·def 아래 줄은 4칸 들여 써요.',TabError:'탭과 띄어쓰기를 섞어 썼어요. 띄어쓰기 4칸으로 맞춰요.',TypeError:'자료형이 맞지 않아요. 문자열과 숫자를 + 하지 않았는지, const에 다시 넣지 않았는지 확인해 보세요.',ZeroDivisionError:'0으로 나눌 수 없어요.',IndexError:'리스트 번호가 범위를 벗어났어요. 번호는 0부터예요.',ValueError:'값을 바꿀 수 없어요. 숫자가 아닌 글자를 int()로 바꾸려 했는지 확인해 보세요.',EOFError:'input()이 읽을 입력값이 없어요. 입력값 칸을 채워 주세요.',KeyError:'딕셔너리에 없는 키예요.',AttributeError:'그 값에는 그런 기능(메서드)이 없어요. 철자를 확인해 보세요.',ReferenceError:'정의되지 않은 이름을 썼어요. 변수 이름 오타나 따옴표 빠짐을 확인해 보세요.',RangeError:'값이 허용 범위를 벗어났어요.'};
function explain(lang,err){if(!err)return null;if(err==='TIMEOUT')return {msg:'시간 초과',hint:'실행이 끝나지 않아 멈췄어요. 끝나지 않는 반복(무한 루프)이 있는지 확인해 보세요.'};
  let line=null,msg=String(err).trim();
  if(lang==='python'){const ls=msg.split('\n');const m=[...msg.matchAll(/File "<exec>", line (\d+)/g)].pop();if(m)line=+m[1];msg=ls.filter(Boolean).pop()||msg;}
  const name=(msg.match(/^(\w+Error)/)||[])[1];let hint=name&&ERRKO[name]||'';if(/constant variable/.test(msg))hint='const로 만든 변수에는 다시 값을 넣을 수 없어요. let을 쓰세요.';
  return {line,msg,hint}}
function consoleHtml(r,lang){if(!r)return '';const x=r.ok?null:explain(lang,r.err);
  return `<span class="lab">실행 결과</span>${esc(r.out||'')}${!r.ok?`<span class="err">${x&&x.line?`${x.line}번째 줄 · `:''}${esc(x?x.msg:r.err)}</span>${x&&x.hint?`<span class="hint">${esc(x.hint)}</span>`:''}`:(r.out?'':'<span style="color:var(--code-muted)">(출력 없음)</span>')}`}

/* ---------- 편집기 ---------- */
const KEYS={python:['⇥','(',')','"',':','=','[',']','+','-','*','/','%','<','>','#','_','.',',',"'"],javascript:['⇥','(',')','{','}','"',';','=','[',']','+','-','*','/','<','>','`','$','.',',',"'",'!','&','|'],html:['⇥','<','>','/','"','=','{','}',':',';','#','.','-','(',')',"'"]};
const PAIR={'(':')','[':']','{':'}','"':'"',"'":"'",'`':'`'};
function makeEditor(host,lang,value){host.innerHTML=`<div class="editor"><div class="ed"></div><div class="keys">${(KEYS[lang]||[]).map(k=>`<button type="button" data-k="${esc(k)}">${esc(k)}</button>`).join('')}</div></div>`;
  const cm=CodeMirror(host.querySelector('.ed'),{value:value||'',mode:MODE[lang],lineNumbers:true,indentUnit:lang==='python'?4:2,tabSize:lang==='python'?4:2,indentWithTabs:false,smartIndent:true,matchBrackets:true,autoCloseBrackets:true,inputStyle:'contenteditable',spellcheck:false,autocorrect:false,autocapitalize:false,lineWrapping:false,
    extraKeys:{Tab:c=>c.execCommand(c.somethingSelected()?'indentMore':'insertSoftTab'),'Shift-Tab':'indentLess'}});
  cm.getWrapperElement().style.fontSize=S.set.fs+'px';
  host.querySelector('.keys').addEventListener('click',e=>{const b=e.target.closest('[data-k]');if(!b)return;const k=b.dataset.k;
    if(k==='⇥')cm.execCommand('insertSoftTab');else if(PAIR[k]&&!cm.somethingSelected()){cm.replaceSelection(k+PAIR[k]);const p=cm.getCursor();cm.setCursor({line:p.line,ch:p.ch-1})}else cm.replaceSelection(k);cm.focus()});
  setTimeout(()=>cm.refresh(),30);return cm}

/* ---------- 레슨 ---------- */
let L=null;
const qv=$('#qv'),footIn=$('#footIn'),lFoot=$('#lFoot');
function pickQs(u,mode){const len=S.set.len,t=now();let pool;
  if(mode==='review'){pool=ALLQ.filter(q=>isDue(q.id,t)).sort((a,b)=>st(b.id).w-st(a.id).w||st(a.id).due-st(b.id).due);return pool.slice(0,len)}
  const due=u.q.filter(q=>isDue(q.id,t)),fresh=u.q.filter(q=>!st(q.id));
  let items=due.slice(0,Math.ceil(len*.4)).concat(fresh).slice(0,len);
  if(items.length<len)items=items.concat(shuffle(u.q.filter(q=>!items.includes(q))).slice(0,len-items.length));
  const codes=items.filter(q=>q.k==='code'),rest=items.filter(q=>q.k!=='code');
  if(!codes.length){const c=u.q.find(q=>q.k==='code'&&!items.includes(q));if(c&&rest.length>3){rest.pop();codes.push(c)}}
  return rest.concat(codes.slice(0,2))}
function start(mode,uid){const u=uid?UM[uid]:null;const qs=pickQs(u,mode);if(!qs.length){toast('지금 복습할 문제가 없어요');return}
  if(u){S.ui.cur=u.id;save();}closeUSheet(true);
  L={mode,u,qs:qs.map(q=>({q,retry:false})),i:0,ok:0,tot:0,xp:0,combo:0,best:0,t0:now(),miss:[],state:'ask',tok:0};
  if(qs.some(q=>q.u.lang==='python'))warmPy();
  $('#lesson').hidden=false;document.body.style.overflow='hidden';renderQ();}
function setBar(){$('#lBar').style.width=(L.i/L.qs.length*100)+'%';$('#combo').textContent=L.combo>=3?L.combo+'연속':''}
function head(title,it){const q=it.q;return `<div class="q-head"><h2>${title}</h2>${it.retry?'<span class="tag retry">다시 한 번</span>':!st(q.id)?'<span class="tag new">새 문제</span>':''}<span class="lv" style="border-color:var(--g-${q.u.c.g});color:var(--g-${q.u.c.g})">${esc(q.u.c.name)}</span></div>`}
function optBtn(i,inner){return `<button class="btn opt" data-opt="${i}"><span class="n">${i+1}</span><span class="c">${inner}</span></button>`}
function renderQ(){const it=L.qs[L.i],q=it.q,lang=q.u.lang;L.state='ask';L.sel=null;L.tok++;L.tries=0;L.cm=null;setBar();lFoot.className='l-foot';let h='';
  if(q.k==='mc'||q.k==='out'){if(!it.ord)it.ord=shuffle(q.o.map((_,i)=>i));
    const title=q.k==='out'?(q.q||(lang==='html'?'화면에 어떻게 보일까요?':'실행하면 무엇이 출력될까요?')):q.q;
    h=head(esc(title),it)+(q.code?codeBlock(q.code,lang):'')+`<div class="opts">${it.ord.map((oi,i)=>optBtn(i,q.k==='out'||/[<>(){}=;"]/.test(q.o[oi])?`<pre>${esc(q.o[oi])}</pre>`:`<span>${esc(q.o[oi])}</span>`)).join('')}</div>`;}
  else if(q.k==='fill'){if(!it.ord)it.ord=shuffle(q.o.map((_,i)=>i));h=head(esc(q.q),it)+codeBlock(q.code,lang,{slot:true})+`<p class="q-code-help">빈칸에 들어갈 코드를 고르세요</p><div class="tiles">${it.ord.map((oi,i)=>`<button class="btn tile mono" data-opt="${i}">${esc(q.o[oi])}</button>`).join('')}</div>`;}
  else if(q.k==='order'){if(!it.ord)it.ord=shuffle(q.lines.map((_,i)=>i));L.built=[];h=head(esc(q.q),it)+`<div class="ans-box" id="ansBox"></div><div class="line-bank" id="lineBank">${it.ord.map((li,i)=>`<button class="btn lt" data-lt="${i}">${hl(q.lines[li],lang)}</button>`).join('')}</div>`;}
  else if(q.k==='bug'){h=head(esc(q.q||'틀린 곳이 있는 줄을 고르세요'),it)+codeBlock(q.code,lang,{pick:true,id:'bugCode'})+`<p class="q-code-help">줄을 눌러서 고르세요</p>`;}
  else if(q.k==='code'){h=head('직접 코딩',it)+`<p style="font-size:1.05rem;font-weight:700;line-height:1.5">${esc(q.q)}</p>${q.stdin?`<p class="need">입력값: ${q.stdin.map(esc).join(', ')} (input()에 차례로 들어가요)</p>`:''}${q.need?`<p class="need">꼭 써야 할 것: ${q.need.map(r=>`<code>${esc(needText(r))}</code>`).join(' ')}</p>`:''}<div id="edHost"></div><div class="run-row"><button class="btn" id="runBtn">${ICON.play}실행해 보기</button><span class="need">실행은 채점 없이 결과만 보여 줘요</span></div>${lang==='html'?`<iframe class="preview" id="pv" sandbox="allow-scripts allow-same-origin allow-modals" title="미리보기"></iframe>`:''}<div class="console" id="out" ${lang==='html'?'data-html hidden':''}><span class="lab">실행 결과</span><span style="color:var(--code-muted)">실행하면 여기에 결과가 나와요</span></div>`;}
  qv.innerHTML=h;$('#lBody').scrollTop=0;if(!RM){qv.classList.remove('q-in');void qv.offsetWidth;qv.classList.add('q-in');}
  if(q.k==='code'){L.cm=makeEditor($('#edHost'),lang,q.start||'');if(lang==='html'&&q.start)renderHtml($('#pv'),q.start);}
  renderFootAsk();}
function needText(r){return r.replace(/\\s[+*]/g,' ').replace(/\\/g,'').replace(/\|/g,' 또는 ').replace(/\s+/g,' ').trim()}
function renderFootAsk(){const it=L.qs[L.i],q=it.q;footIn.classList.remove('rise-up');
  const fast=S.set.fast&&(q.k==='mc'||q.k==='out'||q.k==='bug');
  footIn.innerHTML=`<div class="foot-row">${q.k==='code'&&L.tries>=1?`<button class="skip-t" id="giveUp">정답 보기</button>`:''}${fast?`<span class="muted" style="font-size:.8rem;margin-left:auto">누르면 바로 채점돼요</span>`:`<button class="btn primary" id="checkBtn" ${q.k==='code'?'':'disabled'}>${q.k==='code'?'제출하기':'확인'}</button>`}</div>`;}
function canCheck(){const q=L.qs[L.i].q;if(q.k==='order')return L.built.length===q.lines.length;if(q.k==='code')return true;return L.sel!==null}
function refreshCheck(){const b=$('#checkBtn');if(b)b.disabled=!canCheck()}
async function check(){if(L.state!=='ask'||!canCheck())return;const it=L.qs[L.i],q=it.q;let ok=false;
  if(q.k==='mc'||q.k==='out'){const oi=it.ord[L.sel];ok=oi===0;qv.querySelectorAll('[data-opt]').forEach((b,i)=>{b.classList.remove('sel');if(it.ord[i]===0)b.classList.add('right');else if(i===L.sel)b.classList.add('wrong')});}
  else if(q.k==='fill'){const oi=it.ord[L.sel];ok=oi===0;const sl=$('#slot');sl.textContent=q.o[0];sl.classList.add(ok?'ok':'ng');qv.querySelectorAll('[data-opt]').forEach((b,i)=>{if(it.ord[i]===0)b.classList.add('right');else if(i===L.sel)b.classList.add('wrong')});}
  else if(q.k==='order'){ok=L.built.map(i=>q.lines[it.ord[i]]).join('\n')===q.lines.join('\n');}
  else if(q.k==='bug'){ok=L.sel===q.a;qv.querySelectorAll('#bugCode .ln').forEach((r,i)=>{r.classList.remove('sel');if(i===q.a)r.classList.add('right');else if(i===L.sel)r.classList.add('wrong')});if(ok)S.stat.bugs++;}
  else if(q.k==='code'){const b=$('#checkBtn');if(b){b.disabled=true;b.textContent='채점 중…'}const r=await gradeCode(q,L.cm.getValue());if(!L||L.qs[L.i]!==it)return;
    if(!r.ok){L.tries++;sfx('ng');showCodeFail(r);renderFootAsk();return}ok=true;}
  finish(ok);}
async function execFor(q,code){const lang=q.u.lang,out=$('#out');S.stat.runs++;sfx('run');
  if(lang==='html'){out.hidden=false;out.dataset.fresh='1';out.innerHTML='<span class="lab">콘솔</span><span style="color:var(--code-muted)">(console.log 출력이 여기에 나와요)</span>';await renderHtml($('#pv'),code);return {ok:true}}
  out.classList.add('busy');out.innerHTML=lang==='python'&&!RUN.pyBoot?PYMSG:'실행 중…';
  if(lang==='python'&&RUN.pyBoot){const ready=await Promise.race([RUN.pyBoot.then(()=>1),new Promise(r=>setTimeout(()=>r(0),120))]);if(!ready)out.innerHTML=PYMSG;}
  const r=lang==='python'?await runPy(code,q.stdin||[]):await runJs(code);out.classList.remove('busy');out.innerHTML=consoleHtml(r,lang);return r}
async function gradeCode(q,code){if(!code.trim())return {ok:false,why:'코드를 먼저 써 주세요'};
  const r=await execFor(q,code);
  if(q.need)for(const re of q.need){if(!new RegExp(re).test(code))return {ok:false,why:`이번 문제는 ${needText(re)} 을(를) 써서 풀어야 해요`}}
  if(q.u.lang==='html'){const f=$('#pv');let ok=false;try{ok=!!new Function('doc','win','return ('+q.check+')')(f.contentDocument,f.contentWindow)}catch(e){}return ok?{ok:true}:{ok:false,why:'아직 조건을 다 맞추지 못했어요. 미리보기를 보며 고쳐 보세요'}}
  if(!r.ok)return {ok:false,why:'에러가 났어요. 아래 실행 결과의 설명을 확인해 보세요'};
  const got=norm(r.out);
  if(q.expect!=null&&got!==norm(q.expect))return {ok:false,why:'출력이 달라요',want:q.expect,got};
  if(q.contains&&!q.contains.every(c=>got.includes(c)))return {ok:false,why:`출력에 "${q.contains.join('", "')}" 이(가) 있어야 해요`};
  return {ok:true}}
function showCodeFail(r){lFoot.className='l-foot ng';footIn.innerHTML='';const box=document.createElement('div');box.className='fb-scroll';
  box.innerHTML=`<div class="fb">${mascot('oops',46)}<div class="body"><h3>${esc(r.why)}</h3>${r.want!=null?`<span class="hint">원하는 출력</span><pre class="console" style="margin:2px 0 4px">${esc(r.want)}</pre><span class="hint">내 출력</span><pre class="console" style="margin:2px 0">${esc(r.got||'(출력 없음)')}</pre>`:''}<span class="hint">고쳐서 다시 제출해 보세요.</span></div></div>`;
  footIn.appendChild(box);}
function finish(ok){const it=L.qs[L.i],q=it.q;L.state='done';L.tot++;
  if(ok){L.ok++;L.combo++;L.xp+=it.retry?5:(q.k==='code'?15:10);L.best=Math.max(L.best,L.combo);sfx([5,10,15,20].includes(L.combo)?'combo':'ok');if(L.combo>=3){const cb=$('#combo');cb.classList.remove('pop');void cb.offsetWidth;cb.classList.add('pop');}}else{L.combo=0;sfx('ng');}
  if(!it.retry){grade(q,ok,{hard:q.k==='code'||q.k==='order'});if(!ok){L.miss.push(q);L.qs.push({q,retry:true});}}
  save();setBar();renderFootResult(ok);}
function renderFootResult(ok){const it=L.qs[L.i],q=it.q,lang=q.u.lang;lFoot.className='l-foot '+(ok?'ok':'ng');
  let ans='';if(!ok){if(q.k==='mc'||q.k==='out'||q.k==='fill')ans=`<pre class="console" style="margin:4px 0">${esc(q.o[0])}</pre>`;else if(q.k==='order')ans=codeBlock(q.lines.join('\n'),lang);else if(q.k==='bug')ans=`<span class="ko">${q.a+1}번째 줄이에요</span>`;else if(q.k==='code')ans=`<span class="hint">정답 예시</span>`+codeBlock(q.sol,lang);}
  else if(q.k==='code'&&q.sol)ans=`<details class="bd"><summary>모범 답안 보기</summary>${codeBlock(q.sol,lang)}</details>`;
  const title=ok?pick(['정답!','좋아요!','완벽해요!','잘했어요!']):(q.k==='code'?'정답을 확인해 보세요':'아쉬워요, 정답은');
  footIn.innerHTML=`<div class="fb-scroll"><div class="fb">${mascot(ok?(L.combo>=5?'cheer':'happy'):'oops',50)}<div class="body"><h3>${title}</h3>${ans}${q.e?`<span class="nt">${esc(q.e)}</span>`:''}</div></div></div><div class="foot-row"><button class="btn ${ok?'ok':'ng'}" id="nextBtn">계속</button></div>`;
  if(!RM){footIn.classList.remove('rise-up');void footIn.offsetWidth;footIn.classList.add('rise-up');}
  $('#nextBtn').focus({preventScroll:true});}
function next(){if(!L)return;L.i++;if(L.i>=L.qs.length)return renderDone();renderQ();}
function renderDone(){const secs=Math.round((now()-L.t0)/1000);const acc=L.tot?Math.round(L.ok/L.tot*100):0;
  let bonus=L.tot&&L.ok===L.tot?10:0;L.xp+=bonus;const lv0=levelOf(S.xp);addXP(L.xp);S.stat.lessons++;if(bonus)S.stat.perfect++;S.stat.bestCombo=Math.max(S.stat.bestCombo,L.best);save();L.state='end';
  const lv1=levelOf(S.xp),got=checkBadges();sfx(got.length?'badge':'done');if(acc>=70||lv1>lv0||got.length)setTimeout(confetti,150);
  $('#lBar').style.width='100%';$('#combo').textContent='';lFoot.className='l-foot';
  const miss=[...new Set(L.miss)];
  qv.innerHTML=`<div class="q done"><div class="done-hero">${mascot(acc>=70?'cheer':'happy',110)}</div><h2>${acc>=90?'완벽하게 해냈어요':acc>=70?'잘했어요':'끝까지 해냈어요'}</h2><p class="muted">${L.u?esc(L.u.t):'복습'} · 문제 ${L.tot}개</p>
  <div class="done-stats"><div class="stat goal"><span class="k">얻은 XP</span><span class="v">+<span data-count="${L.xp}">${L.xp}</span></span></div><div class="stat"><span class="k">정답률</span><span class="v">${acc}<small>%</small></span></div><div class="stat fire"><span class="k">걸린 시간</span><span class="v">${Math.floor(secs/60)}:${String(secs%60).padStart(2,'0')}</span></div></div>
  ${lv1>lv0?`<div class="lvup"><b style="font-family:var(--kr)">Lv.${lv1}</b><span>${esc(rankOf(lv1))}(으)로 올라갔어요!</span></div>`:''}${got.length?`<div class="newb"><span style="width:100%;font-weight:800">새 업적</span>${got.map(b=>bdgHtml(b,false)).join('')}</div>`:''}
  ${miss.length?`<div class="miss"><h3>틀린 문제 · 10분 뒤 복습에 다시 나와요</h3>${miss.map(q=>`<div class="miss-row"><div class="c"><span>${esc(q.q||(q.k==='out'?'출력 맞히기':q.k==='bug'?'틀린 줄 찾기':'문제'))}</span>${q.e?`<small>${esc(q.e)}</small>`:''}</div></div>`).join('')}</div>`:''}</div>`;
  countUp(qv);
  footIn.innerHTML=`<div class="foot-row"><button class="btn" id="homeBtn">그만하기</button><button class="btn primary" id="againBtn">${L.u?'이어서 한 판 더':'한 판 더'}</button></div>`;}
function closeLesson(){if(L&&L.state!=='end'&&L.tot>0){addXP(L.xp);save();}L=null;$('#lesson').hidden=true;document.body.style.overflow='';animNext=true;refreshViews();}
$('#lesson').addEventListener('click',async e=>{if(!L)return;const it=L.qs[L.i],t=e.target;
  if(t.closest('#lClose')||t.closest('#homeBtn'))return closeLesson();
  if(t.closest('#againBtn')){const m=L.mode,u=L.u&&L.u.id;L=null;start(m,u);if(!L)closeLesson();return}
  if(t.closest('#nextBtn'))return next();
  if(t.closest('#checkBtn'))return check();
  if(t.closest('#giveUp')){if(L.state==='ask')finish(false);return}
  if(L.state!=='ask')return;const q=it&&it.q;if(!q)return;
  if(t.closest('#runBtn')){const r=await execFor(q,L.cm.getValue());return}
  const ob=t.closest('[data-opt]');if(ob){L.sel=+ob.dataset.opt;qv.querySelectorAll('[data-opt]').forEach(b=>b.classList.toggle('sel',b===ob));
    if(q.k==='fill'){const sl=$('#slot');sl.textContent=q.o[it.ord[L.sel]];}refreshCheck();if(S.set.fast&&(q.k==='mc'||q.k==='out'))check();return}
  const ln=t.closest('#bugCode .ln');if(ln){L.sel=+ln.dataset.ln;qv.querySelectorAll('#bugCode .ln').forEach(r=>r.classList.toggle('sel',r===ln));refreshCheck();if(S.set.fast)check();return}
  const lt=t.closest('[data-lt]');if(lt){const i=+lt.dataset.lt;
    if(lt.parentElement.id==='lineBank'){if(L.built.includes(i))return;L.built.push(i);lt.classList.add('used');}
    else{L.built=L.built.filter(x=>x!==i);qv.querySelector(`#lineBank [data-lt="${i}"]`).classList.remove('used');}
    $('#ansBox').innerHTML=L.built.map(x=>`<button class="btn lt" data-lt="${x}">${hl(q.lines[it.ord[x]],q.u.lang)}</button>`).join('');refreshCheck();return}});

/* ---------- 학습 탭 ---------- */
let animNext=true;
function curCourse(){return CM[S.ui.course]||CS[0]}
function nextUnit(c){return c.units.find(u=>uLearned(u)<u.q.length)||null}
function renderLearn(){const t=now(),c=curCourse(),goal=S.set.goal,tx=todayXP(),sk=streakN(),li=levelInfo(S.xp);
  const dueN=ALLQ.filter(q=>isDue(q.id,t)).length;const nu=nextUnit(c);const hr=new Date().getHours();
  const learnedAll=ALLQ.filter(q=>isLearned(q.id)).length;
  const mood=(hr>=23||hr<5)&&!dueN?'sleep':tx>=goal?'cheer':'idle';
  const msg=tx>=goal?'오늘 목표 달성! 내일도 버그 잡으러 와요.':dueN?`복습할 문제가 ${dueN}개 있어요. 금방 끝나요!`:tx>0?`목표까지 ${goal-tx} XP 남았어요.`:sk>0?`${sk}일째 이어 가는 중! 오늘도 한 단원?`:nu?`오늘은 「${esc(nu.t)}」부터 해 볼까요?`:'모든 단원을 마쳤어요. 놀이터에서 자유롭게 짜 봐요!';
  const wk=[];for(let i=6;i>=0;i--){const d=new Date(now()-i*DAY),k=dkey(d),v=S.days[k]||0;wk.push(`<div class="${v>=goal?'gold':v>0?'on':''} ${i===0?'today':''}"><i>${v>=goal?'★':'✓'}</i>${'일월화수목금토'[d.getDay()]}</div>`)}
  const X=[0,52,74,52,0,-52,-74,-52];
  let h=`<header class="top"><div class="brand"><h1>하루<i>코딩</i></h1><p>하루 10분, 혼자 배우는 코딩</p></div>${installEvt?`<button class="btn primary" id="installBtn" style="padding:8px 12px">앱 설치</button>`:''}<button class="icon-btn" data-open-set aria-label="설정">${ICON.gear}</button></header>
  <section class="hero">${mascot(mood,84)}<div class="bubble-s"><p class="hello" style="font-family:var(--mono)">${hr<11?'Good morning!':hr<18?'Hello, coder!':'Good evening!'}</p>${msg}</div><div class="lvl"><span class="rank" style="font-family:var(--kr)">${esc(li.rank)}</span><span class="n">Lv.${li.L} · ${S.xp} XP</span><div class="bar"><span style="width:${li.pct}%"></span></div><span class="next">${li.L<20?`다음 단계 ${esc(rankOf(li.L+1))}까지 ${li.left} XP`:'최고 단계예요'}</span></div></section>
  <div class="stats"><div class="stat fire"><span class="k">연속 학습</span><span class="v"><span data-count="${sk}">${sk}</span><small>일</small></span></div><div class="stat goal"><span class="k">오늘 XP</span><span class="v"><span data-count="${tx}">${tx}</span><small>/${goal}</small></span><div class="meter"><span style="width:${Math.min(100,tx/goal*100)}%"></span></div></div><div class="stat"><span class="k">익힌 문제</span><span class="v"><span data-count="${learnedAll}">${learnedAll}</span><small>/${ALLQ.length}</small></span></div></div>
  <div class="week" aria-label="최근 7일 학습">${wk.join('')}</div>
  ${dueN?`<button class="btn primary go-main" data-review="1"><span class="t">복습 먼저 · 약 ${Math.max(1,Math.round(Math.min(dueN,S.set.len)*.25))}분</span><span class="u">잊기 직전인 문제 ${dueN}개</span><span class="s">이번 판에 ${Math.min(dueN,S.set.len)}개</span></button>`:''}
  <section class="group"><h2>코스</h2><div class="courses">${CS.map(x=>`<button class="btn course" data-course="${x.id}" aria-pressed="${x===c}" style="--gc:var(--g-${x.g});--gs:var(--g-${x.g}-s)"><span class="c-ic">${({py:'Py',ht:'&lt;/&gt;',js:'JS'})[x.id]}</span><b>${esc(x.name)}</b><span class="cp">${Math.round(cPct(x)*100)}% 완료</span><div class="meter"><span style="width:${cPct(x)*100}%"></span></div></button>`).join('')}</div><p class="note">${esc(c.d)}</p></section>
  <section class="group"><h2>${esc(c.name)} 학습 경로<span>${c.units.filter(u=>uLearned(u)===u.q.length).length}/${c.units.length} 단원</span></h2><div class="path">${c.units.map((u,i)=>{const n=uLearned(u),tot=u.q.length,dn=uDue(u,t),done=n===tot,isNext=u===nu;const C=2*Math.PI*38;
    return `<button class="node ${n?'':'todo'} ${isNext?'next':''}" data-unit="${u.id}" style="--x:${X[i%8]}px;--gc:var(--g-${c.g})">${isNext?`<span class="start-tip">${n?'이어서':'시작'}</span>`:''}<span class="ring"><svg class="pr" viewBox="0 0 84 84"><circle cx="42" cy="42" r="38" stroke="var(--line)"/><circle cx="42" cy="42" r="38" stroke="var(--gc)" stroke-linecap="round" stroke-dasharray="${C}" stroke-dashoffset="${C*(1-n/tot)}"/></svg><span class="bub">${esc(u.ic)}</span>${done?'<span class="crown">✓</span>':''}${dn?`<span class="dueb">복습 ${dn}</span>`:''}</span><span class="nl">${i+1}. ${esc(u.t)}</span><span class="nd">${n}/${tot}</span></button>`}).join('')}</div></section>
  <section class="group"><h2>업적<span>${BADGES.filter(b=>S.badges[b[0]]).length}/${BADGES.length}</span></h2><div class="badges">${BADGES.map(b=>bdgHtml(b,!S.badges[b[0]])).join('')}</div></section>`;
  const vl=$('#vLearn');vl.innerHTML=h;if(animNext){animNext=false;enter(vl);countUp(vl);growBars(vl);}}
$('#vLearn').addEventListener('click',e=>{const t=e.target;
  const cb=t.closest('[data-course]');if(cb){S.ui.course=cb.dataset.course;save();animNext=true;renderLearn();if(CM[S.ui.course].lang==='python')warmPy();return}
  const nb=t.closest('[data-unit]');if(nb)return openUSheet(nb.dataset.unit);
  if(t.closest('[data-review]'))return start('review');
  const bb=t.closest('[data-bdg]');if(bb){const b=BADGES.find(x=>x[0]===bb.dataset.bdg);if(b)toast((S.badges[b[0]]?'달성 · ':'아직 · ')+b[3]);return}
  if(t.closest('#installBtn')&&installEvt){installEvt.prompt();installEvt.userChoice.finally(()=>{installEvt=null;renderLearn()});}});

/* ---------- 단원 시트 ---------- */
function openUSheet(id){const u=UM[id],c=u.c,n=uLearned(u),dn=uDue(u,now());
  $('#usheetIn').innerHTML=`<div class="u-head" style="--gc:var(--g-${c.g});--gs:var(--g-${c.g}-s)"><span class="c-ic">${esc(u.ic)}</span><div><h2>${u.ui+1}. ${esc(u.t)}</h2><p>${esc(u.d)}</p></div></div><div class="meter"><span style="width:${n/u.q.length*100}%;background:var(--g-${c.g})"></span></div><p class="note">${n}/${u.q.length} 문제 익힘${dn?` · 복습할 문제 ${dn}개`:''}</p>
  <div class="u-acts"><button class="btn" data-ucards="${u.id}">개념 카드 보기 <span>${u.cards.length}장 · 예제 실행</span></button><button class="btn primary" data-ustart="${u.id}">${n?'연습 이어서 하기':'연습 시작'} <span>문제 ${S.set.len}개</span></button><button class="btn" id="uClose">닫기</button></div>`;
  $('#usheet').hidden=false;}
function closeUSheet(now){const sh=$('#usheet');if(sh.hidden)return;if(now||RM){sh.hidden=true;return}sh.classList.add('closing');setTimeout(()=>{sh.classList.remove('closing');sh.hidden=true},210)}
$('#usheet').addEventListener('click',e=>{const t=e.target;if(t.id==='usheet'||t.closest('#uClose'))return closeUSheet();
  const s=t.closest('[data-ustart]');if(s)return start('unit',s.dataset.ustart);
  const c=t.closest('[data-ucards]');if(c){closeUSheet(true);openViewer(c.dataset.ucards,0);}});

/* ---------- 개념 카드 뷰어 ---------- */
const V={u:null,i:0};
function openViewer(uid,i){V.u=UM[uid];V.i=i||0;$('#viewer').hidden=false;document.body.style.overflow='hidden';if(V.u.lang==='python')warmPy();renderViewer();}
function closeViewer(){$('#viewer').hidden=true;document.body.style.overflow='';if(tab==='notes')renderNotes();}
function renderViewer(){const u=V.u,cd=u.cards[V.i],lang=u.lang,last=V.i===u.cards.length-1;
  $('#vTitle').textContent=`${u.ui+1}. ${u.t}`;$('#vDots').innerHTML=u.cards.map((_,k)=>`<i class="${k===V.i?'on':''}"></i>`).join('');
  $('#vIn').innerHTML=`<p class="need" style="font-weight:700;color:var(--g-${u.c.g})">${esc(u.c.name)} · 개념 ${V.i+1}/${u.cards.length}</p><h2>${esc(cd.h)}</h2><p class="p">${cd.p}</p>${cd.code?`<div id="vEd"></div><div class="run-row"><button class="btn primary" id="vRun">${ICON.play}실행</button><button class="btn" id="vReset">원래대로</button><button class="btn" id="vPlay">놀이터로</button></div>${cd.stdin?`<p class="need">입력값: ${cd.stdin.map(esc).join(', ')}</p>`:''}${lang==='html'?`<iframe class="preview" id="pv" sandbox="allow-scripts allow-same-origin allow-modals" title="미리보기"></iframe>`:''}<div class="console" id="out" ${lang==='html'?'data-html':''}><span class="lab">${lang==='html'?'콘솔':'실행 결과'}</span><span style="color:var(--code-muted)">${lang==='html'?'(console.log 출력이 여기에 나와요)':'실행을 누르면 결과가 나와요. 코드를 고쳐서 실행해 봐도 돼요.'}</span></div>`:''}`;
  if(!RM){const v=$('#vIn');v.classList.remove('v-anim');void v.offsetWidth;v.classList.add('v-anim');}
  V.cm=cd.code?makeEditor($('#vEd'),lang,cd.code):null;if(cd.code&&lang==='html')renderHtml($('#pv'),cd.code);
  $('#vBody').scrollTop=0;
  $('#vFoot').innerHTML=`<button class="btn" id="vPrev" ${V.i?'':'disabled'}>이전</button>${last?`<button class="btn primary" data-ustart="${u.id}">연습 시작</button>`:`<button class="btn primary" id="vNext">다음</button>`}`;}
$('#viewer').addEventListener('click',async e=>{const t=e.target;const cd=V.u&&V.u.cards[V.i];
  if(t.closest('#vClose'))return closeViewer();
  if(t.closest('#vPrev')&&V.i>0){V.i--;return renderViewer()}
  if(t.closest('#vNext')){V.i++;return renderViewer()}
  const s=t.closest('[data-ustart]');if(s){closeViewer();return start('unit',s.dataset.ustart)}
  if(t.closest('#vRun')&&V.cm){await execFor({u:V.u,stdin:cd.stdin},V.cm.getValue());badgeToast(checkBadges());save();return}
  if(t.closest('#vReset')&&V.cm){V.cm.setValue(cd.code);return}
  if(t.closest('#vPlay')&&V.cm){P.lang=V.u.lang;S.code[P.lang]=V.cm.getValue();if(cd.stdin)S.ui['stdin_'+P.lang]=cd.stdin.join('\n');save();closeViewer();setTab('play');}});

/* ---------- 개념 탭 ---------- */
function renderNotes(){const c=CM[S.ui.notes]||curCourse();
  let h=`<header class="top"><div class="brand"><h1>개념 노트</h1><p>단원별 핵심 설명과 실행해 볼 수 있는 예제</p></div><button class="icon-btn" data-open-set aria-label="설정">${ICON.gear}</button></header>
  <div class="seg" id="nSeg">${CS.map(x=>`<button data-nc="${x.id}" aria-pressed="${x===c}">${esc(x.name)}</button>`).join('')}</div>`;
  c.units.forEach(u=>{h+=`<section class="group"><h2>${u.ui+1}. ${esc(u.t)}<span>${u.cards.length}장</span></h2><div class="c-list">${u.cards.map((cd,i)=>`<button class="btn c-item" data-card="${u.id}|${i}" style="--gc:var(--g-${c.g});--gs:var(--g-${c.g}-s)"><span class="c-ic">${i===0?esc(u.ic):i+1}</span><span><b>${esc(cd.h)}</b><small>${esc(cd.p.replace(/<[^>]+>/g,'').replace(/&lt;/g,'<').replace(/&gt;/g,'>').slice(0,46))}…</small></span></button>`).join('')}</div></section>`});
  const v=$('#vNotes');v.innerHTML=h;}
$('#vNotes').addEventListener('click',e=>{const t=e.target;const s=t.closest('[data-nc]');if(s){S.ui.notes=s.dataset.nc;save();renderNotes();enter($('#vNotes'));return}
  const c=t.closest('[data-card]');if(c){const [u,i]=c.dataset.card.split('|');openViewer(u,+i);}});

/* ---------- 놀이터 ---------- */
const P={lang:S.ui.pl||'python',cm:null};
const STARTER={python:'# 자유롭게 써 보세요\nname = input("이름: ")\nfor i in range(3):\n    print(f"{name} 화이팅! {i + 1}")\n',javascript:'// 자유롭게 써 보세요\nconst fruits = ["사과", "바나나", "포도"];\nfor (const f of fruits) {\n  console.log(`${f} 맛있다`);\n}\n',html:'<!-- 자유롭게 써 보세요 -->\n<h1>나의 페이지</h1>\n<button id="b">눌러 보세요</button>\n<p id="out">0번 눌렀어요</p>\n<style>\n  h1 { color: #4338CA; }\n</style>\n<script>\n  let n = 0;\n  document.querySelector("#b").addEventListener("click", () => {\n    n++;\n    document.querySelector("#out").textContent = n + "번 눌렀어요";\n  });\n</script>\n'};
function renderPlay(){const lang=P.lang;const ex=CS.flatMap(c=>c.units.filter(u=>u.lang===lang).flatMap(u=>u.cards.filter(cd=>cd.code).map(cd=>({u,cd}))));
  $('#vPlay').innerHTML=`<header class="top"><div class="brand"><h1>놀이터</h1><p>채점 없이 마음대로 코드를 짜고 실행해요</p></div><button class="icon-btn" data-open-set aria-label="설정">${ICON.gear}</button></header>
  <div class="seg" id="pSeg">${['python','html','javascript'].map(l=>`<button data-pl="${l}" aria-pressed="${l===lang}">${LANGNAME[l]}</button>`).join('')}</div>
  <div class="pg-head"><select class="pick" id="pEx" aria-label="예제 불러오기"><option value="">예제 불러오기…</option>${ex.map((x,i)=>`<option value="${i}">${x.u.ui+1}. ${esc(x.u.t)} · ${esc(x.cd.h)}</option>`).join('')}</select></div>
  <div id="pEd"></div>
  ${lang==='python'?`<textarea class="stdin" id="pIn" placeholder="입력값 (input()에 한 줄씩 차례로 들어가요)" rows="2">${esc(S.ui.stdin_python||'')}</textarea>`:''}
  <div class="run-row"><button class="btn primary" id="pRun">${ICON.play}실행</button><button class="btn" id="pClear">지우기</button><button class="btn" id="pReset">처음 예제로</button></div>
  ${lang==='html'?`<iframe class="preview" id="pv" sandbox="allow-scripts allow-same-origin allow-modals" title="미리보기" style="height:320px"></iframe>`:''}
  <div class="console" id="out" ${lang==='html'?'data-html':''}><span class="lab">${lang==='html'?'콘솔':'실행 결과'}</span><span style="color:var(--code-muted)">${lang==='python'?(CAP?'처음 실행할 때 인터넷에서 파이썬(약 10MB)을 한 번 받아요.':'처음 실행할 때 파이썬을 준비하느라 몇 초 걸려요.'):'실행을 누르면 결과가 나와요.'}</span></div>`;
  P.cm=makeEditor($('#pEd'),lang,S.code[lang]!=null?S.code[lang]:STARTER[lang]);
  P.cm.on('change',()=>{S.code[lang]=P.cm.getValue();clearTimeout(P.t);P.t=setTimeout(save,500)});
  if(lang==='html')renderHtml($('#pv'),P.cm.getValue());if(lang==='python')warmPy();
  P.ex=ex;}
$('#vPlay').addEventListener('click',async e=>{const t=e.target;const s=t.closest('[data-pl]');if(s){P.lang=s.dataset.pl;S.ui.pl=P.lang;save();renderPlay();return}
  if(t.closest('#pRun')){const stdin=P.lang==='python'?($('#pIn').value||'').split('\n').filter((x,i,a)=>x!==''||i<a.length-1):[];if(P.lang==='python'){S.ui.stdin_python=$('#pIn').value;}await execFor({u:{lang:P.lang},stdin},P.cm.getValue());badgeToast(checkBadges());save();return}
  if(t.closest('#pClear')){P.cm.setValue('');P.cm.focus();return}
  if(t.closest('#pReset')){P.cm.setValue(STARTER[P.lang]);return}});
$('#vPlay').addEventListener('change',e=>{if(e.target.id==='pEx'&&e.target.value!==''){const x=P.ex[+e.target.value];P.cm.setValue(x.cd.code);if(x.cd.stdin&&$('#pIn'))$('#pIn').value=x.cd.stdin.join('\n');e.target.value='';toast('예제를 불러왔어요')}});

/* ---------- 모션 도우미 ---------- */
function stagger(root){[...root.children].forEach((c,i)=>c.style.setProperty('--i',Math.min(i,12)));root.querySelectorAll('.badges,.path,.courses').forEach(u=>[...u.children].forEach((c,i)=>c.style.setProperty('--i',Math.min(i,14))))}
function enter(root){if(RM)return;stagger(root);root.classList.remove('enter');void root.offsetWidth;root.classList.add('enter');setTimeout(()=>root.classList.remove('enter'),1400)}
function countUp(root){if(RM)return;root.querySelectorAll('[data-count]').forEach(el=>{const to=+el.dataset.count;if(!to)return;const t0=performance.now(),d=700;(function f(t){const k=Math.min(1,(t-t0)/d),e=1-Math.pow(1-k,3);el.textContent=Math.round(to*e);if(k<1)requestAnimationFrame(f)})(t0)})}
function growBars(root){if(RM)return;const bars=[...root.querySelectorAll('.meter>span,.lvl .bar>span')];const w=bars.map(b=>b.style.width);bars.forEach(b=>{b.style.transition='none';b.style.width='0'});void root.offsetWidth;requestAnimationFrame(()=>bars.forEach((b,i)=>{b.style.transition='';b.style.width=w[i]}))}
function moveInd(){const ind=$('#navInd'),b=document.querySelector('.nav [aria-current="page"]');if(!ind||!b)return;ind.style.width=b.offsetWidth+'px';ind.style.transform=`translateX(${b.offsetLeft}px)`}
addEventListener('resize',moveInd);

/* ---------- 탭 ---------- */
let tab=lsGet('haru-tab')||'learn';
function setTab(t){if(!['learn','notes','play'].includes(t))t='learn';tab=t;lsSet('haru-tab',t);
  $('#vLearn').hidden=t!=='learn';$('#vNotes').hidden=t!=='notes';$('#vPlay').hidden=t!=='play';
  document.querySelectorAll('.nav [data-tab]').forEach(b=>{if(b.dataset.tab===t)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current')});
  animNext=true;refreshViews();window.scrollTo(0,0);moveInd();if(t!=='learn')enter($(t==='notes'?'#vNotes':'#vPlay'));}
function refreshViews(){if(tab==='learn')renderLearn();else if(tab==='notes')renderNotes();else renderPlay();}
document.addEventListener('click',e=>{const tb=e.target.closest('.nav [data-tab]');if(tb){setTab(tb.dataset.tab);return}if(e.target.closest('[data-open-set]'))openSheet();});
document.addEventListener('keydown',e=>{if(!$('#sheet').hidden&&e.key==='Escape')return closeSheet();if(L){if(e.key==='Escape')return closeLesson();if(e.target.closest&&e.target.closest('.CodeMirror'))return;
  if(e.key==='Enter'){if(e.target.closest&&e.target.closest('button')&&!['nextBtn','checkBtn','againBtn'].includes(e.target.id))return;e.preventDefault();if(L.state==='ask')check();else if(L.state==='done')next();else if(L.state==='end')$('#againBtn').click();}
  else if(L.state==='ask'&&/^[1-4]$/.test(e.key)){const b=qv.querySelector(`[data-opt="${+e.key-1}"]`);if(b)b.click()}}});

/* ---------- 설정 ---------- */
function syncSheet(){['setLen','setGoal','setFs'].forEach(id=>{const el=$('#'+id),k=el.dataset.k;el.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.v)===String(S.set[k])))});
  $('#setTypes').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',!!S.set[b.dataset.k]));$('#verNote').textContent='버전 '+APP_VER+(CAP?' · 안드로이드 앱':' · 웹앱');}
function openSheet(){syncSheet();$('#bk').value='';$('#reset').textContent='진도 초기화';$('#sheet').hidden=false;}
function closeSheet(){const sh=$('#sheet');if(RM||sh.hidden){sh.hidden=true;return refreshViews()}sh.classList.add('closing');setTimeout(()=>{sh.classList.remove('closing');sh.hidden=true;refreshViews()},210)}
$('#sClose').onclick=closeSheet;
$('#sheet').addEventListener('click',e=>{if(e.target.id==='sheet')return closeSheet();
  const sb=e.target.closest('.seg button');if(sb){const k=sb.parentElement.dataset.k;S.set[k]=+sb.dataset.v;save();syncSheet();return}
  const cb=e.target.closest('.chk button');if(cb){S.set[cb.dataset.k]=!S.set[cb.dataset.k];save();syncSheet();}});
$('#bkCopy').onclick=()=>{const txt=JSON.stringify(S);$('#bk').value=txt;try{navigator.clipboard.writeText(txt).then(()=>toast('진도를 복사했어요'),()=>{$('#bk').select();toast('위 글을 직접 복사하세요')})}catch(e){$('#bk').select()}};
$('#bkLoad').onclick=()=>{try{const x=JSON.parse($('#bk').value);if(!x||typeof x.q!=='object')throw 0;S=normS(x);save();syncSheet();toast('진도를 복원했어요')}catch(e){toast('복원할 수 없는 내용이에요')}};
$('#reset').onclick=e=>{const b=e.currentTarget;if(b.dataset.arm!=='1'){b.dataset.arm='1';b.textContent='정말 지울까요? 한 번 더 누르세요';setTimeout(()=>{b.dataset.arm='';b.textContent='진도 초기화'},4000);return}
  S=normS({set:S.set,ui:{onboarded:true}});save();b.dataset.arm='';b.textContent='진도 초기화';toast('진도를 초기화했어요')};

/* ---------- 인트로 · 첫 안내 ---------- */
function runIntro(done){const el=$('#intro');if(S.set.intro===false){el.remove();return done()}
  const cmd='> print("하루코딩")';const tl=$('#termLine');let i=0,closed=false;
  const close=()=>{if(closed)return;closed=true;el.classList.add('out');setTimeout(()=>el.remove(),550);done()};el.addEventListener('click',close);
  if(RM){tl.textContent=cmd;$('#introM').innerHTML=mascot('cheer',96);setTimeout(close,900);return}
  (function type(){tl.innerHTML=esc(cmd.slice(0,i))+'<span class="cur"></span>';if(i++<cmd.length)return setTimeout(type,i<3?160:55);
    $('#introM').innerHTML=mascot('cheer',96);$('#introM').style.animationDelay='.1s';$('#introLogo').style.animationDelay='.35s';$('#introSub').style.animationDelay='.6s';setTimeout(close,2300)})();}
const ONB={i:0,goal:50,c:'py'};
function renderOnb(){const o=$('#onbIn');const dots=`<div class="onb-dots">${[0,1,2].map(k=>`<i class="${k===ONB.i?'on':''}"></i>`).join('')}</div>`;
  if(ONB.i===0)o.innerHTML=`${mascot('happy',120)}<h2 style="font-family:var(--kr)">안녕하세요!<br>버그 먹는 벌레, 버기예요</h2><p class="lead">코딩을 한 번도 안 해 봤어도 괜찮아요. 하루 10분이면 충분해요.</p><ul><li><b>읽</b><span>짧은 <strong>개념 카드</strong>로 배우고, 예제를 바로 실행해 봐요.</span></li><li><b>풀</b><span>출력 맞히기·빈칸·순서·틀린 줄 찾기로 연습해요.</span></li><li><b>짜</b><span>직접 코드를 써서 실행하고 자동으로 채점받아요.</span></li><li><b>복</b><span>틀린 문제만 골라서 간격을 두고 다시 나와요.</span></li></ul>${dots}<button class="btn primary onb-go" data-onb="next">다음</button>`;
  else if(ONB.i===1)o.innerHTML=`${mascot('idle',100)}<h2 style="font-family:var(--kr)">하루에 얼마나 할까요?</h2><p class="lead">설정에서 언제든 바꿀 수 있어요.</p><div class="onb-pick">${[[30,'가볍게','하루 5분 정도'],[50,'꾸준히','하루 10분 정도'],[100,'열심히','하루 20분 정도']].map(([v,a,b])=>`<button class="btn" data-goal="${v}" aria-pressed="${ONB.goal===v}"><b>${a} · ${v} XP</b><span>${b}</span></button>`).join('')}</div>${dots}<button class="btn primary onb-go" data-onb="next">다음</button>`;
  else o.innerHTML=`${mascot('cheer',100)}<h2 style="font-family:var(--kr)">무엇부터 배울까요?</h2><p class="lead">다른 코스도 언제든 바꿀 수 있어요.</p><div class="onb-pick">${[['py','Python','처음 배우기 가장 쉬워요. 추천!'],['ht','HTML·CSS','웹페이지를 직접 만들어 봐요'],['js','JavaScript','웹페이지를 움직여 봐요']].map(([v,a,b])=>`<button class="btn" data-oc="${v}" aria-pressed="${ONB.c===v}"><b>${a}</b><span>${b}</span></button>`).join('')}</div>${dots}<button class="btn primary onb-go" data-onb="done">코딩 시작!</button>`;}
function showOnb(){if(S.ui.onboarded)return;if(Object.keys(S.q).length){S.ui.onboarded=true;save();return}$('#onb').hidden=false;renderOnb();}
$('#onb').addEventListener('click',e=>{const t=e.target;const g=t.closest('[data-goal]');if(g){ONB.goal=+g.dataset.goal;return renderOnb()}
  const c=t.closest('[data-oc]');if(c){ONB.c=c.dataset.oc;return renderOnb()}
  const b=t.closest('[data-onb]');if(!b)return;if(b.dataset.onb==='next'){ONB.i++;renderOnb();$('#onb').scrollTop=0;return}
  S.set.goal=ONB.goal;S.ui.course=ONB.c;S.ui.onboarded=true;save();$('#onb').hidden=true;animNext=true;refreshViews();confetti();sfx('done');if(ONB.c==='py')warmPy();});

let tT=0;function toast(m){const el=$('#toast');el.textContent=m;el.hidden=true;void el.offsetWidth;el.hidden=false;clearTimeout(tT);tT=setTimeout(()=>el.hidden=true,2200)}
let installEvt=null;addEventListener('beforeinstallprompt',e=>{e.preventDefault();installEvt=e;if(tab==='learn'&&!L)renderLearn()});

setTab(tab);requestAnimationFrame(moveInd);setTimeout(moveInd,600);
runIntro(showOnb);
if(CAP){const App=plug('App');if(App)App.addListener('backButton',()=>{if(!$('#sheet').hidden)return closeSheet();if(!$('#usheet').hidden)return closeUSheet();if(!$('#viewer').hidden)return closeViewer();if(L)return closeLesson();if(tab!=='learn')return setTab('learn');App.exitApp()});}
else if('serviceWorker' in navigator&&location.protocol==='https:'){navigator.serviceWorker.register('sw.js').catch(()=>{})}
if(curCourse().lang==='python'&&tab==='learn')setTimeout(warmPy,2500);
window.__haru={UM,QM,ALLQ,runPy,runJs,renderHtml,gradeCode,norm};
})();
