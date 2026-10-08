const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const os = require('os');
const { exec } = require('child_process');

const DOCS_DIR = path.resolve('C:/Users/Lenovo/Documents/Mi dashboard');
const PORT = 8080;

function getLocalIp() {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address;
      }
    }
  }
  return '127.0.0.1';
}

function getActiveTunnelUrl() {
  const logPath = path.join(DOCS_DIR, 'cloudflared.log');
  if (fs.existsSync(logPath)) {
    try {
      const content = fs.readFileSync(logPath, 'utf8');
      const matches = content.match(/https:\/\/[a-zA-Z0-9-]+\.trycloudflare\.com/g);
      if (matches && matches.length > 0) {
        return matches[matches.length - 1];
      }
    } catch (e) {}
  }
  return 'https://preventing-ought-trading-yard.trycloudflare.com';
}

// ======================================================================
// 1. SISTEMA DE DETECCIÓN Y ACTUALIZACIÓN AUTOMÁTICA INTELIGENTE
// ======================================================================
let isUpdating = false;
let autoSyncTimeout = null;
const WATCHED_FILES = [
  'Dashboard HTML RETAIL .xlsx',
  'Dashboard HTML PREPAGO.xlsx',
  'RETAIL P2.xlsx'
];
let fileMtimes = {};

function initFileWatcher() {
  for (const f of WATCHED_FILES) {
    const fullPath = path.join(DOCS_DIR, f);
    try {
      if (fs.existsSync(fullPath)) {
        const stat = fs.statSync(fullPath);
        fileMtimes[f] = stat.mtimeMs;
      }
    } catch(e) {}
  }
}

function triggerAutoUpdate(reason) {
  if (isUpdating) {
    console.log(`[AUTO-SYNC] Ya hay una actualización en curso. Se pospone para el siguiente ciclo.`);
    return;
  }

  isUpdating = true;
  const timeStr = new Date().toLocaleTimeString();
  console.log(`\n======================================================================`);
  console.log(`[AUTO-SYNC ${timeStr}] ⚡ ${reason}`);
  console.log(`[AUTO-SYNC] 🔄 Procesando archivos Excel y publicando en GitHub Pages...`);
  console.log(`======================================================================`);

  exec('python "actualizar_datos.py"', { cwd: DOCS_DIR, maxBuffer: 25 * 1024 * 1024 }, (err, stdout, stderr) => {
    isUpdating = false;
    const finishTime = new Date().toLocaleTimeString();
    if (err) {
      console.error(`[AUTO-SYNC ERROR ${finishTime}] Falló la actualización:`, err.message);
    } else {
      console.log(`\n======================================================================`);
      console.log(`[AUTO-SYNC ${finishTime}] ✅ ¡DASHBOARD LOCAL Y GITHUB PAGES ACTUALIZADOS!`);
      console.log(`======================================================================\n`);
    }
  });
}

// Inicializar tiempos de modificación
initFileWatcher();

// Comprobación periódica cada 4 segundos
setInterval(() => {
  if (isUpdating) return;
  for (const f of WATCHED_FILES) {
    const fullPath = path.join(DOCS_DIR, f);
    try {
      if (fs.existsSync(fullPath)) {
        const stat = fs.statSync(fullPath);
        const prevMtime = fileMtimes[f] || 0;
        // Si el archivo fue modificado (diferencia mayor a 2 segundos)
        if (prevMtime > 0 && stat.mtimeMs > prevMtime + 2000) {
          fileMtimes[f] = stat.mtimeMs;
          console.log(`[AUTO-SYNC] Detectado guardado en '${f}'. Esperando 6s a que Excel termine de escribir...`);
          if (autoSyncTimeout) clearTimeout(autoSyncTimeout);
          autoSyncTimeout = setTimeout(() => {
            triggerAutoUpdate(`Detección de nuevo guardado en '${f}'`);
          }, 6000);
          break;
        }
        fileMtimes[f] = stat.mtimeMs;
      }
    } catch(e) {}
  }
}, 4000);

// ======================================================================
// 2. ENDPOINTS Y APIS
// ======================================================================
function handleExcelApis(req, res, reqPath) {
  if (reqPath === '/api/excel-status') {
    try {
      const retailFile = path.join(DOCS_DIR, 'Dashboard HTML RETAIL .xlsx');
      const prepagoFile = path.join(DOCS_DIR, 'Dashboard HTML PREPAGO.xlsx');
      const p2File = path.join(DOCS_DIR, 'RETAIL P2.xlsx');
      const indexFile = path.join(DOCS_DIR, 'index.html');

      const retailStat = fs.existsSync(retailFile) ? fs.statSync(retailFile) : null;
      const prepagoStat = fs.existsSync(prepagoFile) ? fs.statSync(prepagoFile) : null;
      const p2Stat = fs.existsSync(p2File) ? fs.statSync(p2File) : null;
      const indexStat = fs.existsSync(indexFile) ? fs.statSync(indexFile) : null;

      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({
        isUpdating,
        retail: retailStat ? { mtime: retailStat.mtime, size: retailStat.size } : null,
        prepago: prepagoStat ? { mtime: prepagoStat.mtime, size: prepagoStat.size } : null,
        p2: p2Stat ? { mtime: p2Stat.mtime, size: p2Stat.size } : null,
        dashboard: indexStat ? { mtime: indexStat.mtime, size: indexStat.size } : null
      }));
      return true;
    } catch(e) {
      res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({ error: e.message }));
      return true;
    }
  }

  if (reqPath === '/api/actualizar-datos' || reqPath === '/api/sync-excels') {
    if (isUpdating) {
      res.writeHead(429, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({ success: false, message: 'La actualización ya está en curso. Por favor espera unos momentos.' }));
      return true;
    }

    triggerAutoUpdate('Solicitud manual desde interfaz web');
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({
      success: true,
      message: 'Actualización iniciada en segundo plano...',
      timestamp: new Date().toISOString()
    }));
    return true;
  }

  return false;
}

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    return res.end();
  }

  let reqPath = decodeURI(req.url.split('?')[0]);
  if (reqPath === '/' || reqPath === '') {
    reqPath = '/index.html';
  }

  if (handleExcelApis(req, res, reqPath)) return;

  if (reqPath === '/api/tunnel' || reqPath === '/api/network-info') {
    const localIp = getLocalIp();
    const rawTunnel = getActiveTunnelUrl();
    const tunnelUrl = rawTunnel.endsWith('/index.html') ? rawTunnel : rawTunnel + '/index.html';
    const wifiUrl = `http://${localIp}:${PORT}/index.html`;
    const localUrl = `http://localhost:${PORT}/index.html`;

    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    return res.end(JSON.stringify({
      tunnelUrl,
      wifiUrl,
      localUrl,
      localIp,
      hasTunnel: !tunnelUrl.includes('placeholder')
    }));
  }

  const filePath = path.join(DOCS_DIR, reqPath);

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      return res.end('Archivo no encontrado');
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';
    const acceptEncoding = req.headers['accept-encoding'] || '';
    const compressible = ['.html', '.json', '.js', '.css'].includes(ext);

    if (compressible && acceptEncoding.includes('gzip')) {
      res.writeHead(200, {
        'Content-Type': contentType,
        'Content-Encoding': 'gzip'
      });
      const stream = fs.createReadStream(filePath);
      const gzip = zlib.createGzip({ level: 5 });
      stream.pipe(gzip).pipe(res);
    } else {
      res.writeHead(200, {
        'Content-Type': contentType,
        'Content-Length': stats.size
      });
      const stream = fs.createReadStream(filePath);
      stream.pipe(res);
    }
  });
});

server.listen(PORT, '0.0.0.0', () => {
  const ip = getLocalIp();
  const tunnel = getActiveTunnelUrl();
  console.log(`======================================================================`);
  console.log(`[SALESLAND SERVER LIVE & AUTO-SYNC ACTIVO]`);
  console.log(`-> Local:        http://localhost:${PORT}/index.html`);
  console.log(`-> Red WiFi:     http://${ip}:${PORT}/index.html`);
  console.log(`-> Enlace Web:   ${tunnel}/index.html`);
  console.log(`-> Auto-Sync:    Vigilando 'Dashboard HTML RETAIL .xlsx', 'Dashboard HTML PREPAGO.xlsx' y 'RETAIL P2.xlsx'`);
  console.log(`======================================================================`);
});
