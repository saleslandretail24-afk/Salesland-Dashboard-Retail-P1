# GEMINI.md — Salesland Dashboard Retail P1

Este documento establece las directivas oficiales, la arquitectura técnica, las reglas de seguridad y el contexto operativo completo para trabajar en el proyecto **Salesland Dashboard Retail P1** utilizando **Google Gemini** (Gemini en Google Antigravity, Gemini Code Assist, Google AI Studio o Gemini CLI).

---

## 📌 1. Información General del Proyecto

* **Nombre del Proyecto:** Salesland Retail P1 - Panel Gerencial de Rendimiento Comercial
* **Organización:** Salesland Costa Rica / Telecomunicaciones Retail
* **Repositorio Oficial de GitHub:**  
  [https://github.com/saleslandretail24-afk/Salesland-Dashboard-Retail-P1](https://github.com/saleslandretail24-afk/Salesland-Dashboard-Retail-P1)
* **URL de Producción (GitHub Pages):**  
  `https://saleslandretail24-afk.github.io/Salesland-Dashboard-Retail-P1/index.html`
* **Arquitectura de Software:**
  * **Frontend:** Single Page Application (SPA) construida en Vanilla HTML5, CSS3 moderno (Custom Properties, Glassmorphism, Micro-animaciones) y JavaScript nativo ES6+.
  * **Librerías externas:** Chart.js (CDN), Lucide/SVG Icons integrados inline.
  * **Visualización Geográfica:** Mapa coroplético interactivo de Costa Rica en SVG vectorial nativo de 7 niveles cromáticos Twilight-Cyan.
  * **Dependencias de build:** Ninguna. No requiere Webpack, Vite, Node bundlers ni transpiladores. Se sirve como archivo HTML puro y autónomo.

---

## 🚨 2. Reglas Críticas e Inviolables para Gemini

1. **URL de Producción Inmutable:**  
   La URL oficial y definitiva del dashboard es **exclusivamente la de GitHub Pages**:  
   `https://saleslandretail24-afk.github.io/Salesland-Dashboard-Retail-P1/index.html`  
   **NUNCA** reemplazar esta URL por túneles temporales (como Cloudflare Tunnel, ngrok, localip, etc.) en el botón de compartir, en el modal de código QR (`#qr-modal`) ni en el código fuente.

2. **Protocolo de Sincronización Tripartita de Archivos (MD5 Obligatorio):**  
   Cualquier modificación a `index.html` debe replicarse en las 3 ubicaciones locales, asegurando que tengan **exactamente el mismo hash MD5**:
   * `C:\Users\Lenovo\Documents\Mi dashboard\index.html`
   * `C:\Users\Lenovo\Documents\Mi dashboard\dashboard.html`
   * `C:\Users\Lenovo\Documents\salesland-dashboard-web\index.html`

3. **Despliegue Inmediato a GitHub:**  
   Todo cambio completado debe registrarse y desplegarse inmediatamente al repositorio remoto:
   ```bash
   cd "C:\Users\Lenovo\Documents\salesland-dashboard-web"
   git add index.html GEMINI.md
   git commit -m "feat/fix: descripción detallada del cambio"
   git push origin main
   ```

4. **Tratamiento del Archivo de Gran Tamaño (51 MB):**  
   El archivo `index.html` contiene incrustados todos los registros históricos en arrays de JavaScript (`data_retail.json` y `data_retail_p2.json`).  
   * **No reescribir el archivo completo a ciegas.**  
   * Para editar HTML, CSS o funciones JavaScript, utilizar siempre herramientas de sustitución localizada (como `replace_file_content` o scripts quirúrgicos en Python/Node.js) para preservar intacta la base de datos embebida.

---

## 🛡️ 3. Sistema de Seguridad y Roles (RBAC)

El panel opera con un estricto sistema de control de acceso basado en roles (*Role-Based Access Control*):

### A. Perfil Supervisor (Modo por Defecto / Solo Lectura)
* El elemento `<body>` cuenta con la clase estática `role-supervisor` (`<body class="role-supervisor">`).
* **Elementos Ocultos y Protegidos para Supervisores (`display: none !important`):**
  * **Celular (QR):** Botón `#btn-mobile-qr` oculto.
  * **Seguridad y Contraseñas:** Botón `#btn-security-settings` y modal de cambio de clave ocultos. Solo el administrador puede modificar accesos.
  * **Gestión de Usuarios y Permisos:** Botones `#btn-open-user-mgmt` y `#btn-open-mgmt-from-role` completamente ocultos.
  * **Módulo de Facturación Comercial:** Oculto al 100%. Los supervisores no pueden ver datos de facturación:
    * Columnas `.col-facturacion` en tablas.
    * Tarjetas de facturación `.facturacion-stat` y tabs `[data-mode="facturacion"]`.
    * Montos de factura en las tarjetas de vendedores (`.seller-card-facturacion`).
    * Métricas de facturación en el modal de detalle del asesor.
    * Columna de facturación en el Desglose Analítico por Servicio.
  * **Herramientas Administrativas:** Botones de gestión de cuotas (`#btn-edit-target`), actualización de Excels (`#btn-sync-excels`) y carga manual (`#btn-upload`).
  * **Pestaña de Comparativa entre Supervisores:** Pestaña `tab-supervisores` oculta.
  * **Filtro de Supervisor:** Bloqueado automáticamente al supervisor asignado al iniciar sesión.

### B. Perfil Administrador (Acceso Total Corporativo)
* Desbloqueo mediante contraseña maestra única protegida por algoritmo criptográfico SHA-256 (`Salesland2026*`).
* **Sin pistas de contraseñas por defecto:** No mostrar contraseñas sugeridas en textos de ayuda ni en campos de formularios.
* Habilita:
  * Visualización completa de facturación en Colones (₡).
  * Edición de metas por servicio y mes.
  * Gestión de usuarios y permisos.
  * Sincronización y reprocesamiento de Excels.
  * Comparativas globales de todos los supervisores y canales.

---

## 📊 4. Componentes y Arquitectura de la Interfaz

### 1. Rejilla de 5 Tarjetas de KPIs Ejecutivos (`.kpi-row-salesland`)
Diseñadas con acabado *glassmorphism*, iluminación ambiental (*ambient wash*), borde superior radiante y micro-interacciones:
* **Card 1 (Meta Mensual):** Total de cuota asignada (`#kpi-meta-num`), subtítulo (`#kpi-meta-subtext`), icono de diana/target y tag `🎯 Cuota Base`.
* **Card 2 (Cumplimiento):** Porcentaje sobre meta (`#kpi-cump-num`), subtítulo (`#kpi-cump-subtext`), icono de trofeo/verificación y **barra de progreso animada dinámica (`#kpi-cump-bar`)** que cambia de color automáticamente (Verde $\ge 60\%$, Ámbar $40\text{--}60\%$, Rojo $< 40\%$).
* **Card 3 (Proyección Cierre):** Estimación por ritmo diario run-rate (`#kpi-proy-num`), subtítulo (`#kpi-proy-subtext`), icono de tendencia ascendente y tag `⚡ Estimación Run-Rate`.
* **Card 4 (Vs Año Anterior - YoY):** Ventas del mismo mes del año previo (`#kpi-yoy-val`), cápsula de variación (`#kpi-yoy-badge`) y porcentaje con flecha (`#kpi-yoy-pct`).
* **Card 5 (Vs Mes Anterior - MoM):** Ventas del mes calendario inmediatamente anterior (`#kpi-mom-val`), cápsula de variación (`#kpi-mom-badge`) y porcentaje con flecha (`#kpi-mom-pct`).

### 2. Pestañas de Análisis Comercial
1. **📊 Comparativa Mensual de Servicios (MoM):**
   * Gráfico de barras comparativo (Mes Actual vs Mes Anterior).
   * Desglose Analítico por Servicio con acordeón interactivo para Pospago (Portabilidad, Línea Nueva, Migración).
2. **👤 Campo Visual: Ventas por Vendedores:**
   * Gráfico horizontal con podio olímpico metálico (Oro, Plata, Bronce).
   * Tarjetas ejecutivas con avatares, métricas de efectividad y modal interactivo por asesor.
3. **👥 Rendimiento por Supervisores:**
   * Comparativa de cuotas y ventas consolidadas por equipo y canales de retail.
4. **🗺️ Provincias & Puntos de Venta:**
   * Mapa interactivo vectorial SVG de Costa Rica con selector de provincias, tooltip enriquecido y corona de provincia líder.
5. **📋 Explorador de Transacciones (Data Grid):**
   * Auditoría de ventas individuales con paginación, filtros multicriterio y búsqueda instantánea.

---

## 🔄 5. Flujo de Datos y Pipeline ETL

* **Fuentes de Datos:**
  * `Dashboard HTML RETAIL .xlsx` (Retail P1 - Pospago)
  * `Dashboard HTML PREPAGO.xlsx` (Retail P1 - Prepago)
  * `RETAIL P2.xlsx` (Retail P2 - Pospago y Prepago)
* **Script de Transformación y Carga:**
  ```bash
  python actualizar_datos.py
  ```
  Este script procesa los libros de Excel, normaliza nombres de tiendas y provincias, calcula agregaciones e inyecta la base de datos directamente en las variables de `index.html`.

---

## 🛠️ 6. Guía Rápida para Trabajar con Gemini

### En Google Antigravity / Gemini Code Assist
1. **Espacio de Trabajo:**  
   Asegúrate de que la carpeta de trabajo activa sea:  
   `C:\Users\Lenovo\Documents\Mi dashboard` o `C:\Users\Lenovo\Documents\salesland-dashboard-web`.
2. **Verificar Estado del Servidor Local:**
   ```bash
   node server.js
   ```
   Abre el navegador en `http://127.0.0.1:8080/index.html`.
3. **Verificación de Integridad:**
   ```powershell
   Get-FileHash 'C:\Users\Lenovo\Documents\Mi dashboard\index.html', 'C:\Users\Lenovo\Documents\Mi dashboard\dashboard.html', 'C:\Users\Lenovo\Documents\salesland-dashboard-web\index.html' -Algorithm MD5 | Format-Table
   ```
4. **Comandos de Git y Despliegue:**
   ```bash
   cd "C:\Users\Lenovo\Documents\salesland-dashboard-web"
   git add .
   git commit -m "feat: [descripción de la mejora]"
   git push origin main
   ```

### En Google AI Studio (aistudio.google.com)
* Gracias a la ventana de contexto de **hasta 2 Millones de Tokens** de Gemini (Gemini 1.5 Pro / Gemini 2.0 / Gemini 3.8), puedes cargar este archivo `GEMINI.md` en la sección **System Instructions** y hacer consultas analíticas complejas o pedir propuestas de diseño avanzadas.
