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
self.onmessage = (e) => {
  const { id, code } = e.data;
  let out = '';
  const log = (...a) => { out += a.map((x) => show(x)).join(' ') + '\n'; };
  const con = { log, info: log, warn: log, error: log };
  try {
    new Function('console', '"use strict";\n' + code)(con);
    self.postMessage({ id, ok: true, out });
  } catch (err) {
    self.postMessage({ id, ok: false, out, err: (err && err.name ? err.name + ': ' : '') + (err && err.message || err) });
  }
};
