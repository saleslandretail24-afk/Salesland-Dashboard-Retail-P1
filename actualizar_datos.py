import openpyxl, re, json, unicodedata, sys, os
from collections import Counter

retail_path = r'C:\Users\Lenovo\Documents\Mi dashboard\Dashboard HTML RETAIL .xlsx'
prepago_path = r'C:\Users\Lenovo\Documents\Mi dashboard\Dashboard HTML PREPAGO.xlsx'
index_path = r'C:\Users\Lenovo\Documents\Mi dashboard\index.html'
dash_path = r'C:\Users\Lenovo\Documents\Mi dashboard\dashboard.html'
json_path = r'C:\Users\Lenovo\Documents\Mi dashboard\data_retail.json'

def strip_accents(text):
    text = unicodedata.normalize('NFD', str(text or ''))
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text.lower().strip()

def clean_name(name):
    s = strip_accents(name)
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def clean_price(val):
    if not val: return 0
    s = str(val).replace('₡', '').replace('.', '').replace(',', '').strip()
    m = re.search(r'(\d+)', s)
    if m:
        try:
            num = int(m.group(1))
            if num > 1000000: return 0
            return num
        except: return 0
    return 0

def clean_str_val(val):
    if val is None: return ''
    s = str(val).strip()
    if s.endswith('.0'): s = s[:-2]
    if s in ['-', 'N/A', 'NA', 'None', 'null', 'nan']: return ''
    return s

meses_validos = {'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'}
n_to_m = {'01':'Enero','02':'Febrero','03':'Marzo','04':'Abril','05':'Mayo','06':'Junio','07':'Julio','08':'Agosto','09':'Septiembre','10':'Octubre','11':'Noviembre','12':'Diciembre'}

def normalize_retail_service(raw_val):
    s = str(raw_val or '').strip().lower()
    if 'fonatel' in s or 'ifi' in s:
        return 'IFI'
    elif 'portabilidad' in s:
        return 'Portabilidad Postpago'
    elif 'migraci' in s:
        return 'Migración Pospago'
    elif 'gpon' in s or 'fibra' in s:
        return 'Gpon'
    elif 'dth' in s:
        return 'DTH'
    elif 'postpago' in s or 'pospago' in s:
        return 'Pospago'
    return 'Pospago'

def normalize_provincia(p_raw):
    p = str(p_raw or '').strip()
    p_lower = strip_accents(p)
    if 'san jose' in p_lower: return 'San José'
    if 'alajuela' in p_lower: return 'Alajuela'
    if 'cartago' in p_lower: return 'Cartago'
    if 'heredia' in p_lower: return 'Heredia'
    if 'guanacaste' in p_lower or 'nicoya' in p_lower: return 'Guanacaste'
    if 'puntarenas' in p_lower: return 'Puntarenas'
    if 'limon' in p_lower: return 'Limón'
    return p if p else 'Sin Especificar'

print("--- 1. LOADING RETAIL EXCEL ---")
wb_retail = openpyxl.load_workbook(retail_path, read_only=True)
ws_retail = wb_retail['POSPAGO P1']

retail_records = []
retail_sellers = set()

for r in ws_retail.iter_rows(min_row=2, values_only=True):
    if not any(c is not None and str(c).strip() != '' for c in r[:16]): continue
    f = r[0]
    fecha_str = f.strftime('%Y-%m-%d') if hasattr(f, 'strftime') else str(f)[:10] if f else ''
    
    anio = r[1]
    try: anio = int(anio)
    except:
        if fecha_str and len(fecha_str) >= 4:
            try: anio = int(fecha_str[:4])
            except: anio = 2026
        else: anio = 2026
            
    mes = str(r[2]).strip() if r[2] else ''
    if mes.lower() not in meses_validos:
        if fecha_str and len(fecha_str) >= 7:
            m_num = fecha_str[5:7]
            mes = n_to_m.get(m_num, 'Sin Mes')
        else: mes = 'Sin Mes'
    else: mes = mes.capitalize()
        
    contrato = clean_str_val(r[4])
    id_tramite = clean_str_val(r[3])
    telefono = clean_str_val(r[15]) or clean_str_val(r[16])
    
    cliente = str(r[5]).strip() if r[5] else 'Cliente Final'
    cedula = clean_str_val(r[6])
    plan = str(r[7]).strip() if r[7] else 'Sin Plan'
    precio = clean_price(r[8])
    if precio == 0 and 'conexi' in plan.lower():
        if '1' in plan: precio = 11900
        elif '2' in plan: precio = 14200
        elif '3' in plan: precio = 17500
        
    canal = str(r[9]).strip() if r[9] else 'Otros'
    if canal in ['-', '', ' ']: canal = 'Otros'
    if 'avicam' in canal.lower(): canal = 'Avicam'
    elif 'cadena' in canal.lower(): canal = 'Cadenas'
    elif 'multi' in canal.lower(): canal = 'Multimarca'
    
    pdv = str(r[10]).strip() if r[10] else 'General'
    norm_tipo = normalize_retail_service(r[11])
    
    estado = str(r[12]).strip().upper() if r[12] else 'PENDIENTE'
    if not estado or estado in ['-', ' ']: estado = 'PENDIENTE'
    if 'VENTA' in estado: estado = 'VENTA'
    elif 'RECHAZ' in estado: estado = 'RECHAZADA'
    elif 'DUPLIC' in estado: estado = 'DUPLICADO'
    
    vendedor = str(r[13]).strip() if r[13] else 'Sin Asignar'
    if vendedor and vendedor != 'Sin Asignar':
        retail_sellers.add(vendedor)
        
    supervisor = str(r[14]).strip() if r[14] else 'Sin Supervisor'
    
    donante = str(r[17]).strip() if r[17] else 'N/A'
    if donante in ['-', '', 'Na', 'No Aplica', ' ']: donante = 'N/A'
    elif 'liberty' in donante.lower(): donante = 'Liberty'
    elif 'kolbi' in donante.lower() or 'kölbi' in donante.lower(): donante = 'Kölbi'
    
    provincia = normalize_provincia(r[21])
    canton = str(r[22]).strip() if r[22] else ''
    
    retail_records.append([fecha_str, anio, mes, cliente, cedula, plan, precio, canal, pdv, norm_tipo, estado, vendedor, supervisor, donante, provincia, canton, contrato, id_tramite, telefono])

wb_retail.close()
print(f"Retail records extracted: {len(retail_records)}")

# Seller Name Unification Mapping
retail_cleaned_map = {clean_name(r): r for r in retail_sellers}

EXPLICIT_MAP = {
    "Diego Alejandro Espinoza Tenorio": "Alejandro Espinoza",
    "Geysell Sayonara Espinoza Gonzalez": "Geysel Espinoza Gonzalez",
    "Roberth Aaron Ureña Flores": "Roberth Aron Ureña Flores",
    "Yanelys Dominguez Valdez": "Yanelis Dominguez Valdes",
    "Yanelys Berta Dominguez Valdez": "Yanelis Dominguez Valdes",
    "Carlos Alberto Guerrero Narvaez": "Carlos Guerrero Narvaez",
    "Carlos Alberti Guerrero Narvaez": "Carlos Guerrero Narvaez",
    "Keli Francini Valverde Mora": "Francini Valverde Mora",
    "Juan Pablo Castillo Zeledón": "Pablo Castillo Zeledon",
    "Juan Pablo Castillo Zeledon": "Pablo Castillo Zeledon",
    "Clelia Virginia Centeno Espinoza": "Clelia Centeno Espinoza",
    "Glen Francisco Vega Cordoba": "Glen Vega Cordoba",
    "Hillary Gutiérrez Campos": "Hillary Michelle Gutierrez Campos",
    "Keylor Javier Álvarez Guevara": "Keylor Alvarez Guevara",
    "Keylor Javier Alvarez Guevara": "Keylor Alvarez Guevara",
    "Johel Ramirez Obando": "Johel Gerardo Ramirez Obando",
    "Francisco Enriquez Briones": "Francisco Antonio Enriquez Briones",
    "Sol Fonseca Quirós": "Sol Maria Fonseca Quiros",
    "Janiff Rodríguez Bonilla": "Janiff Dahyan Rodriguez Bonilla",
    "Junior Porras Cisneros": "Junior Andrey Porras Cisneros",
    "Desire Martínez Chaves": "Desiree Martinez Chaves",
    "Naomy García Arguedas": "Naomy De Los Angeles Garcia Arguedas",
    "Adriana Cruz Cisneros": "Adriana Maria Cruz Cisneros",
    "Wendy Yanela Carrera Villarreal": "Wendy Yanela Carrera Villareal",
    "Saqueo Mártir Cabrera": "Saqueo Martir Cabrera Leiva",
    "Josue Alvardo Serrano": "Josue Alvarado Serrano",
    "Karol Bolaños Delgado": "Karol De Los Angeles Bolaños Delgado",
    "Michael Alexander Delgado Garcia": "Michael Delgado Garcia",
    "Carolina De Los Angeles Hernandez Soza": "Carolina Hernandez Soza",
    "Carolina Hernández Soza": "Carolina Hernandez Soza",
    "Sofía Campos Valerio": "Sofia Alejandra Campos Valerio",
    "Lidia Rebeca Garita Garro": "Rebeca Garita Garro",
    "Andrea De Los Angeles Garcia Ramirez": "Andrea Garcia Ramirez",
    "Andrea Umaña Villegas": "Andrea Melisa Umaña Villegas",
    "Sebastian Esteban Jimenez Garita": "Sebastián Jiménez Garita",
    "Jesus Eduardo Miranda Piñar": "Jesus Miranda Piñar",
    "Sochil Pamela Ovares Chacón": "Zoshil Pamela Ovares Chacon",
    "Yorleny De Los Angeles Vargas Rojas": "Yorleni De Los Angeles Vargas Rojas",
    "Carlos Flores Sánchez": "Carlos Enrique Flores Sanchez",
    "Victoria Ruiz Villalobos": "Marianne Victoria Ruiz Villalobos",
    "Seidy Cruz Céspedes": "Seidy Delfina Cruz Céspedes",
    "Seidy Delfina Cruz Cespedes": "Seidy Delfina Cruz Céspedes",
    "Andy Solano Mendez": "Andy Gabriel Solano Mendez",
    "Cristofer Alonso Vargas": "Cristopher Alonso Vargas",
    "Noilyn Alvarez Cascante": "Noylin Erlith Álvarez Cascante",
    "Sherryl Segura Solano": "Sheryll Segura Solano",
    "Yorlene De Los Ángeles García": "Yorlene De Los Angeles Garcia",
    "Angie Maria Jiménez Castillo": "Angie Maria Jimenez Castillo",
    "Eliette Nicole Rodríguez Arguedas": "Eliette Nicole Rodriguez Arguedas",
    "Gendry Alvarez Obando": "Gendry Álvarez Obando",
    "Kemsy Krisey Briones Jiménez": "Kemsy Krisey Briones Jimenez",
    "Pablo Alonso Chavarría Mendiola": "Pablo Alonso Chavarria Mendiola",
    "Daniela Dayana Zuñiga Rodriguez": "Daniela Dayana Zúñiga Rodriguez",
    "Keisy Daniela Chavarria Arroyo": "Keisy Daniela Chavarría Arroyo",
    "Yendry Paola Vargas Sandi": "Yendry Paola Vargas Sandí",
    "Yoselin Maria Duran Montero": "Yoselin María Duran Montero",
    "Evelyn Patricia Gonzalez Arrieta": "Evelyn Patricia González Arrieta",
    "Kimberly Fuentes González": "Kimberly Fuentes González",
    "Nicole María Seas Correa": "Nicole María Seas Correa",
    "Maria Daniela Molina Castro": "María Daniela Molina Castro",
    "María Gabriela Rojas Carvajal": "Maria Gabriela Rojas Carvajal",
    # Prepago internal unifications
    "Stephanie Davila Vasquez": "Stephanie Dávila Vásquez",
    "Jennifer Maria Rodriguez Calderon": "Jennifer Maria Rodríguez Calderon",
    "Miriam Maria Porras Mora": "Míriam Maria Porras Mora",
    "Ericka Alexandra Hernandez Romero": "Ericka Hernández Romero",
    "Deybel Pricsilla Pena Lopez": "Deybell Priscilla Peña",
    "Lisseth Anabell Campos Colimdres": "Lisseth Campos Colindres"
}

def resolve_prepago_seller(asesor_raw):
    raw = str(asesor_raw or '').strip()
    if not raw or raw in ['-', 'N/A']: return 'Sin Asignar'
    if raw in EXPLICIT_MAP: return EXPLICIT_MAP[raw]
    if raw in retail_sellers: return raw
    cleaned = clean_name(raw)
    if cleaned in retail_cleaned_map: return retail_cleaned_map[cleaned]
    return raw

print("\n--- 2. LOADING PREPAGO EXCEL ---")
wb_prepago = openpyxl.load_workbook(prepago_path, read_only=True)
ws_prepago = wb_prepago['PREPAGO P1']

prepago_records = []

for r in ws_prepago.iter_rows(min_row=2, values_only=True):
    if not any(c is not None and str(c).strip() != '' for c in r[:10]): continue
    f = r[0]
    fecha_str = f.strftime('%Y-%m-%d') if hasattr(f, 'strftime') else str(f)[:10] if f else ''
    
    anio = r[1]
    try: anio = int(anio)
    except:
        if fecha_str and len(fecha_str) >= 4:
            try: anio = int(fecha_str[:4])
            except: anio = 2026
        else: anio = 2026
            
    mes = str(r[2]).strip() if r[2] else ''
    if mes.lower() not in meses_validos:
        if fecha_str and len(fecha_str) >= 7:
            m_num = fecha_str[5:7]
            mes = n_to_m.get(m_num, 'Sin Mes')
        else: mes = 'Sin Mes'
    else: mes = mes.capitalize()
    
    asesor_raw = r[3]
    vendedor = resolve_prepago_seller(asesor_raw)
    
    cliente = str(r[4]).strip() if r[4] else 'Cliente Final'
    cedula = clean_str_val(r[5])
    
    # Col 7: MONTO DE RECARGA
    precio = clean_price(r[7])
    
    # Col 9: TIPO DE SERVICIO ('Prepago' or 'Portabilidad Prepago')
    raw_serv = str(r[9] or '').strip()
    if 'porta' in raw_serv.lower():
        norm_tipo = 'Portabilidad Prepago'
    else:
        norm_tipo = 'Prepago'
        
    plan = norm_tipo
    
    # Col 16: MULTIMARCA / CADENAS
    raw_canal = str(r[16] or '').strip().lower()
    if 'cadena' in raw_canal: canal = 'Cadenas'
    elif 'multi' in raw_canal: canal = 'Multimarca'
    elif 'avicam' in raw_canal: canal = 'Avicam'
    else: canal = 'Otros'
    
    # Col 17: PDV
    pdv = str(r[17]).strip() if r[17] else 'General'
    
    # All activations in Prepago report are completed sales
    estado = 'VENTA'
    
    # Col 14: SUPERVISOR
    supervisor = str(r[14]).strip() if r[14] else 'Sin Supervisor'
    if supervisor in ['-', '', 'NA', 'N/A']: supervisor = 'Sin Supervisor'
    
    # Col 11: OPERADORA DONANTE
    raw_don = str(r[11] or '').strip().lower()
    if 'liberty' in raw_don: donante = 'Liberty'
    elif 'kolbi' in raw_don or 'kölbi' in raw_don: donante = 'Kölbi'
    else: donante = 'N/A'
    
    # Col 18: PROVINCIA
    provincia = normalize_provincia(r[18])
    
    # Col 19: CANTON
    canton = str(r[19]).strip() if r[19] else ''
    
    # Contrato: for prepago it's 'Prepago'
    contrato = 'Prepago'
    # ID: Col 8 (NUMERO DE SIM)
    id_tramite = clean_str_val(r[8])
    # Teléfono: Col 6 (NUMERO DE TELEFONO ACTIVO) or Col 10 (NUMERO A PORTAR)
    telefono = clean_str_val(r[6]) or clean_str_val(r[10])
    
    prepago_records.append([fecha_str, anio, mes, cliente, cedula, plan, precio, canal, pdv, norm_tipo, estado, vendedor, supervisor, donante, provincia, canton, contrato, id_tramite, telefono])

wb_prepago.close()
print(f"Prepago records extracted: {len(prepago_records)}")

# 3. MERGE DATASETS
combined_records = retail_records + prepago_records
print(f"\n--- 3. COMBINED TOTAL RECORDS: {len(combined_records):,} ---")

# Save to data_retail.json
print("\nSaving to data_retail.json...")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(combined_records, f, ensure_ascii=False)
print("Saved data_retail.json successfully!")

# 4. UPDATE HTML FILES
json_dataset_str = json.dumps(combined_records, ensure_ascii=False)

# Self-sync removed

print("\nEmbedding into index.html and dashboard.html...")
def update_dataset_in_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update comment
    html = re.sub(
        r'//\s*Embedded dataset of[^\n]+',
        f'// Embedded dataset of {len(combined_records):,} records (Retail + Prepago)',
        html
    )

    # 2. Replace window.RAW_DATASET
    raw_dataset_regex = re.compile(r'window\.RAW_DATASET\s*=\s*\[\[[\s\S]*?\]\];', re.MULTILINE)
    if raw_dataset_regex.search(html):
        html = raw_dataset_regex.sub(f'window.RAW_DATASET = {json_dataset_str};', html)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Successfully embedded new dataset in {file_path}")
        return True
    else:
        print(f"ERROR: Could not find window.RAW_DATASET regex in {file_path}")
        return False

web_repo_path = r'C:\Users\Lenovo\Documents\salesland-dashboard-web\index.html'

ok1 = update_dataset_in_html(index_path)
ok2 = update_dataset_in_html(dash_path)
ok3 = False
if os.path.exists(web_repo_path):
    ok3 = update_dataset_in_html(web_repo_path)

# Also publish to GitHub Pages if git is configured
web_repo_dir = r'C:\Users\Lenovo\Documents\salesland-dashboard-web'
if os.path.exists(os.path.join(web_repo_dir, '.git')):
    try:
        print("\nSubiendo actualización a GitHub Pages...")
        import subprocess
        subprocess.run(['git', 'add', 'index.html'], cwd=web_repo_dir, check=False)
        subprocess.run(['git', 'commit', '-m', f"Actualizar datos desde Excels: {len(combined_records):,} registros"], cwd=web_repo_dir, check=False)
        subprocess.run(['git', '-c', 'credential.helper=', '-c', 'credential.helper=manager', 'push', 'origin', 'main'], cwd=web_repo_dir, check=False)
        print("[OK] Publicacion en GitHub Pages completada con exito.")
    except Exception as e:
        print(f"Nota Git: {e}")

if ok1 and ok2:
    print(f"\nSUCCESS! Dataset con {len(combined_records):,} registros generado y embebido con éxito.")
else:
    print("\nFAILED to embed dataset.")
