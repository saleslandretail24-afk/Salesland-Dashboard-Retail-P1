# Salesland Dashboard Retail P1 - Directivas del Proyecto

Este documento establece las directivas permanentes para el desarrollo, despliegue y mantenimiento del proyecto.

---

## 1. Enlace Oficial Permanente de Compartición
* **Enlace Público Único:**  
  `https://saleslandretail24-afk.github.io/Salesland-Dashboard-Retail-P1/index.html`
* **REGLA ESTRICTA:**  
  **NUNCA** cambiar este enlace por túneles temporales (Cloudflare, ngrok, localip, etc.) en el botón de compartir, en el modal de código QR (`#qr-modal`), ni en ninguna parte del código a menos que el usuario lo solicite expresamente.

---

## 2. Flujo de Guardado y Despliegue en GitHub
* **Despliegue Inmediato:**  
  Siempre que se realice una modificación, ajuste o mejora en el código, los cambios **DEBEN** ser guardados, confirmados (`git commit`) y enviados inmediatamente (`git push origin main`) al repositorio remoto en GitHub:  
  `https://github.com/saleslandretail24-afk/Salesland-Dashboard-Retail-P1.git`
* **Configuración de Autenticación Git:**  
  El repositorio local en `C:\Users\Lenovo\Documents\salesland-dashboard-web` está configurado con autenticación segura y `credential.helper=""` para garantizar que `git push origin main` se ejecute de manera autónoma sin bloquearse por prompts de GUI.

---

## 3. Sincronización de Archivos del Proyecto
Los siguientes tres archivos **deben mantenerse en idéntico contenido y hash MD5**:
1. `C:\Users\Lenovo\Documents\Mi dashboard\index.html`
2. `C:\Users\Lenovo\Documents\Mi dashboard\dashboard.html`
3. `C:\Users\Lenovo\Documents\salesland-dashboard-web\index.html`

---

## 4. Estado de Metas y Parámetros Comerciales
* **Metas de Octubre 2026 (Retail P1):** Total 7,806 instalaciones
  * Prepago: 5,450
  * Porta Prepago: 1,000
  * Pospago: 1,296
  * Gpon: 36
  * DTH: 12
  * IFI: 12
* **Metas de Septiembre 2026 (Retail P1):**
  * Conservadas intactas históricamente (DTH 24, IFI no aplica).
* **Filtros:**
  * Meses ordenados cronológicamente de Enero a Diciembre (Octubre por defecto).
  * Supervisores ordenados alfabéticamente de la A a la Z.

---

## 5. Diseño y Visualización
* **Pestaña 1 (MoM & Servicios):** Comparativa Visual MoM compacta (~35%) y Desglose Analítico por Servicio amplio (~65%). Columna renombrada a `Meta`.
* **Pestaña 2 (Top Vendedores):** Ranking visual con podio metálico, filtros por métrica (`Ventas`, `Facturación`, `Efectividad`) y vista de `Top 10 / 15 / 20`.
* **Pestaña 3 (Supervisores & PDVs):** Gráficos de barras horizontales con ribbons de micro-KPIs ejecutivos, podio y selectores métricos (`Ventas`, `Efectividad %`, `Facturación`).
