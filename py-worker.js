// Python 실행기: 화면이 멈추지 않도록 별도 작업 스레드에서 Pyodide를 돌린다.
// 앱(APK)에는 Python 실행기를 넣지 않고, 처음 실행할 때 인터넷에서 한 번 받아 둔다.
const SOURCES = ['pyodide/', 'https://incastle-wq.github.io/harucoding/pyodide/', 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/'];
let BASE = null;
for (const src of SOURCES) {
  try { importScripts(src + 'pyodide.js'); BASE = new URL(src, self.location.href).href; break; } catch (e) { /* 다음 주소 시도 */ }
}
let pyReady = null;
function boot() {
  if (!pyReady) pyReady = BASE ? loadPyodide({ indexURL: BASE }) : Promise.reject(new Error('인터넷에 연결한 뒤 다시 실행해 주세요.'));
  return pyReady;
}
async function run({ id, code, stdin, warm }) {
  let out = '';
  try {
    const py = await boot();
    if (warm) return self.postMessage({ id, ok: true, out: '' });
    const dec = new TextDecoder('utf-8');
    const sink = { write: (b) => { out += dec.decode(b, { stream: true }); return b.length; } };
    py.setStdout(sink);
    py.setStderr(sink);
    const lines = (stdin || []).slice();
    py.setStdin({ stdin: () => { if (!lines.length) return null; const v = String(lines.shift()); out += v + '\n'; return v; } });
    const g = py.globals.get('dict')();
    try { await py.runPythonAsync(code, { globals: g }); } finally { g.destroy(); }
    self.postMessage({ id, ok: true, out });
  } catch (err) {
    self.postMessage({ id, ok: false, out, err: String((err && err.message) || err) });
  }
}
let chain = Promise.resolve();
self.onmessage = (e) => { chain = chain.then(() => run(e.data)); };
