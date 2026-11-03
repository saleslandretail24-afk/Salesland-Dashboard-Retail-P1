import openpyxl, re, json, unicodedata, sys, os, time, datetime
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

# File paths
retail_path = r'C:\Users\Lenovo\Documents\Mi dashboard\Dashboard HTML RETAIL .xlsx'
prepago_path = r'C:\Users\Lenovo\Documents\Mi dashboard\Dashboard HTML PREPAGO.xlsx'
p2_path = r'C:\Users\Lenovo\Documents\Mi dashboard\RETAIL P2.xlsx'

index_path = r'C:\Users\Lenovo\Documents\Mi dashboard\index.html'
dash_path = r'C:\Users\Lenovo\Documents\Mi dashboard\dashboard.html'
json_path = r'C:\Users\Lenovo\Documents\Mi dashboard\data_retail.json'
json_p2_path = r'C:\Users\Lenovo\Documents\Mi dashboard\data_retail_p2.json'
web_repo_path = r'C:\Users\Lenovo\Documents\salesland-dashboard-web\index.html'
web_repo_dir = r'C:\Users\Lenovo\Documents\salesland-dashboard-web'

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

def clean_phone_val(val):
    if val is None: return ''
    s = str(val).strip()
    if s.endswith('.0'): s = s[:-2]
    if s.lower() in ['-', 'n/a', 'na', 'none', 'null', 'nan', '']: return ''
    if s.startswith('+'): s = s[1:].strip()
    digits = re.sub(r'\D', '', s)
    if digits.startswith('506'):
        if len(digits) > 3:
            digits = digits[3:]
        else:
            return ''
    return digits if digits else s

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

CANTON_TO_PROV = {
    'san jose': 'San José', 'escazu': 'San José', 'desamparados': 'San José', 'puriscal': 'San José',
    'tarrazu': 'San José', 'aserri': 'San José', 'mora': 'San José', 'goicoechea': 'San José',
    'santa ana': 'San José', 'alajuelita': 'San José', 'vazquez de coronado': 'San José', 'coronado': 'San José',
    'acosta': 'San José', 'tibas': 'San José', 'moravia': 'San José', 'montes de oca': 'San José',
    'turrubares': 'San José', 'dota': 'San José', 'curridabat': 'San José', 'perez zeledon': 'San José',
    'leon cortes': 'San José', 'san isidro del general': 'San José',
    'alajuela': 'Alajuela', 'san ramon': 'Alajuela', 'grecia': 'Alajuela', 'san mateo': 'Alajuela',
    'atenas': 'Alajuela', 'naranjo': 'Alajuela', 'palmares': 'Alajuela', 'poas': 'Alajuela',
    'orotina': 'Alajuela', 'san carlos': 'Alajuela', 'zarcero': 'Alajuela', 'sarchi': 'Alajuela',
    'upala': 'Alajuela', 'los chiles': 'Alajuela', 'guatuso': 'Alajuela', 'rio cuarto': 'Alajuela',
    'ciudad quesada': 'Alajuela',
    'cartago': 'Cartago', 'paraiso': 'Cartago', 'la union': 'Cartago', 'tres rios': 'Cartago',
    'jimenez': 'Cartago', 'turrialba': 'Cartago', 'alvarado': 'Cartago', 'oreamuno': 'Cartago',
    'el guarco': 'Cartago',
    'heredia': 'Heredia', 'barva': 'Heredia', 'santo domingo': 'Heredia', 'santa barbara': 'Heredia',
    'san rafael': 'Heredia', 'san isidro': 'Heredia', 'belen': 'Heredia', 'flores': 'Heredia',
    'san pablo': 'Heredia', 'sarapiqui': 'Heredia',
    'liberia': 'Guanacaste', 'nicoya': 'Guanacaste', 'santa cruz': 'Guanacaste', 'bagaces': 'Guanacaste',
    'carrillo': 'Guanacaste', 'canas': 'Guanacaste', 'abangares': 'Guanacaste', 'tilaran': 'Guanacaste',
    'nandayure': 'Guanacaste', 'la cruz': 'Guanacaste', 'hojancha': 'Guanacaste', 'filadelfia': 'Guanacaste',
    'puntarenas': 'Puntarenas', 'esparza': 'Puntarenas', 'buenos aires': 'Puntarenas', 'montes de oro': 'Puntarenas',
    'osa': 'Puntarenas', 'quepos': 'Puntarenas', 'golfito': 'Puntarenas', 'coto brus': 'Puntarenas',
    'parrita': 'Puntarenas', 'corredores': 'Puntarenas', 'garabito': 'Puntarenas', 'monteverde': 'Puntarenas',
    'puerto jimenez': 'Puntarenas', 'jaco': 'Puntarenas', 'ciudad neily': 'Puntarenas',
    'limon': 'Limón', 'pococi': 'Limón', 'siquirres': 'Limón', 'talamanca': 'Limón',
    'matina': 'Limón', 'guacimo': 'Limón', 'guapiles': 'Limón'
}

def normalize_provincia(p_raw, canton_raw=''):
    p = str(p_raw or '').strip()
    p_lower = strip_accents(p)
    if 'san jose' in p_lower: return 'San José'
    if 'alajuela' in p_lower: return 'Alajuela'
    if 'cartago' in p_lower: return 'Cartago'
    if 'heredia' in p_lower: return 'Heredia'
    if 'guanacaste' in p_lower or 'nicoya' in p_lower or 'liberia' in p_lower: return 'Guanacaste'
    if 'puntarenas' in p_lower: return 'Puntarenas'
    if 'limon' in p_lower or 'guapiles' in p_lower or 'pococi' in p_lower: return 'Limón'
    c_lower = strip_accents(canton_raw)
    if c_lower in CANTON_TO_PROV:
        return CANTON_TO_PROV[c_lower]
    for k, v in CANTON_TO_PROV.items():
        if k and k in c_lower:
            return v
    return 'Sin Especificar'

def normalize_pdv_name(raw_pdv):
    s = str(raw_pdv or '').strip()
    if not s or s.lower() in ['-', 'n/a', 'na', 'none', 'null', 'nan', '1', '0', 'sin asignar', 'n/d']:
        return 'General'
    if re.match(r'^\d+$', s):
        return 'General'
    s = re.sub(r'\s+', ' ', s)
    return s

EXPLICIT_MAP = {
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
    "Stephanie Davila Vasquez": "Stephanie Dávila Vásquez",
    "Jennifer Maria Rodriguez Calderon": "Jennifer Maria Rodríguez Calderon",
    "Miriam Maria Porras Mora": "Míriam Maria Porras Mora",
    "Ericka Alexandra Hernandez Romero": "Ericka Hernández Romero",
    "Deybel Pricsilla Pena Lopez": "Deybell Priscilla Peña",
    "Lisseth Anabell Campos Colimdres": "Lisseth Campos Colindres",
    "Yahaira De Los Angeles Castro Solis": "Yahaira Castro Solis",
    "5122868": "Sin Asignar"
}

def canonicalize_records_names(records):
    """Unifies seller (idx 11), supervisor (idx 12), PDV (idx 8), and Canton (idx 15) names."""
    # 1. Sellers & Supervisors
    for idx, default_lbl in [(11, 'Sin Asignar'), (12, 'Sin Supervisor')]:
        counts = Counter()
        for r in records:
            val = re.sub(r'\s+', ' ', str(r[idx] or '').strip())
            if val in EXPLICIT_MAP:
                val = EXPLICIT_MAP[val]
            if not val or val in ['-', 'NA', 'N/A'] or re.match(r'^\d+$', val):
                val = default_lbl
            r[idx] = val
            if val != default_lbl:
                counts[val] += 1

        groups = defaultdict(list)
        for name, cnt in counts.items():
            groups[clean_name(name)].append((name, cnt))

        canon_map = {}
        for k, variants in groups.items():
            if len(variants) == 1:
                canon_map[k] = variants[0][0]
            else:
                variants.sort(key=lambda x: (x[1], sum(1 for c in x[0] if ord(c) > 127)), reverse=True)
                canon_map[k] = variants[0][0]

        for r in records:
            val = r[idx]
            if val != default_lbl:
                k = clean_name(val)
                if k in canon_map:
                    r[idx] = canon_map[k]

    # 2. PDV (idx 8) & Canton (idx 15) case/accent unification (prefer Mixed/Title Case over ALL CAPS unless acronym <= 4 chars)
    for idx, default_lbl in [(8, 'General'), (15, '')]:
        counts = Counter()
        for r in records:
            val = re.sub(r'\s+', ' ', str(r[idx] or '').strip())
            if not val or val.lower() in ['-', 'na', 'n/a', 'n/d']:
                val = default_lbl
            r[idx] = val
            if val != default_lbl:
                counts[val] += 1

        groups = defaultdict(list)
        for name, cnt in counts.items():
            groups[clean_name(name)].append((name, cnt))

        canon_map = {}
        for k, variants in groups.items():
            if len(variants) == 1:
                v0 = variants[0][0]
                if v0.isupper() and len(v0) > 4:
                    v0 = v0.title()
                canon_map[k] = v0
            else:
                # Prefer non-ALL-CAPS (Title Case) and accented variants when unifying
                variants.sort(key=lambda x: (0 if (x[0].isupper() and len(x[0]) > 4) else 1, sum(1 for c in x[0] if ord(c) > 127), x[1]), reverse=True)
                best = variants[0][0]
                if best.isupper() and len(best) > 4:
                    best = best.title()
                canon_map[k] = best

        for r in records:
            val = r[idx]
            if val != default_lbl:
                k = clean_name(val)
                if k in canon_map:
                    r[idx] = canon_map[k]

def detect_prepago_geo_cols(ws):
    """Detects exact column indices for PDV, PROVINCIA, and CANTON in PREPAGO sheets."""
    header_row = next(ws.iter_rows(min_row=1, max_row=1, values_only=True), None)
    idx_pdv, idx_prov, idx_cant = 17, 18, 19
    if header_row:
        for i, h in enumerate(header_row):
            h_clean = strip_accents(h)
            if h_clean == 'pdv':
                idx_pdv = i
            elif h_clean == 'provincia':
                idx_prov = i
            elif h_clean in ('canton', 'cantón'):
                idx_cant = i
    return idx_pdv, idx_prov, idx_cant

# ==========================================
# 1. PROCESSING RETAIL P1
# ==========================================
print("======================================================================")
print("  SALESLAND | PROCESANDO DATOS RETAIL P1...")
print("======================================================================")
wb_retail = openpyxl.load_workbook(retail_path, read_only=True)
ws_retail = wb_retail['POSPAGO P1']

retail_records = []
retail_sellers = set()

for r in ws_retail.iter_rows(min_row=2, values_only=True):
    if not any(c is not None and str(c).strip() != '' for c in r[:16]): continue
    f = r[0]
    fecha_str = f.strftime('%Y-%m-%d') if hasattr(f, 'strftime') else str(f).strip()[:10] if f else ''
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_str):
        continue

    anio = r[1]
    try: anio = int(anio)
    except:
        try: anio = int(fecha_str[:4])
        except: anio = 2026

    mes = str(r[2]).strip() if r[2] else ''
    if mes.lower() not in meses_validos:
        m_num = fecha_str[5:7]
        mes = n_to_m.get(m_num, 'Sin Mes')
    else:
        mes = mes.capitalize()
    if mes == 'Sin Mes':
        continue

    contrato = clean_str_val(r[4])
    id_tramite = clean_str_val(r[3])
    cliente = str(r[5]).strip() if r[5] else 'Cliente Final'
    cedula = clean_str_val(r[6])
    plan = str(r[7]).strip() if r[7] else 'Sin Plan'
    precio = clean_price(r[8])

    raw_canal = str(r[9] or '').strip().lower()
    if 'cadena' in raw_canal: canal = 'Cadenas'
    elif 'multi' in raw_canal: canal = 'Multimarca'
    elif 'avicam' in raw_canal: canal = 'Avicam'
    else: canal = 'Otros'

    pdv = normalize_pdv_name(r[10])
    norm_tipo = normalize_retail_service(r[11])

    raw_est = str(r[12] or '').strip().upper()
    estado = 'VENTA' if raw_est == 'VENTA' else 'RECHAZADA'

    vendedor = str(r[13]).strip() if r[13] else 'Sin Asignar'
    if vendedor in ['-', '', 'NA', 'N/A']: vendedor = 'Sin Asignar'
    if vendedor in EXPLICIT_MAP: vendedor = EXPLICIT_MAP[vendedor]
    retail_sellers.add(vendedor)

    supervisor = str(r[14]).strip() if r[14] else 'Sin Supervisor'
    if supervisor in ['-', '', 'NA', 'N/A']: supervisor = 'Sin Supervisor'

    telefono = clean_phone_val(r[15]) or clean_phone_val(r[16])

    raw_don = str(r[17] or '').strip().lower()
    if 'liberty' in raw_don: donante = 'Liberty'
    elif 'kolbi' in raw_don or 'kölbi' in raw_don: donante = 'Kölbi'
    else: donante = 'N/A'

    canton = str(r[22]).strip() if len(r) > 22 and r[22] else ''
    if canton.upper() in ['N/D', 'N/A', 'NA', '-']: canton = ''
    provincia = normalize_provincia(r[21] if len(r) > 21 else '', canton)

    retail_records.append([fecha_str, anio, mes, cliente, cedula, plan, precio, canal, pdv, norm_tipo, estado, vendedor, supervisor, donante, provincia, canton, contrato, id_tramite, telefono])

wb_retail.close()
print(f"Pospago P1 extraído: {len(retail_records):,} registros")

retail_cleaned_map = {clean_name(s): s for s in retail_sellers}

def resolve_prepago_seller(asesor_raw, ref_sellers, ref_clean_map):
    raw = str(asesor_raw or '').strip()
    if not raw or raw in ['-', 'N/A', 'NA'] or re.match(r'^\d+$', raw): return 'Sin Asignar'
    if raw in EXPLICIT_MAP: return EXPLICIT_MAP[raw]
    if raw in ref_sellers: return raw
    cleaned = clean_name(raw)
    if cleaned in ref_clean_map: return ref_clean_map[cleaned]
    return raw

wb_prepago = openpyxl.load_workbook(prepago_path, read_only=True)
ws_prepago = wb_prepago['PREPAGO P1']
p1_idx_pdv, p1_idx_prov, p1_idx_cant = detect_prepago_geo_cols(ws_prepago)
print(f"Columnas detectadas en PREPAGO P1 -> PDV: col[{p1_idx_pdv}], PROVINCIA: col[{p1_idx_prov}], CANTON: col[{p1_idx_cant}]")

prepago_records = []

for r in ws_prepago.iter_rows(min_row=2, values_only=True):
    if not any(c is not None and str(c).strip() != '' for c in r[:10]): continue
    f = r[0]
    fecha_str = f.strftime('%Y-%m-%d') if hasattr(f, 'strftime') else str(f).strip()[:10] if f else ''
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_str):
        continue

    anio = r[1]
    try: anio = int(anio)
    except:
        try: anio = int(fecha_str[:4])
        except: anio = 2026

    mes = str(r[2]).strip() if r[2] else ''
    if mes.lower() not in meses_validos:
        m_num = fecha_str[5:7]
        mes = n_to_m.get(m_num, 'Sin Mes')
    else:
        mes = mes.capitalize()
    if mes == 'Sin Mes':
        continue

    asesor_raw = r[3]
    vendedor = resolve_prepago_seller(asesor_raw, retail_sellers, retail_cleaned_map)

    cliente = str(r[4]).strip() if r[4] else 'Cliente Final'
    cedula = clean_str_val(r[5])
    precio = clean_price(r[7])

    raw_serv = str(r[9] or '').strip().lower()
    if 'porta' in raw_serv: norm_tipo = 'Portabilidad Prepago'
    else: norm_tipo = 'Prepago'
    plan = norm_tipo

    raw_canal = str(r[16] or '').strip().lower() if len(r) > 16 else ''
    if 'cadena' in raw_canal: canal = 'Cadenas'
    elif 'multi' in raw_canal: canal = 'Multimarca'
    elif 'avicam' in raw_canal: canal = 'Avicam'
    else: canal = 'Otros'

    pdv = normalize_pdv_name(r[p1_idx_pdv] if len(r) > p1_idx_pdv else '')
    estado = 'VENTA'

    supervisor = str(r[14]).strip() if len(r) > 14 and r[14] else 'Sin Supervisor'
    if supervisor in ['-', '', 'NA', 'N/A']: supervisor = 'Sin Supervisor'

    raw_don = str(r[11] or '').strip().lower() if len(r) > 11 else ''
    if 'liberty' in raw_don: donante = 'Liberty'
    elif 'kolbi' in raw_don or 'kölbi' in raw_don: donante = 'Kölbi'
    else: donante = 'N/A'

    canton = str(r[p1_idx_cant]).strip() if len(r) > p1_idx_cant and r[p1_idx_cant] else ''
    if canton.upper() in ['N/D', 'N/A', 'NA', '-']: canton = ''
    provincia = normalize_provincia(r[p1_idx_prov] if len(r) > p1_idx_prov else '', canton)

    contrato = 'Prepago'
    id_tramite = clean_str_val(r[8]) if len(r) > 8 else ''
    telefono = clean_phone_val(r[6]) if len(r) > 6 else ''
    if not telefono and len(r) > 10: telefono = clean_phone_val(r[10])

    prepago_records.append([fecha_str, anio, mes, cliente, cedula, plan, precio, canal, pdv, norm_tipo, estado, vendedor, supervisor, donante, provincia, canton, contrato, id_tramite, telefono])

wb_prepago.close()
print(f"Prepago P1 extraído: {len(prepago_records):,} registros")

combined_records_p1 = retail_records + prepago_records
canonicalize_records_names(combined_records_p1)
print(f"TOTAL RETAIL P1 (limpio y normalizado): {len(combined_records_p1):,} registros")

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(combined_records_p1, f, ensure_ascii=False, separators=(',', ':'))
print("Guardado data_retail.json con éxito!")

# ==========================================
# 2. PROCESSING RETAIL P2
# ==========================================
combined_records_p2 = []
if os.path.exists(p2_path):
    print("\n======================================================================")
    print("  SALESLAND | PROCESANDO DATOS RETAIL P2...")
    print("======================================================================")
    wb_p2 = openpyxl.load_workbook(p2_path, read_only=True)

    ws_pos_p2 = wb_p2['POSPAGO P2']
    pospago_p2_records = []
    p2_sellers = set()

    for r in ws_pos_p2.iter_rows(min_row=2, values_only=True):
        if not any(c is not None and str(c).strip() != '' for c in r[:16]): continue
        f = r[0]
        fecha_str = f.strftime('%Y-%m-%d') if hasattr(f, 'strftime') else str(f).strip()[:10] if f else ''
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_str):
            continue

        anio = r[1]
        try: anio = int(anio)
        except:
            try: anio = int(fecha_str[:4])
            except: anio = 2026

        mes = str(r[2]).strip() if r[2] else ''
        if mes.lower() not in meses_validos:
            m_num = fecha_str[5:7]
            mes = n_to_m.get(m_num, 'Sin Mes')
        else:
            mes = mes.capitalize()
        if mes == 'Sin Mes':
            continue

        contrato = clean_str_val(r[4])
        id_tramite = clean_str_val(r[3])
        cliente = str(r[5]).strip() if r[5] else 'Cliente Final'
        cedula = clean_str_val(r[6])
        plan = str(r[7]).strip() if r[7] else 'Sin Plan'
        precio = clean_price(r[8])

        raw_canal = str(r[9] or '').strip().lower()
        if 'cadena' in raw_canal: canal = 'Cadenas'
        elif 'multi' in raw_canal: canal = 'Multimarca'
        elif 'avicam' in raw_canal: canal = 'Avicam'
        else: canal = 'Otros'

        pdv = normalize_pdv_name(r[10])
        norm_tipo = normalize_retail_service(r[11])

        raw_est = str(r[12] or '').strip().upper()
        estado = 'VENTA' if raw_est == 'VENTA' else 'RECHAZADA'

        vendedor = str(r[13]).strip() if r[13] else 'Sin Asignar'
        if vendedor in ['-', '', 'NA', 'N/A'] or re.match(r'^\d+$', vendedor): vendedor = 'Sin Asignar'
        if vendedor in EXPLICIT_MAP: vendedor = EXPLICIT_MAP[vendedor]
        p2_sellers.add(vendedor)

        supervisor = str(r[14]).strip() if r[14] else 'Sin Supervisor'
        if supervisor in ['-', '', 'NA', 'N/A']: supervisor = 'Sin Supervisor'

        telefono = clean_phone_val(r[15]) or clean_phone_val(r[16])

        raw_don = str(r[17] or '').strip().lower()
        if 'liberty' in raw_don: donante = 'Liberty'
        elif 'kolbi' in raw_don or 'kölbi' in raw_don: donante = 'Kölbi'
        else: donante = 'N/A'

        canton = str(r[22]).strip() if len(r) > 22 and r[22] else ''
        if canton.upper() in ['N/D', 'N/A', 'NA', '-']: canton = ''
        provincia = normalize_provincia(r[21] if len(r) > 21 else '', canton)

        pospago_p2_records.append([fecha_str, anio, mes, cliente, cedula, plan, precio, canal, pdv, norm_tipo, estado, vendedor, supervisor, donante, provincia, canton, contrato, id_tramite, telefono])

    print(f"Pospago P2 extraído: {len(pospago_p2_records):,} registros")
    p2_cleaned_map = {clean_name(s): s for s in p2_sellers}

    ws_prep_p2 = wb_p2['PREPAGO P2']
    p2_idx_pdv, p2_idx_prov, p2_idx_cant = detect_prepago_geo_cols(ws_prep_p2)
    print(f"Columnas detectadas en PREPAGO P2 -> PDV: col[{p2_idx_pdv}], PROVINCIA: col[{p2_idx_prov}], CANTON: col[{p2_idx_cant}]")
    prepago_p2_records = []

    for r in ws_prep_p2.iter_rows(min_row=2, values_only=True):
        if not any(c is not None and str(c).strip() != '' for c in r[:10]): continue
        f = r[0]
        fecha_str = f.strftime('%Y-%m-%d') if hasattr(f, 'strftime') else str(f).strip()[:10] if f else ''
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_str):
            continue

        anio = r[1]
        try: anio = int(anio)
        except:
            try: anio = int(fecha_str[:4])
            except: anio = 2026

        mes = str(r[2]).strip() if r[2] else ''
        if mes.lower() not in meses_validos:
            m_num = fecha_str[5:7]
            mes = n_to_m.get(m_num, 'Sin Mes')
        else:
            mes = mes.capitalize()
        if mes == 'Sin Mes':
            continue

        asesor_raw = r[3]
        vendedor = resolve_prepago_seller(asesor_raw, p2_sellers, p2_cleaned_map)

        cliente = str(r[4]).strip() if r[4] else 'Cliente Final'
        cedula = clean_str_val(r[5])
        precio = clean_price(r[7])

        raw_serv = str(r[9] or '').strip().lower()
        if 'porta' in raw_serv: norm_tipo = 'Portabilidad Prepago'
        else: norm_tipo = 'Prepago'
        plan = norm_tipo

        raw_canal = str(r[16] or '').strip().lower() if len(r) > 16 else ''
        if 'cadena' in raw_canal: canal = 'Cadenas'
        elif 'multi' in raw_canal: canal = 'Multimarca'
        elif 'avicam' in raw_canal: canal = 'Avicam'
        else: canal = 'Otros'

        pdv = normalize_pdv_name(r[p2_idx_pdv] if len(r) > p2_idx_pdv else '')
        estado = 'VENTA'

        supervisor = str(r[14]).strip() if len(r) > 14 and r[14] else 'Sin Supervisor'
        if supervisor in ['-', '', 'NA', 'N/A']: supervisor = 'Sin Supervisor'

        raw_don = str(r[11] or '').strip().lower() if len(r) > 11 else ''
        if 'liberty' in raw_don: donante = 'Liberty'
        elif 'kolbi' in raw_don or 'kölbi' in raw_don: donante = 'Kölbi'
        else: donante = 'N/A'

        canton = str(r[p2_idx_cant]).strip() if len(r) > p2_idx_cant and r[p2_idx_cant] else ''
        if canton.upper() in ['N/D', 'N/A', 'NA', '-']: canton = ''
        provincia = normalize_provincia(r[p2_idx_prov] if len(r) > p2_idx_prov else '', canton)

        contrato = 'Prepago'
        id_tramite = clean_str_val(r[8]) if len(r) > 8 else ''
        telefono = clean_phone_val(r[6]) if len(r) > 6 else ''
        if not telefono and len(r) > 10: telefono = clean_phone_val(r[10])

        prepago_p2_records.append([fecha_str, anio, mes, cliente, cedula, plan, precio, canal, pdv, norm_tipo, estado, vendedor, supervisor, donante, provincia, canton, contrato, id_tramite, telefono])

    wb_p2.close()
    print(f"Prepago P2 extraído: {len(prepago_p2_records):,} registros")

    combined_records_p2 = pospago_p2_records + prepago_p2_records
    canonicalize_records_names(combined_records_p2)
    print(f"TOTAL RETAIL P2 (limpio y normalizado): {len(combined_records_p2):,} registros")

    with open(json_p2_path, 'w', encoding='utf-8') as f:
        json.dump(combined_records_p2, f, ensure_ascii=False, separators=(',', ':'))
    print("Guardado data_retail_p2.json con éxito!")

# ==========================================
# 3. EMBEDDING IN HTML FILES & OFFICIAL TARGETS
# ==========================================
print("\n======================================================================")
print("  EMBEBIENDO DATASETS Y METAS OFICIALES (P1 & P2)...")
print("======================================================================")
json_dataset_str_p1 = json.dumps(combined_records_p1, ensure_ascii=False, separators=(',', ':'))
json_dataset_str_p2 = json.dumps(combined_records_p2, ensure_ascii=False, separators=(',', ':')) if combined_records_p2 else "[]"
timestamp_str = datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p")

def update_dataset_in_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update comment
    p2_count_str = f" y {len(combined_records_p2):,} registros (Retail P2)" if combined_records_p2 else ""
    html = re.sub(
        r'//\s*Embedded dataset of[^\n]+',
        f'// Embedded dataset of {len(combined_records_p1):,} records (Retail P1){p2_count_str}',
        html
    )

    # 2. Replace window.RAW_DATASET
    raw_dataset_regex = re.compile(r'window\.RAW_DATASET\s*=\s*\[\[[\s\S]*?\]\];', re.MULTILINE)
    if raw_dataset_regex.search(html):
        html = raw_dataset_regex.sub(lambda _: f'window.RAW_DATASET = {json_dataset_str_p1};', html)
    else:
        print(f"ERROR: Could not find window.RAW_DATASET in {file_path}")
        return False

    # 3. Replace or insert window.RAW_DATASET_P2
    if 'window.RAW_DATASET_P2' in html:
        raw_p2_regex = re.compile(r'window\.RAW_DATASET_P2\s*=\s*\[[\s\S]*?\];', re.MULTILINE)
        html = raw_p2_regex.sub(lambda _: f'window.RAW_DATASET_P2 = {json_dataset_str_p2};', html)
    else:
        target_marker = f'window.RAW_DATASET = {json_dataset_str_p1};'
        insert_code = f'\n    window.RAW_DATASET_P2 = {json_dataset_str_p2};'
        html = html.replace(target_marker, target_marker + insert_code, 1)

    # 3.5 Update Last Data Update Timestamp in HTML and JS
    html = re.sub(
        r'<strong class="update-timestamp" id="last-update-timestamp">[^<]*</strong>',
        f'<strong class="update-timestamp" id="last-update-timestamp">{timestamp_str}</strong>',
        html
    )
    if 'window.LAST_DATA_UPDATE' in html:
        html = re.sub(r'window\.LAST_DATA_UPDATE\s*=\s*"[^"]*";', f'window.LAST_DATA_UPDATE = "{timestamp_str}";', html)
    else:
        marker = f'window.RAW_DATASET = {json_dataset_str_p1};'
        html = html.replace(marker, f'window.LAST_DATA_UPDATE = "{timestamp_str}";\n    ' + marker, 1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] Dataset y marca de tiempo actualizados en {file_path}")
    return True

ok1 = update_dataset_in_html(index_path)
if ok1:
    import shutil
    shutil.copy2(index_path, dash_path)
    print(f"[OK] Sincronizado idéntico (MD5) en {dash_path}")
    if os.path.exists(web_repo_dir):
        shutil.copy2(index_path, web_repo_path)
        print(f"[OK] Sincronizado idéntico (MD5) en {web_repo_path}")

# ==========================================
# 4. GITHUB PAGES DEPLOYMENT
# ==========================================
if '--no-push' not in sys.argv and os.path.exists(os.path.join(web_repo_dir, '.git')):
    try:
        print("\nSubiendo actualización a GitHub Pages...")
        import subprocess
        ahora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
        p2_txt = f", P2: {len(combined_records_p2):,} reg" if combined_records_p2 else ""
        msg = f"Actualización de datos (P1: {len(combined_records_p1):,} reg{p2_txt}) - {ahora}"
        subprocess.run(['git', 'add', 'index.html'], cwd=web_repo_dir, check=False)
        subprocess.run(['git', 'commit', '-m', msg], cwd=web_repo_dir, check=False)
        subprocess.run(['git', '-c', 'credential.helper=', '-c', 'credential.helper=manager', 'push', 'origin', 'main'], cwd=web_repo_dir, check=False)
        print("[OK] Publicacion en GitHub Pages completada con éxito.")
    except Exception as e:
        print(f"Nota Git: {e}")

print("\n======================================================================")
print(" ¡DATOS PROCESADOS Y ACTUALIZADOS CON ÉXITO!")
print("======================================================================")
