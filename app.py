"""
═══════════════════════════════════════════════════════════════════════════════
  AKILLI EV HVAC SİSTEMİ — BULANIK MANTIK KONTROLCÜSÜ
  Bulanık Mantık Dersi - Dönem Projesi
═══════════════════════════════════════════════════════════════════════════════

  Giriş Değişkenleri (5):
    1. İç Sıcaklık       (°C)   — soğuk / serin / ideal / ılık / sıcak
    2. Dış Sıcaklık      (°C)   — çok_soğuk / soğuk / ılıman / sıcak
    3. Nem               (%)    — kuru / normal / nemli / çok_nemli
    4. Kişi Sayısı       (kişi) — az / orta / çok
    5. Günün Saati       (saat) — gece / sabah / öğlen / akşam

  Çıkış Değişkenleri (2):
    1. Fan Hızı          (%)    — kapalı / düşük / orta / yüksek / maksimum
    2. Isıtma/Soğutma Gücü (-100..+100)
       — güçlü_soğutma / soğutma / kapalı / ısıtma / güçlü_ısıtma

  Çıkarım: Mamdani  |  Durulaştırma: Centroid (ağırlık merkezi)
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# SAYFA YAPILANDIRMASI
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Akıllı HVAC | Bulanık Mantık",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# ÖZEL CSS — Premium Glassmorphism Dark UI
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-primary: #06080f;
        --bg-secondary: #0c1220;
        --bg-card: rgba(15, 23, 42, 0.6);
        --bg-glass: rgba(15, 25, 50, 0.45);
        --border-glass: rgba(99, 102, 241, 0.15);
        --border-hover: rgba(99, 102, 241, 0.35);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-blue: #3b82f6;
        --accent-cyan: #06b6d4;
        --accent-violet: #8b5cf6;
        --accent-rose: #f43f5e;
        --accent-amber: #f59e0b;
        --accent-emerald: #10b981;
        --glow-blue: 0 0 20px rgba(59,130,246,0.15);
        --glow-violet: 0 0 20px rgba(139,92,246,0.15);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background: var(--bg-primary) !important;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(59,130,246,0.08), transparent),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(139,92,246,0.06), transparent) !important;
    }

    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080d1a 0%, #0a1128 50%, #0c0f1f 100%) !important;
        border-right: 1px solid rgba(99,102,241,0.1) !important;
    }
    section[data-testid="stSidebar"] .stSlider > div > div {
        background: rgba(99,102,241,0.08);
        border-radius: 8px;
        padding: 2px 0;
    }

    /* ── HEADER ── */
    .hero-container {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        position: relative;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -40px; left: 50%; transform: translateX(-50%);
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -2px;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 40%, #f472b6 70%, #fb923c 100%);
        background-size: 200% 200%;
        animation: gradientShift 6s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        position: relative;
        z-index: 1;
    }
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    .subtitle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: var(--text-muted);
        letter-spacing: 2.5px;
        text-transform: uppercase;
        position: relative;
        z-index: 1;
    }
    .hero-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), rgba(244,63,94,0.2), transparent);
        margin: 1.2rem 0;
        border: none;
    }

    /* ── METRIC CARDS ── */
    .metric-card {
        background: var(--bg-glass);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 1.4rem 1.6rem;
        border-radius: 16px;
        border: 1px solid var(--border-glass);
        margin: 0.4rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-blue), var(--accent-violet));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .metric-card:hover {
        border-color: var(--border-hover);
        box-shadow: var(--glow-violet);
        transform: translateY(-2px);
    }
    .metric-card:hover::before { opacity: 1; }
    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.8px;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2.4rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
    }
    .metric-card-cool { border-left: 3px solid var(--accent-cyan); }
    .metric-card-cool .metric-value { color: #67e8f9; }
    .metric-card-heat { border-left: 3px solid var(--accent-rose); }
    .metric-card-heat .metric-value { color: #fda4af; }
    .metric-card-idle { border-left: 3px solid var(--accent-amber); }
    .metric-card-idle .metric-value { color: #fde68a; }

    /* ── SECTION HEADERS ── */
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 1.8rem 0 0.8rem 0;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid rgba(99,102,241,0.12);
        letter-spacing: -0.3px;
    }
    .section-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        color: var(--accent-violet);
        text-transform: uppercase;
        letter-spacing: 2px;
        display: block;
        margin-bottom: 0.3rem;
    }

    /* ── RULE BOXES ── */
    .rule-box {
        background: var(--bg-glass);
        backdrop-filter: blur(10px);
        border-left: 3px solid var(--accent-blue);
        padding: 0.7rem 1.1rem;
        margin: 0.35rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #cbd5e1;
        border-radius: 8px;
        transition: all 0.25s ease;
        border-top: 1px solid rgba(99,102,241,0.06);
        border-right: 1px solid rgba(99,102,241,0.06);
        border-bottom: 1px solid rgba(99,102,241,0.06);
    }
    .rule-box:hover {
        border-left-color: var(--accent-violet);
        background: rgba(15, 25, 50, 0.7);
        transform: translateX(3px);
    }
    .rule-strength {
        color: var(--accent-amber);
        font-weight: 600;
    }

    /* ── LOG ENTRIES ── */
    .log-entry {
        background: var(--bg-glass);
        backdrop-filter: blur(10px);
        border-left: 3px solid var(--accent-emerald);
        padding: 0.65rem 1.1rem;
        margin: 0.35rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        color: #cbd5e1;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    .log-entry:hover { background: rgba(15, 25, 50, 0.75); }
    .log-entry-cool { border-left-color: var(--accent-cyan); }
    .log-entry-heat { border-left-color: var(--accent-rose); }
    .log-entry-idle { border-left-color: var(--accent-amber); }
    .log-badge {
        display: inline-block;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
        font-size: 0.65rem;
        font-weight: 600;
        margin-right: 0.6rem;
        letter-spacing: 0.5px;
    }
    .badge-cool { background: rgba(6,182,212,0.15); color: #67e8f9; border: 1px solid rgba(6,182,212,0.25); }
    .badge-heat { background: rgba(244,63,94,0.15); color: #fda4af; border: 1px solid rgba(244,63,94,0.25); }
    .badge-idle { background: rgba(245,158,11,0.15); color: #fde68a; border: 1px solid rgba(245,158,11,0.25); }
    .log-counter {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--text-muted);
        text-align: right;
        padding: 0.3rem 0;
    }

    /* ── EXPANDERS ── */
    .streamlit-expanderHeader {
        background: var(--bg-glass) !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .streamlit-expanderHeader:hover {
        border-color: var(--border-hover) !important;
    }

    /* ── BUTTONS ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-violet)) !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59,130,246,0.25) !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 25px rgba(99,102,241,0.4) !important;
        transform: translateY(-1px) !important;
    }
    .stDownloadButton > button {
        background: var(--bg-glass) !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        border-color: var(--accent-emerald) !important;
        box-shadow: 0 0 15px rgba(16,185,129,0.15) !important;
    }

    /* ── DATAFRAMES & MARKDOWN ── */
    .stDataFrame { border-radius: 12px; overflow: hidden; }
    .stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th {
        color: #e2e8f0 !important;
        line-height: 1.6;
    }
    .stMarkdown strong {
        color: #f8fafc !important;
        font-weight: 600;
    }

    /* ── FOOTER ── */
    .footer-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--text-muted);
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        border-top: 1px solid rgba(99,102,241,0.08);
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.5); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE — LOG SİSTEMİ
# ──────────────────────────────────────────────────────────────────────────────
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'log_counter' not in st.session_state:
    st.session_state.log_counter = 0
if 'prev_inputs' not in st.session_state:
    st.session_state.prev_inputs = None


# ──────────────────────────────────────────────────────────────────────────────
# 1. EVRENLER (UNIVERSE OF DISCOURSE)
# ──────────────────────────────────────────────────────────────────────────────
ic_sicaklik    = ctrl.Antecedent(np.arange(0, 41, 0.5),   'ic_sicaklik')
dis_sicaklik   = ctrl.Antecedent(np.arange(-10, 46, 0.5), 'dis_sicaklik')
nem            = ctrl.Antecedent(np.arange(0, 101, 1),    'nem')
kisi_sayisi    = ctrl.Antecedent(np.arange(0, 11, 1),     'kisi_sayisi')
saat           = ctrl.Antecedent(np.arange(0, 24, 1),     'saat')

fan_hizi       = ctrl.Consequent(np.arange(0, 101, 1),    'fan_hizi')
isi_guc        = ctrl.Consequent(np.arange(-100, 101, 1), 'isi_guc')

# ──────────────────────────────────────────────────────────────────────────────
# 2. ÜYELİK FONKSİYONLARI
# ──────────────────────────────────────────────────────────────────────────────

# İç sıcaklık (°C)
ic_sicaklik['soguk']  = fuzz.trapmf(ic_sicaklik.universe, [0, 0, 10, 16])
ic_sicaklik['serin']  = fuzz.trimf (ic_sicaklik.universe, [14, 18, 22])
ic_sicaklik['ideal']  = fuzz.trimf (ic_sicaklik.universe, [20, 23, 26])
ic_sicaklik['ilik']   = fuzz.trimf (ic_sicaklik.universe, [24, 28, 32])
ic_sicaklik['sicak']  = fuzz.trapmf(ic_sicaklik.universe, [30, 34, 40, 40])

# Dış sıcaklık (°C)
dis_sicaklik['cok_soguk'] = fuzz.trapmf(dis_sicaklik.universe, [-10, -10, 0, 8])
dis_sicaklik['soguk']     = fuzz.trimf (dis_sicaklik.universe, [5, 12, 18])
dis_sicaklik['iliman']    = fuzz.trimf (dis_sicaklik.universe, [15, 22, 28])
dis_sicaklik['sicak']     = fuzz.trapmf(dis_sicaklik.universe, [25, 32, 45, 45])

# Nem (%)
nem['kuru']       = fuzz.trapmf(nem.universe, [0, 0, 25, 40])
nem['normal']     = fuzz.trimf (nem.universe, [35, 50, 65])
nem['nemli']      = fuzz.trimf (nem.universe, [60, 72, 85])
nem['cok_nemli']  = fuzz.trapmf(nem.universe, [80, 90, 100, 100])

# Kişi sayısı
kisi_sayisi['az']   = fuzz.trimf(kisi_sayisi.universe, [0, 0, 3])
kisi_sayisi['orta'] = fuzz.trimf(kisi_sayisi.universe, [2, 4, 6])
kisi_sayisi['cok']  = fuzz.trapmf(kisi_sayisi.universe, [5, 7, 10, 10])

# Günün saati
saat['gece']  = fuzz.trapmf(saat.universe, [0, 0, 5, 7])
saat['sabah'] = fuzz.trimf (saat.universe, [6, 9, 12])
saat['oglen'] = fuzz.trimf (saat.universe, [11, 14, 17])
saat['aksam'] = fuzz.trapmf(saat.universe, [16, 19, 23, 23])

# Fan hızı (%)
fan_hizi['kapali']   = fuzz.trimf(fan_hizi.universe, [0, 0, 15])
fan_hizi['dusuk']    = fuzz.trimf(fan_hizi.universe, [10, 25, 45])
fan_hizi['orta']     = fuzz.trimf(fan_hizi.universe, [35, 55, 70])
fan_hizi['yuksek']   = fuzz.trimf(fan_hizi.universe, [60, 75, 90])
fan_hizi['maksimum'] = fuzz.trapmf(fan_hizi.universe, [80, 92, 100, 100])

# Isıtma/Soğutma gücü (negatif=soğutma, pozitif=ısıtma)
isi_guc['guclu_sogutma'] = fuzz.trapmf(isi_guc.universe, [-100, -100, -75, -50])
isi_guc['sogutma']       = fuzz.trimf (isi_guc.universe, [-65, -40, -15])
isi_guc['kapali']        = fuzz.trimf (isi_guc.universe, [-20, 0, 20])
isi_guc['isitma']        = fuzz.trimf (isi_guc.universe, [15, 40, 65])
isi_guc['guclu_isitma']  = fuzz.trapmf(isi_guc.universe, [50, 75, 100, 100])


# ──────────────────────────────────────────────────────────────────────────────
# 3. KURAL TABANI (20 kural — istenen minimum 15'in üstünde)
# ──────────────────────────────────────────────────────────────────────────────
RULES_TEXT = []

def make_rule(antecedent, consequents, label):
    """Kural oluştur ve metin temsilini sakla."""
    RULES_TEXT.append(label)
    return ctrl.Rule(antecedent, consequents)

rules = [
    # — Aşırı sıcak ortam —
    make_rule(
        ic_sicaklik['sicak'] & dis_sicaklik['sicak'] & kisi_sayisi['cok'],
        [fan_hizi['maksimum'], isi_guc['guclu_sogutma']],
        "R01: İç SICAK ∧ Dış SICAK ∧ Kişi ÇOK → Fan MAKSİMUM, Güç GÜÇLÜ_SOĞUTMA"
    ),
    make_rule(
        ic_sicaklik['sicak'] & nem['cok_nemli'],
        [fan_hizi['maksimum'], isi_guc['guclu_sogutma']],
        "R02: İç SICAK ∧ Nem ÇOK_NEMLİ → Fan MAKSİMUM, Güç GÜÇLÜ_SOĞUTMA"
    ),
    make_rule(
        ic_sicaklik['sicak'] & dis_sicaklik['iliman'],
        [fan_hizi['yuksek'], isi_guc['sogutma']],
        "R03: İç SICAK ∧ Dış ILIMAN → Fan YÜKSEK, Güç SOĞUTMA"
    ),

    # — Ilık ortam —
    make_rule(
        ic_sicaklik['ilik'] & kisi_sayisi['cok'],
        [fan_hizi['yuksek'], isi_guc['sogutma']],
        "R04: İç ILIK ∧ Kişi ÇOK → Fan YÜKSEK, Güç SOĞUTMA"
    ),
    make_rule(
        ic_sicaklik['ilik'] & nem['nemli'],
        [fan_hizi['yuksek'], isi_guc['sogutma']],
        "R05: İç ILIK ∧ Nem NEMLİ → Fan YÜKSEK, Güç SOĞUTMA"
    ),
    make_rule(
        ic_sicaklik['ilik'] & kisi_sayisi['az'] & saat['gece'],
        [fan_hizi['orta'], isi_guc['kapali']],
        "R06: İç ILIK ∧ Kişi AZ ∧ GECE → Fan ORTA, Güç KAPALI"
    ),

    # — İdeal ortam —
    make_rule(
        ic_sicaklik['ideal'] & kisi_sayisi['orta'],
        [fan_hizi['dusuk'], isi_guc['kapali']],
        "R07: İç İDEAL ∧ Kişi ORTA → Fan DÜŞÜK, Güç KAPALI"
    ),
    make_rule(
        ic_sicaklik['ideal'] & kisi_sayisi['az'] & saat['gece'],
        [fan_hizi['kapali'], isi_guc['kapali']],
        "R08: İç İDEAL ∧ Kişi AZ ∧ GECE → Fan KAPALI, Güç KAPALI"
    ),
    make_rule(
        ic_sicaklik['ideal'] & nem['cok_nemli'],
        [fan_hizi['orta'], isi_guc['kapali']],
        "R09: İç İDEAL ∧ Nem ÇOK_NEMLİ → Fan ORTA, Güç KAPALI"
    ),
    make_rule(
        ic_sicaklik['ideal'] & kisi_sayisi['cok'],
        [fan_hizi['orta'], isi_guc['kapali']],
        "R10: İç İDEAL ∧ Kişi ÇOK → Fan ORTA, Güç KAPALI"
    ),

    # — Serin ortam —
    make_rule(
        ic_sicaklik['serin'] & dis_sicaklik['cok_soguk'],
        [fan_hizi['dusuk'], isi_guc['isitma']],
        "R11: İç SERİN ∧ Dış ÇOK_SOĞUK → Fan DÜŞÜK, Güç ISITMA"
    ),
    make_rule(
        ic_sicaklik['serin'] & saat['sabah'],
        [fan_hizi['dusuk'], isi_guc['isitma']],
        "R12: İç SERİN ∧ SABAH → Fan DÜŞÜK, Güç ISITMA"
    ),
    make_rule(
        ic_sicaklik['serin'] & kisi_sayisi['az'],
        [fan_hizi['dusuk'], isi_guc['isitma']],
        "R13: İç SERİN ∧ Kişi AZ → Fan DÜŞÜK, Güç ISITMA"
    ),

    # — Soğuk ortam —
    make_rule(
        ic_sicaklik['soguk'] & dis_sicaklik['cok_soguk'],
        [fan_hizi['orta'], isi_guc['guclu_isitma']],
        "R14: İç SOĞUK ∧ Dış ÇOK_SOĞUK → Fan ORTA, Güç GÜÇLÜ_ISITMA"
    ),
    make_rule(
        ic_sicaklik['soguk'] & dis_sicaklik['soguk'],
        [fan_hizi['dusuk'], isi_guc['guclu_isitma']],
        "R15: İç SOĞUK ∧ Dış SOĞUK → Fan DÜŞÜK, Güç GÜÇLÜ_ISITMA"
    ),
    make_rule(
        ic_sicaklik['soguk'] & saat['gece'],
        [fan_hizi['dusuk'], isi_guc['guclu_isitma']],
        "R16: İç SOĞUK ∧ GECE → Fan DÜŞÜK, Güç GÜÇLÜ_ISITMA"
    ),
    make_rule(
        ic_sicaklik['soguk'] & kisi_sayisi['cok'],
        [fan_hizi['orta'], isi_guc['isitma']],
        "R17: İç SOĞUK ∧ Kişi ÇOK → Fan ORTA, Güç ISITMA"
    ),

    # — Özel durumlar —
    make_rule(
        nem['kuru'] & ic_sicaklik['ilik'],
        [fan_hizi['orta'], isi_guc['sogutma']],
        "R18: Nem KURU ∧ İç ILIK → Fan ORTA, Güç SOĞUTMA"
    ),
    make_rule(
        saat['oglen'] & dis_sicaklik['sicak'] & ic_sicaklik['ilik'],
        [fan_hizi['yuksek'], isi_guc['sogutma']],
        "R19: ÖĞLEN ∧ Dış SICAK ∧ İç ILIK → Fan YÜKSEK, Güç SOĞUTMA"
    ),
    make_rule(
        saat['aksam'] & ic_sicaklik['ideal'] & kisi_sayisi['orta'],
        [fan_hizi['dusuk'], isi_guc['kapali']],
        "R20: AKŞAM ∧ İç İDEAL ∧ Kişi ORTA → Fan DÜŞÜK, Güç KAPALI"
    ),
]


# ──────────────────────────────────────────────────────────────────────────────
# 4. KONTROL SİSTEMİ
# ──────────────────────────────────────────────────────────────────────────────
hvac_ctrl = ctrl.ControlSystem(rules)
hvac_sim  = ctrl.ControlSystemSimulation(hvac_ctrl)


# ──────────────────────────────────────────────────────────────────────────────
# YARDIMCI FONKSİYONLAR
# ──────────────────────────────────────────────────────────────────────────────
def plot_membership(variable, current_value, title, color_palette):
    """Bir değişken için üyelik fonksiyonu grafiği — mevcut değeri dikey çizgi ile."""
    fig, ax = plt.subplots(figsize=(8, 3.2), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')

    for i, term_name in enumerate(variable.terms):
        mf = variable[term_name].mf
        color = color_palette[i % len(color_palette)]
        ax.plot(variable.universe, mf, linewidth=2.2, color=color, label=term_name)
        ax.fill_between(variable.universe, 0, mf, alpha=0.15, color=color)

        # Mevcut girişin üyelik derecesi
        membership = fuzz.interp_membership(variable.universe, mf, current_value)
        if membership > 0.01:
            ax.plot(current_value, membership, 'o', color=color, markersize=10,
                    markeredgecolor='white', markeredgewidth=1.5, zorder=5)

    # Mevcut değer dikey çizgisi
    ax.axvline(current_value, color='#fbbf24', linestyle='--', linewidth=1.5, alpha=0.8)
    ax.text(current_value, 1.05, f' {current_value:.1f}', color='#fbbf24',
            fontweight='bold', fontsize=10)

    ax.set_title(title, color='#f1f5f9', fontsize=12, fontweight='bold', pad=12)
    ax.set_ylabel('Üyelik', color='#94a3b8', fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, alpha=0.15, color='#475569')
    ax.legend(loc='upper right', framealpha=0.9, facecolor='#1e293b',
              edgecolor='#334155', labelcolor='#e2e8f0', fontsize=9)
    for spine in ax.spines.values():
        spine.set_color('#334155')
    plt.tight_layout()
    return fig


def plot_output(variable, crisp_value, title, color):
    """Çıkış değişkeni için durulaştırma grafiği."""
    fig, ax = plt.subplots(figsize=(9, 3.5), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')

    palette = ['#0ea5e9', '#6366f1', '#a855f7', '#ec4899', '#f59e0b']
    for i, term_name in enumerate(variable.terms):
        mf = variable[term_name].mf
        c = palette[i % len(palette)]
        ax.plot(variable.universe, mf, linewidth=2, color=c, alpha=0.6, label=term_name)
        ax.fill_between(variable.universe, 0, mf, alpha=0.1, color=c)

    # Durulaştırılmış değer
    ax.axvline(crisp_value, color=color, linestyle='-', linewidth=3, alpha=0.9)
    ax.plot(crisp_value, 0, 'v', color=color, markersize=18,
            markeredgecolor='white', markeredgewidth=2, zorder=5)
    ax.text(crisp_value, 1.08, f' Çıkış: {crisp_value:.2f}', color=color,
            fontweight='bold', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b',
                      edgecolor=color, linewidth=1.5))

    ax.set_title(title, color='#f1f5f9', fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel('Üyelik', color='#94a3b8', fontsize=10)
    ax.set_ylim(0, 1.2)
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, alpha=0.15, color='#475569')
    ax.legend(loc='upper right', framealpha=0.9, facecolor='#1e293b',
              edgecolor='#334155', labelcolor='#e2e8f0', fontsize=9, ncol=2)
    for spine in ax.spines.values():
        spine.set_color('#334155')
    plt.tight_layout()
    return fig


def calculate_active_rules(inputs):
    """Hangi kuralların hangi güçle ateşlendiğini hesapla."""
    ic_s, dis_s, nm, ks, st_ = inputs
    active = []

    # Tüm dilsel terimlerin üyelik dereceleri
    mu = {
        'ic_sicaklik': {
            t: fuzz.interp_membership(ic_sicaklik.universe, ic_sicaklik[t].mf, ic_s)
            for t in ic_sicaklik.terms
        },
        'dis_sicaklik': {
            t: fuzz.interp_membership(dis_sicaklik.universe, dis_sicaklik[t].mf, dis_s)
            for t in dis_sicaklik.terms
        },
        'nem': {
            t: fuzz.interp_membership(nem.universe, nem[t].mf, nm)
            for t in nem.terms
        },
        'kisi_sayisi': {
            t: fuzz.interp_membership(kisi_sayisi.universe, kisi_sayisi[t].mf, ks)
            for t in kisi_sayisi.terms
        },
        'saat': {
            t: fuzz.interp_membership(saat.universe, saat[t].mf, st_)
            for t in saat.terms
        },
    }

    # Kuralların antesedan listesi (label, [(var, term), ...])
    rule_specs = [
        ("R01", [('ic_sicaklik','sicak'),('dis_sicaklik','sicak'),('kisi_sayisi','cok')]),
        ("R02", [('ic_sicaklik','sicak'),('nem','cok_nemli')]),
        ("R03", [('ic_sicaklik','sicak'),('dis_sicaklik','iliman')]),
        ("R04", [('ic_sicaklik','ilik'),('kisi_sayisi','cok')]),
        ("R05", [('ic_sicaklik','ilik'),('nem','nemli')]),
        ("R06", [('ic_sicaklik','ilik'),('kisi_sayisi','az'),('saat','gece')]),
        ("R07", [('ic_sicaklik','ideal'),('kisi_sayisi','orta')]),
        ("R08", [('ic_sicaklik','ideal'),('kisi_sayisi','az'),('saat','gece')]),
        ("R09", [('ic_sicaklik','ideal'),('nem','cok_nemli')]),
        ("R10", [('ic_sicaklik','ideal'),('kisi_sayisi','cok')]),
        ("R11", [('ic_sicaklik','serin'),('dis_sicaklik','cok_soguk')]),
        ("R12", [('ic_sicaklik','serin'),('saat','sabah')]),
        ("R13", [('ic_sicaklik','serin'),('kisi_sayisi','az')]),
        ("R14", [('ic_sicaklik','soguk'),('dis_sicaklik','cok_soguk')]),
        ("R15", [('ic_sicaklik','soguk'),('dis_sicaklik','soguk')]),
        ("R16", [('ic_sicaklik','soguk'),('saat','gece')]),
        ("R17", [('ic_sicaklik','soguk'),('kisi_sayisi','cok')]),
        ("R18", [('nem','kuru'),('ic_sicaklik','ilik')]),
        ("R19", [('saat','oglen'),('dis_sicaklik','sicak'),('ic_sicaklik','ilik')]),
        ("R20", [('saat','aksam'),('ic_sicaklik','ideal'),('kisi_sayisi','orta')]),
    ]

    for rid, terms in rule_specs:
        # Mamdani: AND = min
        strength = min(mu[v][t] for v, t in terms)
        if strength > 0.01:
            active.append((rid, strength))

    return sorted(active, key=lambda x: -x[1])


# ──────────────────────────────────────────────────────────────────────────────
# ARAYÜZ
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="main-title">🌡️ Akıllı HVAC Sistemi</div>
    <div class="subtitle">Bulanık Mantık Tabanlı İklimlendirme Kontrolcüsü</div>
</div>
<div class="hero-divider"></div>
""", unsafe_allow_html=True)

# Sidebar — Girişler
st.sidebar.markdown("""
<div style="text-align:center; padding:0.8rem 0 0.5rem 0;">
    <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:-0.5px;">⚙️ Kontrol Paneli</div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:#64748b; letter-spacing:2px; text-transform:uppercase; margin-top:0.3rem;">Giriş Parametreleri</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

ic_s_val   = st.sidebar.slider("🏠 İç Sıcaklık (°C)",   0.0, 40.0, 23.0, 0.5)
dis_s_val  = st.sidebar.slider("🌍 Dış Sıcaklık (°C)", -10.0, 45.0, 20.0, 0.5)
nm_val     = st.sidebar.slider("💧 Nem (%)",            0,   100,   50,   1)
ks_val     = st.sidebar.slider("👥 Kişi Sayısı",        0,   10,    3,    1)
st_val     = st.sidebar.slider("🕐 Günün Saati",        0,   23,    14,   1)

st.sidebar.markdown("---")
hesapla = st.sidebar.button("🚀 HESAPLA", use_container_width=True, type="primary")

auto_mode = st.sidebar.checkbox("⚡ Otomatik (anlık) hesapla", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#475569; text-align:center; line-height:1.6;">
    💡 Slider'ları oynatarak<br>sistemin tepkisini gözlemleyin
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SİMÜLASYON
# ──────────────────────────────────────────────────────────────────────────────
if hesapla or auto_mode:
    try:
        hvac_sim.input['ic_sicaklik']   = ic_s_val
        hvac_sim.input['dis_sicaklik']  = dis_s_val
        hvac_sim.input['nem']           = nm_val
        hvac_sim.input['kisi_sayisi']   = ks_val
        hvac_sim.input['saat']          = st_val
        hvac_sim.compute()

        fan_out = hvac_sim.output.get('fan_hizi', 0.0)
        guc_out = hvac_sim.output.get('isi_guc', 0.0)
        sim_ok  = True
    except Exception as e:
        sim_ok = False
        st.error(f"Hesaplama hatası: {e}")
        fan_out, guc_out = 0.0, 0.0

    # ── LOG KAYDI ── (sadece HESAPLA butonuna basıldığında)
    if sim_ok and hesapla:
        current_inputs = (ic_s_val, dis_s_val, nm_val, ks_val, st_val)
        if True:
            st.session_state.prev_inputs = current_inputs
            st.session_state.log_counter += 1

            mode_str = "SOĞUTMA" if guc_out < -10 else ("ISITMA" if guc_out > 10 else "BEKLEMEDE")
            active_r = calculate_active_rules(current_inputs)
            active_rule_names = ", ".join([rid for rid, _ in active_r[:5]])
            top_strength = active_r[0][1] if active_r else 0.0

            log_entry = {
                'no': st.session_state.log_counter,
                'zaman': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                'tarih': datetime.now().strftime('%Y-%m-%d'),
                'ic_sicaklik': ic_s_val,
                'dis_sicaklik': dis_s_val,
                'nem': nm_val,
                'kisi_sayisi': ks_val,
                'saat': st_val,
                'fan_hizi': round(fan_out, 2),
                'isi_guc': round(guc_out, 2),
                'mod': mode_str,
                'aktif_kurallar': active_rule_names,
                'max_ateslenme': round(top_strength, 4),
            }
            st.session_state.logs.append(log_entry)

    # ── Çıkış kartları
    if sim_ok:
        mode_emoji = "❄️" if guc_out < -10 else ("🔥" if guc_out > 10 else "⏸️")
        mode_text  = "SOĞUTMA" if guc_out < -10 else ("ISITMA" if guc_out > 10 else "BEKLEMEDE")
        mode_css   = "metric-card-cool" if guc_out < -10 else ("metric-card-heat" if guc_out > 10 else "metric-card-idle")

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            st.markdown(f"""
            <div class="metric-card {mode_css}">
                <div class="metric-label">{mode_emoji} Çalışma Modu</div>
                <div class="metric-value">{mode_text}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">💨 Fan Hızı</div>
                <div class="metric-value">{fan_out:.1f}<span style="font-size:0.9rem;color:#64748b;"> %</span></div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⚡ Isıtma / Soğutma Gücü</div>
                <div class="metric-value">{guc_out:+.1f}<span style="font-size:0.9rem;color:#64748b;"> birim</span></div>
            </div>""", unsafe_allow_html=True)

        st.markdown("##")

        # ── Çıkış grafikleri
        st.markdown('<div class="section-header"><span class="section-tag">Defuzzification</span>📊 Durulaştırma — Centroid Yöntemi</div>', unsafe_allow_html=True)
        og1, og2 = st.columns(2)
        with og1:
            st.pyplot(plot_output(fan_hizi, fan_out, "Fan Hızı — Çıkış Üyelik Fonksiyonu", "#0ea5e9"))
        with og2:
            st.pyplot(plot_output(isi_guc, guc_out, "Isıtma/Soğutma Gücü — Çıkış Üyelik Fonksiyonu", "#ec4899"))

        # ── Aktif kurallar
        st.markdown('<div class="section-header"><span class="section-tag">Rule Activation</span>🎯 Aktif Kurallar — Ateşlenme Güçleri</div>', unsafe_allow_html=True)
        active_rules = calculate_active_rules((ic_s_val, dis_s_val, nm_val, ks_val, st_val))

        if not active_rules:
            st.warning("Hiçbir kural aktif değil. Giriş değerlerini kontrol edin.")
        else:
            cols = st.columns(2)
            for i, (rid, strength) in enumerate(active_rules):
                rule_text = next((r for r in RULES_TEXT if r.startswith(rid)), rid)
                bar = "█" * int(strength * 20) + "░" * (20 - int(strength * 20))
                cols[i % 2].markdown(
                    f'<div class="rule-box">{rule_text}<br>'
                    f'<span class="rule-strength">[{bar}] {strength:.3f}</span></div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")

        # ── CANLI LOG PANELİ ──
        st.markdown('<div class="section-header"><span class="section-tag">System Log</span>📋 Anlık Çalışma Logu</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="log-counter">Toplam kayıt: {len(st.session_state.logs)} | '
            f'Son güncelleme: {datetime.now().strftime("%H:%M:%S")}</div>',
            unsafe_allow_html=True
        )

        if st.session_state.logs:
            # Son 5 log girişini canlı göster
            st.markdown("#### Son İşlemler")
            recent_logs = list(reversed(st.session_state.logs[-5:]))
            for entry in recent_logs:
                if entry['mod'] == 'SOĞUTMA':
                    css_class = 'log-entry log-entry-cool'
                    badge_class = 'badge-cool'
                elif entry['mod'] == 'ISITMA':
                    css_class = 'log-entry log-entry-heat'
                    badge_class = 'badge-heat'
                else:
                    css_class = 'log-entry log-entry-idle'
                    badge_class = 'badge-idle'

                st.markdown(
                    f'<div class="{css_class}">'
                    f'<span class="log-badge {badge_class}">#{entry["no"]:03d}</span>'
                    f'<strong>[{entry["zaman"]}]</strong> '
                    f'İç:{entry["ic_sicaklik"]}°C  Dış:{entry["dis_sicaklik"]}°C  '
                    f'Nem:{entry["nem"]}%  Kişi:{entry["kisi_sayisi"]}  Saat:{entry["saat"]}  '
                    f'→  Fan:<strong>{entry["fan_hizi"]}%</strong>  '
                    f'Güç:<strong>{entry["isi_guc"]:+.1f}</strong>  '
                    f'[{entry["mod"]}] '
                    f'Kurallar: {entry["aktif_kurallar"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # Tam log tablosu
            with st.expander(f"📊 Tam Log Tablosu ({len(st.session_state.logs)} kayıt)"):
                log_df = pd.DataFrame(st.session_state.logs)
                log_df.columns = [
                    'No', 'Zaman', 'Tarih', 'İç °C', 'Dış °C', 'Nem %',
                    'Kişi', 'Saat', 'Fan %', 'Güç', 'Mod',
                    'Aktif Kurallar', 'Max Ateşlenme'
                ]
                st.dataframe(log_df, use_container_width=True, hide_index=True)

            # İndirme ve Temizleme
            log_col1, log_col2, log_col3 = st.columns([2, 1, 1])
            with log_col1:
                csv_df = pd.DataFrame(st.session_state.logs)
                csv_data = csv_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 Logları CSV Olarak İndir",
                    data=csv_data,
                    file_name=f"hvac_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime='text/csv',
                    use_container_width=True
                )
            with log_col2:
                if st.button("🗑️ Logları Temizle", use_container_width=True):
                    st.session_state.logs = []
                    st.session_state.log_counter = 0
                    st.session_state.prev_inputs = None
                    st.rerun()
            with log_col3:
                st.metric("Toplam İşlem", st.session_state.log_counter)
        else:
            st.info("Henüz log kaydı yok. Slider'ları hareket ettirin veya HESAPLA butonuna basın.")

        st.markdown("---")

# ──────────────────────────────────────────────────────────────────────────────
# ÜYELİK FONKSİYONLARI
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header"><span class="section-tag">Membership Functions</span>📈 Giriş Değişkenleri — Üyelik Fonksiyonları</div>', unsafe_allow_html=True)

PALETTE_BLUE   = ['#0ea5e9', '#22d3ee', '#10b981', '#f59e0b', '#ef4444']
PALETTE_TEAL   = ['#06b6d4', '#0ea5e9', '#6366f1', '#ef4444']
PALETTE_PURPLE = ['#a855f7', '#6366f1', '#0ea5e9', '#10b981']
PALETTE_PINK   = ['#ec4899', '#f59e0b', '#10b981']
PALETTE_AMBER  = ['#1e293b', '#f59e0b', '#fbbf24', '#a855f7']

mc1, mc2 = st.columns(2)
with mc1:
    st.pyplot(plot_membership(ic_sicaklik, ic_s_val,  "İç Sıcaklık (°C)", PALETTE_BLUE))
    st.pyplot(plot_membership(nem,         nm_val,    "Nem (%)",         PALETTE_PURPLE))
    st.pyplot(plot_membership(saat,        st_val,    "Günün Saati",     PALETTE_AMBER))
with mc2:
    st.pyplot(plot_membership(dis_sicaklik, dis_s_val, "Dış Sıcaklık (°C)", PALETTE_TEAL))
    st.pyplot(plot_membership(kisi_sayisi,  ks_val,    "Kişi Sayısı",       PALETTE_PINK))

# ──────────────────────────────────────────────────────────────────────────────
# TEST SENARYOLARI
# ──────────────────────────────────────────────────────────────────────────────
with st.expander("🧪 Test Senaryoları (10 senaryo — sistemin davranışını gözleyin)"):
    senaryolar = [
        ("Yaz öğleni, kalabalık salon",     35, 38, 70, 8, 14),
        ("Kış gecesi, az kişi",              12, -5, 40, 1, 2),
        ("İdeal bahar günü",                 22, 20, 50, 3, 11),
        ("Sıcak ve çok nemli (tropikal)",    32, 30, 92, 4, 15),
        ("Kuru ve ılık sonbahar",            27, 18, 22, 2, 10),
        ("Soğuk sabah, kalabalık ofis",      15, 5,  45, 7, 8),
        ("Akşam, ideal sıcaklık",            23, 22, 55, 4, 19),
        ("Aşırı sıcak, terk edilmiş oda",    34, 38, 60, 0, 16),
        ("Buz gibi, kimse yok",              8,  -8, 35, 0, 4),
        ("Serin sabah, az kişi",             18, 10, 50, 2, 7),
    ]

    rows = []
    sim_test = ctrl.ControlSystemSimulation(hvac_ctrl)
    for ad, ics, diss, nms, kss, sts in senaryolar:
        try:
            sim_test.input['ic_sicaklik']   = ics
            sim_test.input['dis_sicaklik']  = diss
            sim_test.input['nem']           = nms
            sim_test.input['kisi_sayisi']   = kss
            sim_test.input['saat']          = sts
            sim_test.compute()
            f = sim_test.output.get('fan_hizi', 0)
            g = sim_test.output.get('isi_guc',  0)
            mod = "Soğutma" if g < -10 else ("Isıtma" if g > 10 else "Beklemede")
            rows.append([ad, ics, diss, nms, kss, sts, f"{f:.1f}%", f"{g:+.1f}", mod])
        except Exception:
            rows.append([ad, ics, diss, nms, kss, sts, "—", "—", "Hata"])

    df = pd.DataFrame(rows, columns=[
        "Senaryo", "İç °C", "Dış °C", "Nem %", "Kişi", "Saat",
        "Fan Hızı", "Güç", "Mod"
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────────────────────────────────────
# SİSTEM DOKÜMANTASYONU
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header"><span class="section-tag">Documentation</span>📐 Sistem Dokümantasyonu</div>', unsafe_allow_html=True)

# ── Sistem İstatistikleri ──
stat1, stat2, stat3, stat4 = st.columns(4)
with stat1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">📏 Toplam Kural</div>
        <div class="metric-value">20</div>
    </div>""", unsafe_allow_html=True)
with stat2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">📥 Giriş Değişkeni</div>
        <div class="metric-value">5</div>
    </div>""", unsafe_allow_html=True)
with stat3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">📤 Çıkış Değişkeni</div>
        <div class="metric-value">2</div>
    </div>""", unsafe_allow_html=True)
with stat4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">🏷️ Dilsel Terim</div>
        <div class="metric-value">29</div>
    </div>""", unsafe_allow_html=True)

st.markdown("##")

# ── Değişken Tanımları ──
with st.expander("📊 Giriş ve Çıkış Değişkenleri — Dilsel Terimler ve Evrenler"):
    st.markdown("#### 📥 Giriş Değişkenleri (5 değişken, 19 dilsel terim)")
    giris_df = pd.DataFrame([
        ["1", "İç Sıcaklık", "°C", "0 – 40", "soğuk, serin, ideal, ılık, sıcak", "5", "trapmf, trimf, trimf, trimf, trapmf"],
        ["2", "Dış Sıcaklık", "°C", "-10 – 45", "çok_soğuk, soğuk, ılıman, sıcak", "4", "trapmf, trimf, trimf, trapmf"],
        ["3", "Nem", "%", "0 – 100", "kuru, normal, nemli, çok_nemli", "4", "trapmf, trimf, trimf, trapmf"],
        ["4", "Kişi Sayısı", "kişi", "0 – 10", "az, orta, çok", "3", "trimf, trimf, trapmf"],
        ["5", "Günün Saati", "saat", "0 – 23", "gece, sabah, öğlen, akşam", "4", "trapmf, trimf, trimf, trapmf"],
    ], columns=["#", "Değişken", "Birim", "Evren (Aralık)", "Dilsel Terimler", "Terim Sayısı", "Üyelik Fonk. Tipleri"])
    st.dataframe(giris_df, use_container_width=True, hide_index=True)

    st.markdown("#### 📤 Çıkış Değişkenleri (2 değişken, 10 dilsel terim)")
    cikis_df = pd.DataFrame([
        ["1", "Fan Hızı", "%", "0 – 100", "kapalı, düşük, orta, yüksek, maksimum", "5", "trimf, trimf, trimf, trimf, trapmf"],
        ["2", "Isıtma/Soğutma Gücü", "birim", "-100 – +100", "güçlü_soğutma, soğutma, kapalı, ısıtma, güçlü_ısıtma", "5", "trapmf, trimf, trimf, trimf, trapmf"],
    ], columns=["#", "Değişken", "Birim", "Evren (Aralık)", "Dilsel Terimler", "Terim Sayısı", "Üyelik Fonk. Tipleri"])
    st.dataframe(cikis_df, use_container_width=True, hide_index=True)

    st.markdown("""
    > **Toplam:** 5 giriş + 2 çıkış = **7 değişken** | 19 giriş terimi + 10 çıkış terimi = **29 dilsel terim**
    """)

# ── Kural Tabanı ──
with st.expander("📜 Kural Tabanı — 20 IF-THEN Kuralı (Açıklamalı)"):
    st.markdown("""
    Bulanık mantık kuralları **Mamdani** çıkarım yöntemiyle çalışır.
    Birden fazla koşul **AND (∧)** operatörü ile birleştirilir → **minimum** fonksiyonu uygulanır.
    """)

    kural_verileri = [
        ["R01", "İç Sıcaklık = SICAK ∧ Dış Sıcaklık = SICAK ∧ Kişi = ÇOK",
         "Fan = MAKSİMUM, Güç = GÜÇLÜ_SOĞUTMA",
         "Hem içerisi hem dışarısı sıcak ve kalabalık ortamda sistemi tam kapasite soğutmaya geçirir."],
        ["R02", "İç Sıcaklık = SICAK ∧ Nem = ÇOK_NEMLİ",
         "Fan = MAKSİMUM, Güç = GÜÇLÜ_SOĞUTMA",
         "Sıcak ve bunaltıcı nemli havada maksimum soğutma ile konfor sağlanır."],
        ["R03", "İç Sıcaklık = SICAK ∧ Dış Sıcaklık = ILIMAN",
         "Fan = YÜKSEK, Güç = SOĞUTMA",
         "İçerisi sıcak ama dışarısı ılıman olduğunda orta-yüksek seviyede soğutma yeterlidir."],
        ["R04", "İç Sıcaklık = ILIK ∧ Kişi = ÇOK",
         "Fan = YÜKSEK, Güç = SOĞUTMA",
         "Ilık ortamda kalabalık kişi sayısı ısı yükünü artırdığı için soğutma devreye girer."],
        ["R05", "İç Sıcaklık = ILIK ∧ Nem = NEMLİ",
         "Fan = YÜKSEK, Güç = SOĞUTMA",
         "Ilık ve nemli ortamda hava sirkülasyonu artırılarak rahatsızlık giderilir."],
        ["R06", "İç Sıcaklık = ILIK ∧ Kişi = AZ ∧ Saat = GECE",
         "Fan = ORTA, Güç = KAPALI",
         "Gece saatlerinde ılık ama az kişili ortamda enerji tasarrufu için sadece fan çalışır."],
        ["R07", "İç Sıcaklık = İDEAL ∧ Kişi = ORTA",
         "Fan = DÜŞÜK, Güç = KAPALI",
         "İdeal sıcaklıkta orta kalabalıkla hafif hava sirkülasyonu yeterlidir."],
        ["R08", "İç Sıcaklık = İDEAL ∧ Kişi = AZ ∧ Saat = GECE",
         "Fan = KAPALI, Güç = KAPALI",
         "Gece, ideal sıcaklık ve az kişide sistem tamamen kapanarak enerji tasarrufu sağlar."],
        ["R09", "İç Sıcaklık = İDEAL ∧ Nem = ÇOK_NEMLİ",
         "Fan = ORTA, Güç = KAPALI",
         "Sıcaklık ideal olsa bile aşırı nem durumunda fan ile nem dengelenir."],
        ["R10", "İç Sıcaklık = İDEAL ∧ Kişi = ÇOK",
         "Fan = ORTA, Güç = KAPALI",
         "İdeal sıcaklıkta kalabalık ortamda fan ile hava kalitesi korunur, ısıtma/soğutma gerekmez."],
        ["R11", "İç Sıcaklık = SERİN ∧ Dış Sıcaklık = ÇOK_SOĞUK",
         "Fan = DÜŞÜK, Güç = ISITMA",
         "İçerisi serin, dışarısı çok soğuk olduğunda ısıtma ile konfor sağlanır."],
        ["R12", "İç Sıcaklık = SERİN ∧ Saat = SABAH",
         "Fan = DÜŞÜK, Güç = ISITMA",
         "Sabah saatlerinde serin ortamda hafif ısıtma ile güne konforlu başlanır."],
        ["R13", "İç Sıcaklık = SERİN ∧ Kişi = AZ",
         "Fan = DÜŞÜK, Güç = ISITMA",
         "Az kişili serin ortamda insan vücut ısısı yetersiz kalır, ısıtma devreye girer."],
        ["R14", "İç Sıcaklık = SOĞUK ∧ Dış Sıcaklık = ÇOK_SOĞUK",
         "Fan = ORTA, Güç = GÜÇLÜ_ISITMA",
         "Her iki taraf da soğuk olduğunda güçlü ısıtma ve orta fan ile hızlı ısınma sağlanır."],
        ["R15", "İç Sıcaklık = SOĞUK ∧ Dış Sıcaklık = SOĞUK",
         "Fan = DÜŞÜK, Güç = GÜÇLÜ_ISITMA",
         "İçerisi ve dışarısı soğukta güçlü ısıtma aktif, fan düşük tutularak ısı kaybı önlenir."],
        ["R16", "İç Sıcaklık = SOĞUK ∧ Saat = GECE",
         "Fan = DÜŞÜK, Güç = GÜÇLÜ_ISITMA",
         "Gece soğuk ortamda güçlü ısıtma ile uyku konforu sağlanır, fan düşük gürültü için."],
        ["R17", "İç Sıcaklık = SOĞUK ∧ Kişi = ÇOK",
         "Fan = ORTA, Güç = ISITMA",
         "Soğuk ortamda kalabalık kişi ısıya katkı sağlar, bu yüzden normal ısıtma yeterlidir."],
        ["R18", "Nem = KURU ∧ İç Sıcaklık = ILIK",
         "Fan = ORTA, Güç = SOĞUTMA",
         "Kuru ve ılık havada fan ile hava dolaşımı sağlanır, hafif soğutma uygulanır."],
        ["R19", "Saat = ÖĞLEN ∧ Dış Sıcaklık = SICAK ∧ İç Sıcaklık = ILIK",
         "Fan = YÜKSEK, Güç = SOĞUTMA",
         "Öğlen saatlerinde dışarısı sıcakken ısı transferi artar, proaktif soğutma yapılır."],
        ["R20", "Saat = AKŞAM ∧ İç Sıcaklık = İDEAL ∧ Kişi = ORTA",
         "Fan = DÜŞÜK, Güç = KAPALI",
         "Akşam saatlerinde ideal ortamda enerji tasarrufu moduna geçilir."],
    ]

    kural_df = pd.DataFrame(kural_verileri, columns=[
        "Kural No", "IF (Koşul)", "THEN (Sonuç)", "Açıklama"
    ])
    st.dataframe(kural_df, use_container_width=True, hide_index=True, height=740)

    st.markdown("---")

    # Kuralları görsel olarak da göster
    st.markdown("#### 🔍 Kuralların IF-THEN Gösterimi")
    for i, row in enumerate(kural_verileri):
        rid, kosul, sonuc, aciklama = row
        st.markdown(
            f'<div class="rule-box">'
            f'<strong>{rid}:</strong> '
            f'<span style="color:#22d3ee">IF</span> {kosul} '
            f'<span style="color:#fbbf24">THEN</span> {sonuc}<br>'
            f'<span style="font-size:0.75rem; color:#94a3b8">💡 {aciklama}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

# ── Metodoloji ──
with st.expander("ℹ️ Metodoloji ve Sistem Bilgisi"):
    st.markdown("""
    #### ⚙️ Bulanık Çıkarım Sistemi Yapılandırması

    | Parametre | Değer |
    |---|---|
    | **Çıkarım Yöntemi** | Mamdani |
    | **Bulanıklaştırma** | Üçgen (trimf) ve Yamuk (trapmf) üyelik fonksiyonları |
    | **AND operatörü** | Minimum (∧) |
    | **OR operatörü** | Maksimum (∨) |
    | **Toplama (Aggregation)** | Maksimum |
    | **Durulaştırma** | Centroid (ağırlık merkezi) |

    #### 📦 Kullanılan Kütüphaneler

    | Kütüphane | Amaç |
    |---|---|
    | `scikit-fuzzy` | Bulanık mantık motoru, üyelik fonksiyonları, kural sistemi |
    | `numpy` | Sayısal hesaplamalar, evren dizileri |
    | `matplotlib` | Üyelik fonksiyonu ve durulaştırma grafikleri |
    | `streamlit` | Web tabanlı interaktif arayüz (GUI) |
    | `pandas` | Veri tabloları, log yönetimi, CSV dışa aktarma |

    #### 🧠 Neden Bulanık Mantık?

    HVAC sistemi **belirsiz ve sürekli değişen koşullarla** çalışır:
    - Sıcaklık, nem gibi değişkenler kesin eşik değerleriyle değil, *kademeli geçişlerle* değişir
    - "Sıcak", "nemli", "kalabalık" gibi **dilsel terimler** insan algısını doğrudan modellemeye uygundur
    - Klasik PID kontrolcülere kıyasla, **uzman bilgisi** doğrudan kural tabanına aktarılabilir
    - Birden fazla girişin etkileşimini **IF-THEN kuralları** ile doğal dilde ifade etmek mümkündür
    - Centroid durulaştırma ile **yumuşak, kademeli geçişler** sağlanarak ani açma/kapama önlenir
    """)

st.markdown("""
<div class="footer-text">
    📚 Bulanık Mantık Dersi — Dönem Projesi<br>
    Mersin Üniversitesi &nbsp;·&nbsp; Furkan Fatih Çiftçi &nbsp;·&nbsp; 22430070037
</div>
""", unsafe_allow_html=True)
