# CLAUDE.md — Salesland Dashboard Retail P1

Este archivo contiene las directivas, arquitectura y contexto completo del proyecto para trabajar directamente con Claude (Claude Code CLI, Claude Projects o Claude Chat).

---

## 📌 1. Información General y Enlaces Oficiales

* **Nombre del Proyecto:** Salesland Retail P1 - Panel Gerencial de Rendimiento Comercial
* **Repositorio GitHub:** [https://github.com/saleslandretail24-afk/Salesland-Dashboard-Retail-P1](https://github.com/saleslandretail24-afk/Salesland-Dashboard-Retail-P1)
* **URL de Producción (GitHub Pages):**  
  `https://saleslandretail24-afk.github.io/Salesland-Dashboard-Retail-P1/index.html`
* **Tecnología:** Single Page Application (SPA) en Vanilla HTML5, CSS3 moderno con variables CSS, JavaScript ES6+ nativo, Chart.js y mapa coroplético interactivo SVG de Costa Rica. No usa frameworks pesados ni bundlers (Webpack/Vite).

---

## 🚨 2. Reglas Críticas e Inviolables

1. **Enlace Oficial Único:**  
   NUNCA reemplazar la URL de GitHub Pages por túneles temporales (Cloudflare, ngrok, localip, etc.) en el botón de compartir, en el modal de código QR (`#qr-modal`) ni en el código.
2. **Sincronización MD5 de los 3 Archivos HTML:**  
   Siempre que se edite `index.html`, los siguientes 3 archivos deben actualizarse y mantener **exactamente el mismo hash MD5**:
   * `C:\Users\Lenovo\Documents\Mi dashboard\index.html`
   * `C:\Users\Lenovo\Documents\Mi dashboard\dashboard.html`
   * `C:\Users\Lenovo\Documents\salesland-dashboard-web\index.html`
3. **Despliegue Inmediato:**  
   Cada cambio debe guardarse, confirmarse y enviarse inmediatamente a GitHub:
   ```bash
   cd "C:\Users\Lenovo\Documents\salesland-dashboard-web"
   git add .
   git commit -m "feat/fix: descripción del cambio"
   git push origin main
   ```
4. **Archivo de Gran Tamaño (51 MB):**  
   `index.html` contiene incrustados los datos históricos y registros de ventas en variables JavaScript (`data_retail.json` y `data_retail_p2.json`). Evitar sobreescribir el archivo completo ciegamente; usar scripts de sustitución precisa en Python o Node.js.

---

## 🛡️ 3. Sistema de Seguridad y Roles (RBAC)

El dashboard cuenta con un control de acceso de dos niveles:
* **Perfil por Defecto (Supervisores):**
  * `<body class="role-supervisor">` desde el HTML estático.
  * Los supervisores tienen **Acceso Único de Solo Lectura**.
  * **Elementos Ocultos para Supervisores (`display: none !important`):**
    * Botón de código QR móvil (`#btn-mobile-qr`).
    * Botón y modal de cambio de contraseñas (`#btn-security-settings`).
    * Botón y modal de Gestión de Usuarios y Permisos (`#btn-open-user-mgmt`, `#btn-open-mgmt-from-role`).
    * Todo lo relacionado con **Facturación** (columnas `.col-facturacion`, tarjetas ribbon `.facturacion-stat`, pills `[data-mode="facturacion"]`, montos en tarjetas de vendedores `.seller-card-facturacion`, facturación en modal de vendedor, precios en tablas y tooltips de colones).
    * Botones administrativos (`#btn-sync-excels`, `#btn-edit-target`, `#btn-upload`).
    * Pestaña comparativa entre supervisores (`tab-supervisores`).
* **Perfil Administrador:**
  * Acceso total corporativo mediante contraseña maestra única protegida por SHA-256 (`Salesland2026*`).
  * No mostrar pistas visibles de contraseñas por defecto en modales ni formularios.
  * Habilita gestión de metas, actualización de Excels, cambio de credenciales y facturación comercial completa.

---

## 📊 4. Estructura de Pestañas y Vistas

1. **Tab 1: Comparativa Mensual de Servicios (MoM)**
   * Gráfico de barras MoM comparando Mes Actual vs Mes Anterior.
   * *Desglose Analítico por Servicio Vendido:* Tabla con Anterior, Actual, Meta, % Cumplimiento, Proyección, Variación MoM y Facturación (visible solo para admin). Subdesglose desplegable para la familia Pospago (Línea Nueva, Portabilidad, Migración).
2. **Tab 2: Campo Visual de Vendedores**
   * Gráfico horizontal con podio metálico (oro, plata, bronce).
   * Tarjetas ejecutivas individuales de vendedores con avatar, iniciales, ventas, meta, cumplimiento y efectividad.
   * Modal detallado de asesor al hacer clic con desglose de servicios y tabla de transacciones.
3. **Tab 3: Rendimiento por Supervisores y PDVs**
   * Gráficos horizontales con ribbons de micro-KPIs.
   * Clasificación por canales y tiendas.
4. **Tab 4: Provincias & Territorio**
   * Mapa tecnológico vectorial SVG de Costa Rica con paleta coroplética Twilight-Cyan de 7 niveles.
   * Pines con corona dorada identificando a la provincia líder.
   * Tarjetas laterales interactivas por provincia y ranking de cantones.
5. **Tab 5: Explorador de Transacciones (Data Grid)**
   * Tabla maestra de auditoría con buscador en tiempo real, filtros avanzados y paginación.

---

## 🔄 5. Flujo de Datos y Actualización (ETL)

* **Archivos Fuente (Excel):**
  * `Dashboard HTML RETAIL .xlsx` (Retail P1 Pospago)
  * `Dashboard HTML PREPAGO.xlsx` (Retail P1 Prepago)
  * `RETAIL P2.xlsx` (Retail P2 Pospago y Prepago)
* **Script de Procesamiento:**
  ```bash
  python actualizar_datos.py
  ```
  Extrae los registros, normaliza provincias, limpia fechas/nombres, genera los archivos `data_retail.json` y `data_retail_p2.json` e inyecta la data directamente en `index.html`.

---

## 💻 6. Comandos de Desarrollo Local

* **Iniciar Servidor Local (puerto 8080):**
  ```bash
  node server.js
  ```
* **Acceso Local:**
  `http://127.0.0.1:8080/index.html`
* **Verificar Hash MD5 en PowerShell:**
  ```powershell
  Get-FileHash 'C:\Users\Lenovo\Documents\Mi dashboard\index.html', 'C:\Users\Lenovo\Documents\Mi dashboard\dashboard.html', 'C:\Users\Lenovo\Documents\salesland-dashboard-web\index.html' -Algorithm MD5 | Format-Table
  ```
* **Desplegar a GitHub:**
  ```bash
  cd "C:\Users\Lenovo\Documents\salesland-dashboard-web"
  git add index.html CLAUDE.md
  git commit -m "feat: actualizar dashboard y directivas para Claude"
  git push origin main
  ```
