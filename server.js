const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const os = require('os');

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

// Real-time Excel Status & Automatic Update Endpoints
let isUpdating = false;

function handleExcelApis(req, res, reqPath) {
  if (reqPath === '/api/excel-status') {
    try {
      const retailFile = path.join(DOCS_DIR, 'Dashboard HTML RETAIL .xlsx');
      const prepagoFile = path.join(DOCS_DIR, 'Dashboard HTML PREPAGO.xlsx');
      const indexFile = path.join(DOCS_DIR, 'index.html');

      const retailStat = fs.existsSync(retailFile) ? fs.statSync(retailFile) : null;
      const prepagoStat = fs.existsSync(prepagoFile) ? fs.statSync(prepagoFile) : null;
      const indexStat = fs.existsSync(indexFile) ? fs.statSync(indexFile) : null;

      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({
        isUpdating,
        retail: retailStat ? { mtime: retailStat.mtime, size: retailStat.size } : null,
        prepago: prepagoStat ? { mtime: prepagoStat.mtime, size: prepagoStat.size } : null,
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

    isUpdating = true;
    console.log('[SERVER] Iniciando proceso de actualización de Excels vía API...');
    
    const { exec } = require('child_process');
    exec('python "actualizar_datos.py"', { cwd: DOCS_DIR, maxBuffer: 15 * 1024 * 1024 }, (err, stdout, stderr) => {
      isUpdating = false;
      if (err) {
        console.error('[SERVER ERROR] Error en actualizar_datos.py:', err.message);
        res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ success: false, error: err.message, stderr: String(stderr) }));
        return;
      }

      console.log('[SERVER] Proceso de actualización finalizado con éxito.');
      let count = 0;
      const m = (stdout || '').match(/COMBINED TOTAL RECORDS:s*([0-9,]+)/i);
      if (m) count = parseInt(m[1].replace(/,/g, ''), 10);

      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({
        success: true,
        records: count,
        message: '¡Dashboard actualizado exitosamente desde los Excels!',
        timestamp: new Date().toISOString()
      }));
    });
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

  // Real-time tunnel and network endpoint
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

    // Enable gzip compression for html, json, js, and css
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
  console.log(`[SALESLAND SERVER LIVE GZIP] Puerto: ${PORT} | Directorio: ${DOCS_DIR}`);
  console.log(`-> Local:     http://localhost:${PORT}/index.html`);
  console.log(`-> Red WiFi:  http://${ip}:${PORT}/index.html`);
  console.log(`-> Enlace Web: ${tunnel}/index.html`);
});
