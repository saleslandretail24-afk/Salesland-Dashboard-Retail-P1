# 📦 Guía de Migración y Prompt Maestro — Salesland Dashboard Retail (P1 & P2)

Este documento contiene:
1. **Cómo instalar y ejecutar este mismo proyecto en otra computadora en 5 minutos** (clonando desde GitHub y copiando los Excels).
2. **El Prompt Maestro (Blueprint Técnico Completo en Markdown)** para pegar en cualquier asistente de IA (Google Antigravity / Gemini, Claude Code, Cursor, ChatGPT) si deseas recrear o generar un dashboard con esta misma arquitectura desde cero en otra computadora.

---

## 🖥️ PARTE 1: Cómo llevar y ejecutar este proyecto exacto en otra computadora

### 1. Requisitos previos en la nueva computadora
Instala las siguientes herramientas gratuitas:
* **Node.js (v18 o superior):** [https://nodejs.org/](https://nodejs.org/)
* **Python (v3.10 o superior):** [https://www.python.org/](https://www.python.org/) (marcar *"Add Python to PATH"* al instalar).
* **Git para Windows:** [https://git-scm.com/](https://git-scm.com/)
* **Librerías de Python para procesar los Excels:**
  ```powershell
  pip install pandas openpyxl
  ```

### 2. Clonar el proyecto desde GitHub
Abre **PowerShell** en la otra computadora y ejecuta:
```powershell
cd "$HOME\Documents"
git clone https://github.com/saleslandretail24-afk/Salesland-Dashboard-Retail-P1.git "salesland-dashboard-web"
```

### 3. Crear la carpeta de trabajo local (`Mi dashboard`)
Si deseas mantener la misma estructura de doble carpeta que tienes en esta PC:
```powershell
New-Item -ItemType Directory -Force -Path "$HOME\Documents\Mi dashboard"
Copy-Item "$HOME\Documents\salesland-dashboard-web\*" "$HOME\Documents\Mi dashboard\" -Recurse -Force
Copy-Item "$HOME\Documents\Mi dashboard\index.html" "$HOME\Documents\Mi dashboard\dashboard.html" -Force
```

### 4. Copiar los 3 archivos Excel fuente
Copia tus 3 archivos Excel maestros dentro de `$HOME\Documents\Mi dashboard\`:
1. `Dashboard HTML RETAIL .xlsx` *(Ventas Pospago / Hogar Retail P1)*
2. `Dashboard HTML PREPAGO.xlsx` *(Ventas Prepago Retail P1)*
3. `RETAIL P2.xlsx` *(Ventas Pospago y Prepago Retail P2)*

> **Nota:** Si las rutas en `actualizar_datos.py` apuntan a `C:\Users\Lenovo\Documents\...` y tu usuario de Windows en la otra PC tiene otro nombre, reemplaza `C:\Users\Lenovo` por tu nuevo usuario o usa `os.path.expanduser('~')`.

### 5. Comandos de uso diario en la otra computadora
* **Iniciar servidor con auto-actualización en vivo (puerto 8080):**
  ```powershell
  cd "$HOME\Documents\Mi dashboard"
  node server.js
  ```
  Luego abre en el navegador: `http://127.0.0.1:8080/index.html`
* **Actualizar datos manualmente desde los Excels y publicar en GitHub Pages:**
  ```powershell
  cd "$HOME\Documents\Mi dashboard"
  python actualizar_datos.py
  ```

---

## 🤖 PARTE 2: Prompt Maestro para Recrear el Dashboard con IA en Otra Computadora

Copia el siguiente bloque completo y pégalo en tu agente de IA (**Antigravity / Gemini / Claude / Cursor**) cuando quieras construir o replicar este sistema desde cero o para otra operación comercial:

````markdown
# PROMPT MAESTRO: Construcción de Panel Gerencial Ejecutivo BI (Arquitectura Salesland Retail P1/P2)

Actúa como un Arquitecto Senior de Business Intelligence y Desarrollador Full-Stack Especialista en Visualización de Datos. Necesito que construyas un sistema completo de Dashboard Gerencial de Rendimiento Comercial autónomo (Single-File SPA + Servidor Local con Live Reload + Pipeline ETL de Excel a HTML/JSON).

---

## 1. ARQUITECTURA GENERAL DEL SISTEMA

El proyecto no debe usar bundlers pesados (ni Webpack, ni Vite, ni React compilado) para garantizar portabilidad total. Debe componerse de 3 piezas fundamentales:

1. **`index.html` (y espejo idéntico `dashboard.html`):**
   - Aplicación Single Page Application (SPA) 100% autocontenida en **Vanilla HTML5 + CSS3 moderno (Variables CSS, Glassmorphism, Dark/Light Theme) + JavaScript ES6+ nativo**.
   - Librerías vía CDN: **Chart.js** (`chart.umd.min.js`), **SheetJS (`xlsx.full.min.js`)** para exportación e importación Excel, y **Google Fonts** (`Plus Jakarta Sans`, `Inter`, `JetBrains Mono`).
   - Datos embebidos directamente en el HTML dentro de `<script>`:
     - `window.RAW_DATASET = [...]` (Proyecto P1)
     - `window.RAW_DATASET_P2 = [...]` (Proyecto P2)
     - `window.LAST_UPDATE_STR = "DD/MM/YYYY HH:MM"`
   - Funciona tanto abriéndolo con doble clic (`file://`), como servido desde `node server.js` (`http://127.0.0.1:8080`) o publicado estáticamente en **GitHub Pages**.

2. **`actualizar_datos.py` (Pipeline ETL en Python):**
   - Lee múltiples libros de Excel (`Dashboard HTML RETAIL .xlsx`, `Dashboard HTML PREPAGO.xlsx`, `RETAIL P2.xlsx`) usando `pandas` y `openpyxl`.
   - Limpia y normaliza cadenas (supervisores, vendedores, tiendas/PDVs, cantones, 7 provincias de Costa Rica, canales y familias de servicio: `Prepago`, `Porta Prepago`, `Pospago` [con sub-tipos `Línea Nueva`, `Portabilidad`, `Migración`], `Gpon`, `DTH`, `IFI`).
   - Exporta respaldos JSON (`data_retail.json` y `data_retail_p2.json`) e inyecta los arreglos JSON directamente en `index.html`, copiando luego el archivo con `shutil.copy2` a `dashboard.html` y al repositorio de GitHub Pages para conservar **exactamente el mismo hash MD5** en las 3 copias.

3. **`server.js` (Servidor Node.js Zero-Dependencies):**
   - Servidor HTTP en el puerto `8080` sin dependencias externas (`http`, `fs`, `path`, `child_process`).
   - Monitorea (`fs.watchFile`) cambios en los archivos `.xlsx` con debounce de 2 segundos y ejecuta automáticamente `python actualizar_datos.py`.
   - Expone endpoints:
     - `GET /events`: Server-Sent Events (SSE) que transmite estados `updating`, `reload` y `error` al navegador para recargar el dashboard automáticamente cuando se guarda un Excel.
     - `GET /api/excel-status`: Devuelve `{ isUpdating, files: [{ name, exists, mtime, sizeMB }] }`.
     - `POST /api/sync-excels`: Dispara bajo demanda la ejecución de `python actualizar_datos.py`.

---

## 2. ESQUEMA DE DATOS POR REGISTRO (`window.RAW_DATASET`)

Cada fila de venta inyectada en `window.RAW_DATASET` y `window.RAW_DATASET_P2` sigue este contrato JSON:

```json
{
  "fecha": "2026-10-15",
  "anio": "2026",
  "mes": "Octubre",
  "dia": "15",
  "vendedor": "NOMBRE DEL VENDEDOR",
  "supervisor": "NOMBRE DEL SUPERVISOR",
  "pdv": "TIENDA / PUNTO DE VENTA",
  "canal": "CADENA COMERCIAL",
  "canton": "CANTON",
  "provincia": "SAN JOSE",
  "servicio": "Pospago",
  "tipo_Activacion": "Portabilidad",
  "precio": 16500,
  "cantidad": 1
}
```

---

## 3. SEGURIDAD, AUTENTICACIÓN Y CONTROL DE ROLES (RBAC)

Implementa el módulo `window.SaleslandSecurity` y `window.SaleslandRBAC` con dos perfiles estrictos:

### A. Gateway de Inicio de Sesión y Tokens Persistentes ("Recordarme por 7 días")
- Al abrir el sistema sin sesión activa, muestra una pantalla de bloqueo (`#auth-gateway-overlay`) y bloquea el contenedor principal (`.dashboard-wrapper.auth-locked`).
- **Dos modos de acceso en el Gateway:**
  1. **Modo Supervisor:** Solicita selección de nombre de Supervisor y PIN de 4 dígitos (validado contra catálogo de PINs por supervisor + soporte para PIN personalizado en `localStorage`).
  2. **Modo Administrador:** Solicita contraseña maestra verificada mediante hash criptográfico **SHA-256** (`Web Crypto API` con fallback determinista para contexto `file://`). Nunca mostrar la contraseña en texto plano ni en pistas de UI.
- **Tokens de Sesión y Recordatorio:**
  - `salesland_auth_remember_token` (Administrador) y `salesland_supervisor_token` (Supervisor) almacenados en `localStorage` como JSON `{ hash, expires }` con expiración de 7 días (`7 * 24 * 60 * 60 * 1000` ms) cuando el checkbox "Recordarme" está activo, además de bandera de sesión activa en `sessionStorage`.
  - Función `lockDashboard()` para cerrar sesión limpiando tanto `localStorage` como `sessionStorage` y regresando a modo Supervisor restringido.

### B. Reglas de Visibilidad RBAC (`<body class="role-supervisor">` por defecto)
- **En Modo Supervisor (Solo Lectura):**
  - Bloquea el filtro `#filter-supervisor` al nombre del supervisor autenticado.
  - **Oculta al 100% la Facturación Comercial (`₡`)** tanto en la interfaz visual (CSS `display: none !important` en `.col-facturacion`, `.facturacion-stat`, `.seller-card-facturacion`, `[data-mode="facturacion"]`, opción `facturacion` en `#seller-sort-select`) como en **todas las exportaciones a Excel/CSV** (Vendedores, Transacciones, Cantones y Tiendas/PDVs).
  - Si un Administrador tenía activo el modo `facturacion` en gráficos o tablas y cambia a rol Supervisor, `applyRolePermissions()` restablece automáticamente los modos a `ventas` / `fecha`.
  - Oculta botones administrativos: `#btn-mobile-qr`, `#btn-security-settings`, `#btn-open-user-mgmt`, `#btn-edit-target`, `#btn-sync-excels`, `#btn-upload` y la pestaña comparativa de supervisores (`tab-supervisores`).
- **En Modo Administrador (`<body class="role-admin">`):**
  - Acceso completo a facturación en Colones (`₡`), edición de metas mensuales por servicio y por vendedor, sincronización de Excels, gestión de usuarios/PINs, cambio de contraseña maestra y comparativa global entre supervisores.

---

## 4. DISEÑO VISUAL Y SISTEMA DE COMPONENTES (UI/UX)

- **Estética:** Executive HUD / Glassmorphism corporativo con soporte para **Modo Claro y Modo Oscuro** (`data-theme="dark"`), acentos en azul cian (`#0284c7` / `#38bdf8`), esmeralda (`#10b981`), ámbar (`#f59e0b`) y rojo coral (`#ef4444`).
- **Barra Superior (Header & Filtros Globales):**
  - Selector de Proyecto en tiempo real (`Retail P1` vs `Retail P2`) con persistencia en `localStorage`.
  - Filtros globales reactivos: **Año**, **Mes**, **Día**, **Supervisor**, **Provincia**, **Canal**, **Servicio** y botón de limpieza rápida.
  - Botones de acción según rol: Sincronizar Excels, Configurar Metas, Usuarios/Roles, Código QR Móvil (apuntando exclusivamente a la URL oficial de GitHub Pages) y Tema Claro/Oscuro.

### Rejilla de 5 Tarjetas de KPIs Ejecutivos (`.kpi-row-salesland`)
Cada tarjeta incluye micro-gráficos tipo ecualizador (`eq-bar`), cápsulas de estado y animaciones suaves:
1. **Meta Mensual (`#kpi-meta-num`):** Suma de la cuota del mes/servicio activo (o meta proporcional de equipo cuando se filtra un supervisor).
2. **Cumplimiento (`#kpi-cump-num`):** `(Ventas Actuales / Meta) * 100` con barra de progreso dinámica (`#kpi-cump-bar`) que cambia de color según semáforo (`>= 60%` verde, `40-59%` ámbar, `< 40%` rojo) y cálculo de brecha (`Faltan X uds` o `Superada por +X uds`).
3. **Proyección de Cierre (`#kpi-proy-num`):** Estimación *Run-Rate* lineal: `Math.round((Ventas Actuales / Días Activos Transcurridos del Mes en App.data) * Días Totales del Mes)`.
4. **Vs Año Anterior - YoY (`#kpi-yoy-val`):** Comparativa contra el mismo mes del año anterior con badge de variación porcentual y diferencia neta.
5. **Vs Mes Anterior - MoM (`#kpi-mom-val`):** Comparativa contra el mes calendario inmediatamente anterior (manejando cruce Enero -> Diciembre del año previo).

---

## 5. LAS 6 PESTAÑAS ANALÍTICAS DEL DASHBOARD

1. **📊 Tab 1 — Comparativa Mensual de Servicios (MoM):**
   - Gráfico de barras agrupadas en Chart.js comparando Mes Actual vs Mes Anterior por servicio.
   - Tabla de *Desglose Analítico por Servicio Vendido* con columnas: Servicio, Mes Anterior, Mes Actual, Meta, % Cumplimiento (con barra), Proyección Run-Rate, Variación % MoM y Facturación (solo Admin).
   - **Acordeón interactivo** en las filas de `Pospago` (`Línea Nueva`, `Portabilidad`, `Migración`) y `Servicios Hogar` (`Gpon`, `DTH`, `IFI`).

2. **👤 Tab 2 — Campo Visual: Ventas por Vendedores:**
   - **Podio Olímpico Top 3** (Oro, Plata, Bronce) con medallas, avatares y métricas destacadas.
   - Gráfico horizontal Top 15 vendedores conmutable entre Unidades y Facturación.
   - Cuadrícula de tarjetas ejecutivas por vendedor con buscador instantáneo, filtro de estado de meta, ordenamiento y barra de ritmo esperado (*Ritmo al día X*).
   - **Modal de Ficha Individual del Vendedor:** Al hacer clic en un vendedor, abre su perfil con KPIs propios, desglose por servicio, listado de transacciones y botón de exportación individual a Excel.

3. **👥 Tab 3 — Rendimiento por Supervisores y Tiendas (PDVs):**
   - Ribbons de micro-KPIs de liderazgo.
   - Gráficos horizontales comparativos por Supervisor y por Punto de Venta (PDV).
   - Tabla de cumplimiento de metas de equipo por supervisor.

4. **🗺️ Tab 4 — Provincias & Territorio (Mapa Coroplético SVG):**
   - Mapa vectorial interactivo SVG nativo de las **7 provincias de Costa Rica** con escala coroplética *Twilight-Cyan* de 7 niveles según volumen de ventas.
   - Pin con corona dorada sobre la provincia líder, tooltips flotantes enriquecidos y clic en provincia para filtrar territorio.
   - Tablas clasificatorias de **Provincias**, **Cantones** y **Puntos de Venta (PDVs)** con exportación a Excel protegida por RBAC.

5. **📋 Tab 5 — Explorador de Transacciones (Data Grid):**
   - Tabla maestra paginada con búsqueda en tiempo real, ordenamiento por columnas y exportación completa a Excel (`.xlsx`) y CSV (`.csv`) respetando las reglas RBAC.

6. **📄 Tab 6 — Reporte Ejecutivo (Vista de Impresión A4 / PDF y Excel):**
   - Documento gerencial auto-generado con resumen ejecutivo narrativo, semáforos de riesgo comercial, KPIs consolidados, tabla de desempeño por línea de negocio y matriz territorial por provincia.
   - Incluye botones para **Imprimir / Guardar PDF** (con `@media print` optimizado) y **Exportar Reporte Ejecutivo a Excel**.
````
