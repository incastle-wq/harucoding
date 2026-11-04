// Python 실행기: 화면이 멈추지 않도록 별도 작업 스레드에서 Pyodide를 돌린다.
importScripts('pyodide/pyodide.js');
let pyReady = null;
function boot() {
  if (!pyReady) pyReady = loadPyodide({ indexURL: new URL('pyodide/', self.location.href).href });
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
