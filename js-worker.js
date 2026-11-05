// JavaScript 실행기: console.log 출력을 모아서 돌려준다. 무한 반복이면 화면 쪽에서 작업을 끊는다.
function show(v, depth) {
  depth = depth || 0;
  if (typeof v === 'string') return depth ? "'" + v + "'" : v;
  if (v === null) return 'null';
  if (v === undefined) return 'undefined';
  if (typeof v === 'function') return '[Function: ' + (v.name || 'anonymous') + ']';
  if (Array.isArray(v)) return depth > 2 ? '[Array]' : '[' + v.map((x) => show(x, depth + 1)).join(', ') + ']';
  if (typeof v === 'object') {
    if (depth > 2) return '[Object]';
    const ks = Object.keys(v);
    return ks.length ? '{ ' + ks.map((k) => k + ': ' + show(v[k], depth + 1)).join(', ') + ' }' : '{}';
  }
  return String(v);
}
// 워커에는 브라우저 저장소가 없어서, 예제가 그대로 돌도록 메모리 저장소를 흉내 낸다(실행마다 비워짐).
const mem = new Map();
const fakeStorage = {
  getItem: (k) => (mem.has(String(k)) ? mem.get(String(k)) : null),
  setItem: (k, v) => { mem.set(String(k), String(v)); },
  removeItem: (k) => { mem.delete(String(k)); },
  clear: () => mem.clear(),
  get length() { return mem.size; },
};
const realSetTimeout = self.setTimeout.bind(self), realClear = self.clearTimeout.bind(self);
self.onmessage = async (e) => {
  const { id, code } = e.data;
  let out = '', pending = 0, failed = null;
  mem.clear();
  const log = (...a) => { out += a.map((x) => show(x)).join(' ') + '\n'; };
  const con = { log, info: log, warn: log, error: log };
  const timers = new Set();
  const st = (fn, ms, ...args) => { pending++; const t = realSetTimeout(() => { timers.delete(t); pending--; try { fn(...args); } catch (err) { failed = failed || err; } }, Math.min(ms || 0, 2000)); timers.add(t); return t; };
  const ct = (t) => { if (timers.delete(t)) { pending--; realClear(t); } };
  const onRej = (ev) => { failed = failed || ev.reason; ev.preventDefault && ev.preventDefault(); };
  self.addEventListener('unhandledrejection', onRej);
  try {
    const ret = new Function('console', 'localStorage', 'setTimeout', 'clearTimeout', '"use strict";\n' + code)(con, fakeStorage, st, ct);
    if (ret && typeof ret.then === 'function') await ret;
    // 타이머·Promise로 나중에 찍히는 출력까지 기다린다(최대 약 2.5초)
    const t0 = Date.now();
    do { await new Promise((r) => realSetTimeout(r, pending ? 20 : 0)); } while (pending > 0 && Date.now() - t0 < 2500);
    await new Promise((r) => realSetTimeout(r, 0));
    if (failed) throw failed;
    self.postMessage({ id, ok: true, out });
  } catch (err) {
    self.postMessage({ id, ok: false, out, err: (err && err.name ? err.name + ': ' : '') + (err && err.message || err) });
  } finally {
    self.removeEventListener('unhandledrejection', onRej);
    timers.forEach(realClear);
  }
};
