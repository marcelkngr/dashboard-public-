# ============================================================
# Online Retail II – Executive Dashboard
# Starten mit:  streamlit run dashboard.py
# ============================================================

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="Online Retail Dashboard", page_icon="🛒", layout="wide")

# ── ÜBERSETZUNGEN ────────────────────────────────────────────
TEXTE = {
    "DE": {
        "titel":           "Online Retail Analytics - Königer Marcel 6624026",
        "untertitel":      "Executive Dashboard · UCI Online Retail II · 2009–2011 · Großbritannien",
        "von":             "VON",
        "bis":             "BIS",
        "kunde_filter":    "KUNDE FILTERN",
        "alle_kunden":     "Alle Kunden",
        "top10_kunden":    "Top 10 Kunden",
        "kunden_suche":    "Kunden-ID eingeben",
        "gesamtumsatz":    "Gesamtumsatz",
        "gesamt_sub":      "2009–2011 gesamt",
        "bester_monat":    "Bester Monat",
        "wachstum":        "Wachstum 2010→2011",
        "jahresvergleich": "Jahresvergleich",
        "bestellungen":    "Bestellungen",
        "kunden":          "Kunden",
        "produkte":        "verschiedene Produkte",
        "umsatz_2009":     "UMSATZ 2009",
        "umsatz_2010":     "UMSATZ 2010",
        "umsatz_2011":     "UMSATZ 2011",
        "basisjahr":       "Bestellungen · Basisjahr",
        "vs_2009":         "Bestellungen · vs. 2009",
        "vs_2010":         "Bestellungen · vs. 2010",
        "insight1_titel":  "Umsatzentwicklung",
        "insight1_text":   "Bester Monat: {mon} · £{val}K\n{over} von {total} Monaten über Durchschnitt",
        "insight2_titel":  "Internationale Märkte",
        "insight2_text":   "Großbritannien: {uk:.0f}% des Umsatzes\nStärkstes Exportland: {land}",
        "insight3_titel":  "Kundensegmente",
        "insight3_text":   "Größtes Segment: {seg} ({n:,} Kunden)\nChampions-Anteil: {pct:.0f}%",
        "insight4_titel":  "Warenkorbanalyse",
        "insight4_text":   "Häufigstes Produktpaar: {sup:.2f}% Support\nCross-Selling-Potential identifiziert",
        "mon_umsatz":      "Monatlicher Umsatz 2009–2011",
        "mon_sub":         "Balken = Monatsumsatz · Linie = 3M-Gleitmittel",
        "yoy_titel":       "Jährliches Umsatzwachstum (2010 → 2011)",
        "yoy_sub":         "YoY in % · grün = Wachstum · rot = Rückgang · gestrichelt = CAGR {cagr:+.1f}% p.a.",
        "saison_mon":      "Saisonalität – Umsatz nach Monat",
        "saison_mon_sub":  "Gesamtumsatz pro Monat · stärkster Monat: {mon}",
        "saison_q":        "Saisonalität – Umsatz nach Quartal",
        "saison_q_sub":    "Gesamtumsatz pro Quartal · 2009–2011",
        "top_laender":     "Top 10 Länder nach Umsatz",
        "top_laender_sub": "Umsatz in £ · ohne Großbritannien",
        "top_produkte":    "Top 10 Produkte nach Umsatz",
        "top_prod_sub":    "Gesamtumsatz pro Produkt in £",
        "rfm_titel":       "RFM-Kundensegmentierung – Detailansicht",
        "rfm_sub":         "Ø Kennzahlen pro Segment · Recency in Rot = über 200 Tage inaktiv",
        "seg":             "SEGMENT",
        "kunden_%":        "KUNDEN %",
        "recency":         "Ø RECENCY",
        "frequency":       "Ø FREQUENCY",
        "monetary":        "Ø MONETARY",
        "prio_titel":      "Prioritäten: Gefährdete reaktivieren, Champions schützen",
        "prio_sub":        "Handlungsempfehlungen je Segment",
        "warenkorb":       "Top 10 Produktpaare – Warenkorbanalyse",
        "warenkorb_sub":   "Support = % aller Bestellungen mit diesem Produktpaar · Ziel: Cross-Selling",
        "footer":          "UCI Online Retail II · 2009–2011 · BBA Datenaufbereitung und -verarbeitung · DuckDB",
        "monate_label":    ["Jan","Feb","Mär","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"],
        "empfehlungen": [
            ("Champions",       "#2a5298", "Belohnen und binden. Exklusiv-Angebote, Early Access, persönliche Betreuung."),
            ("Loyal Customers", "#4a7ab5", "Upselling und Cross-Selling. Neue Kategorien vorstellen, Treueprogramm anbieten."),
            ("Recent Customers","#e8792f", "Onboarding optimieren. Willkommensserie, Zweitkauf-Incentive, Produktempfehlungen."),
            ("Needs Attention", "#c0392b", "Reaktivierung mit personalisierten Angeboten. Regelmäßige Touchpoints."),
            ("At Risk",         "#c0392b", "Sofort reaktivieren! Win-Back-Kampagnen, persönliche Ansprache, Sonderkonditionen."),
            ("Lost",            "#888880", "Letzte Chance: einmalige Reaktivierungsaktion. Bei Misserfolg aus CRM entfernen."),
        ],
    },
    "EN": {
        "titel":           "Online Retail Analytics",
        "untertitel":      "Executive Dashboard · UCI Online Retail II · 2009–2011 · United Kingdom",
        "von":             "FROM",
        "bis":             "TO",
        "kunde_filter":    "FILTER CUSTOMER",
        "alle_kunden":     "All Customers",
        "top10_kunden":    "Top 10 Customers",
        "kunden_suche":    "Enter Customer ID",
        "gesamtumsatz":    "Total Revenue",
        "gesamt_sub":      "2009–2011 total",
        "bester_monat":    "Best Month",
        "wachstum":        "Growth 2010→2011",
        "jahresvergleich": "Year-over-year",
        "bestellungen":    "Orders",
        "kunden":          "Customers",
        "produkte":        "different products",
        "umsatz_2009":     "REVENUE 2009",
        "umsatz_2010":     "REVENUE 2010",
        "umsatz_2011":     "REVENUE 2011",
        "basisjahr":       "Orders · Base year",
        "vs_2009":         "Orders · vs. 2009",
        "vs_2010":         "Orders · vs. 2010",
        "insight1_titel":  "Revenue Development",
        "insight1_text":   "Best month: {mon} · £{val}K\n{over} of {total} months above average",
        "insight2_titel":  "International Markets",
        "insight2_text":   "United Kingdom: {uk:.0f}% of revenue\nStrongest export market: {land}",
        "insight3_titel":  "Customer Segments",
        "insight3_text":   "Largest segment: {seg} ({n:,} customers)\nChampions share: {pct:.0f}%",
        "insight4_titel":  "Basket Analysis",
        "insight4_text":   "Most frequent product pair: {sup:.2f}% support\nCross-selling potential identified",
        "mon_umsatz":      "Monthly Revenue 2009–2011",
        "mon_sub":         "Bars = monthly revenue · Line = 3M moving average",
        "yoy_titel":       "Annual Revenue Growth (2010 → 2011)",
        "yoy_sub":         "YoY in % · green = growth · red = decline · dashed = CAGR {cagr:+.1f}% p.a.",
        "saison_mon":      "Seasonality – Revenue by Month",
        "saison_mon_sub":  "Total revenue per month · strongest month: {mon}",
        "saison_q":        "Seasonality – Revenue by Quarter",
        "saison_q_sub":    "Total revenue per quarter · 2009–2011",
        "top_laender":     "Top 10 Countries by Revenue",
        "top_laender_sub": "Revenue in £ · excl. United Kingdom",
        "top_produkte":    "Top 10 Products by Revenue",
        "top_prod_sub":    "Total revenue per product in £",
        "rfm_titel":       "RFM Customer Segmentation – Detail View",
        "rfm_sub":         "Avg. metrics per segment · Recency in red = inactive 200+ days",
        "seg":             "SEGMENT",
        "kunden_%":        "CUSTOMERS %",
        "recency":         "AVG RECENCY",
        "frequency":       "AVG FREQUENCY",
        "monetary":        "AVG MONETARY",
        "prio_titel":      "Priorities: Reactivate At-Risk, Protect Champions",
        "prio_sub":        "Action recommendations per segment",
        "warenkorb":       "Top 10 Product Pairs – Basket Analysis",
        "warenkorb_sub":   "Support = % of all orders containing this product pair · Goal: Cross-selling",
        "footer":          "UCI Online Retail II · 2009–2011 · BBA Data Processing · DuckDB",
        "monate_label":    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
        "empfehlungen": [
            ("Champions",       "#2a5298", "Reward and retain. Exclusive offers, early access, personal service. Highest priority."),
            ("Loyal Customers", "#4a7ab5", "Upselling and cross-selling. Introduce new categories, offer loyalty program."),
            ("Recent Customers","#e8792f", "Optimize onboarding. Welcome series, second-purchase incentive, product recommendations."),
            ("Needs Attention", "#c0392b", "Reactivate with personalized offers. Regular touchpoints, bundle deals."),
            ("At Risk",         "#c0392b", "Reactivate immediately! Win-back campaigns, personal outreach, special conditions."),
            ("Lost",            "#888880", "Last chance: one-time reactivation. Remove from active CRM if unsuccessful."),
        ],
    },
}

# ── STYLING ──────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    .stApp { background-color: #f8f8f6; color: #1a1a1a; font-family: 'Inter', sans-serif; }
    .block-container { padding: 3rem 2.5rem 4rem 2.5rem; max-width: 1400px; }
    [data-testid="stSidebar"] { display: none; }
    .dash-title { font-size:22px; font-weight:800; color:#1a1a1a; margin-bottom:2px; }
    .dash-sub   { font-size:12px; color:#aaaaaa; margin-top:0; letter-spacing:0.03em; }
    .dash-meta  { font-size:11px; color:#aaaaaa; text-align:right; margin-top:-28px; }
    .header-divider { border:none; border-top:1px solid #e0e0dc; margin:12px 0 20px 0; }
    .kpi-card { background:#ffffff; border:1px solid #e8e8e0; border-radius:6px; padding:20px 22px 14px 22px; }
    .kpi-eyebrow { font-size:10px; font-weight:600; letter-spacing:0.1em; color:#aaaaaa; text-transform:uppercase; margin-bottom:6px; }
    .kpi-value   { font-size:32px; font-weight:800; color:#1a1a1a; line-height:1.0; margin-bottom:2px; }
    .kpi-sub     { font-size:11px; color:#aaaaaa; margin-bottom:10px; }
    .insights-row { display:flex; gap:16px; margin-bottom:24px; }
    .insight-box { flex:1; background:#ffffff; border:1px solid #e8e8e0; border-left:3px solid #e8792f; border-radius:6px; padding:14px 16px; }
    .insight-num   { font-size:18px; font-weight:800; color:#e8792f; margin-bottom:4px; }
    .insight-title { font-size:13px; font-weight:700; color:#1a1a1a; margin-bottom:3px; }
    .insight-text  { font-size:11px; color:#888880; line-height:1.4; }
    .chart-card { background:#ffffff; border:1px solid #e8e8e0; border-radius:6px; padding:20px 22px 8px 22px; margin-bottom:16px; }
    .chart-title    { font-size:14px; font-weight:700; color:#1a1a1a; margin-bottom:2px; }
    .chart-subtitle { font-size:11px; color:#aaaaaa; margin-bottom:8px; }
    .section-divider { border:none; border-top:1px solid #e0e0dc; margin:28px 0 20px 0; }
    .lang-btn { display:inline-block; padding:4px 10px; border-radius:4px; font-size:11px; font-weight:700; cursor:pointer; }
    [data-testid="metric-container"] { display:none; }
</style>
""", unsafe_allow_html=True)

BLAU      = "#2a5298"
BLAU_HELL = "#c5d3ee"
ROT       = "#c0392b"
GRUEN     = "#2d7a52"
ORANGE    = "#e8792f"
GRAU      = "#cccccc"

def style(fig, height=380):
    fig.update_layout(
        height=height,
        plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
        font=dict(color="#1a1a1a", size=11, family="Inter, Arial, sans-serif"),
        title_text="",
        xaxis=dict(showgrid=True, gridcolor="#f0f0ea",
                   title_font=dict(color="#aaaaaa", size=10),
                   tickfont=dict(color="#888880"), linecolor="#e8e8e0", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#f0f0ea",
                   title_font=dict(color="#aaaaaa", size=10),
                   tickfont=dict(color="#888880"), linecolor="#e8e8e0", zeroline=False),
        legend=dict(font=dict(color="#1a1a1a", size=11), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=40, t=10, b=10),
    )
    return fig

# ── DATEN LADEN ──────────────────────────────────────────────
@st.cache_data
def lade_daten():
    df     = pd.read_csv("online_retail_cleaned.csv.gz", dtype={"Customer ID": str})
    rfm    = pd.read_csv("rfm_segments.csv",             dtype={"Customer ID": str})
    paare  = pd.read_csv("top_pairs.csv")
    sonder = pd.read_csv("sonderposten.csv")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df, rfm, paare, sonder

df, rfm, paare, sonder = lade_daten()

# ── HEADER + SPRACHAUSWAHL ───────────────────────────────────
c_title, c_lang = st.columns([4, 1])
with c_title:
    sprache = st.session_state.get("sprache", "DE")
    T = TEXTE[sprache]
    st.markdown(f"<div class='dash-title'>{T['titel']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='dash-sub'>{T['untertitel']}</div>", unsafe_allow_html=True)

with c_lang:
    st.markdown("<br>", unsafe_allow_html=True)
    col_de, col_en = st.columns(2)
    with col_de:
        if st.button("🇩🇪 DE", use_container_width=True,
                     type="primary" if st.session_state.get("sprache","DE") == "DE" else "secondary"):
            st.session_state["sprache"] = "DE"
            st.rerun()
    with col_en:
        if st.button("🇬🇧 EN", use_container_width=True,
                     type="primary" if st.session_state.get("sprache","DE") == "EN" else "secondary"):
            st.session_state["sprache"] = "EN"
            st.rerun()

sprache = st.session_state.get("sprache", "DE")
T = TEXTE[sprache]

st.markdown("<hr class='header-divider'>", unsafe_allow_html=True)

# ── FILTER ───────────────────────────────────────────────────
monate = sorted(df["YearMonth"].unique())
min_datum = pd.to_datetime(df["InvoiceDate"].min()).date()
max_datum = pd.to_datetime(df["InvoiceDate"].max()).date()

f1, f2, f3 = st.columns([2, 2, 4])

with f1:
    st.markdown(f"<p style='font-size:10px;font-weight:600;letter-spacing:0.1em;color:#aaa;text-transform:uppercase;margin-bottom:4px;'>{T['von']}</p>", unsafe_allow_html=True)
    von_datum = st.date_input("von", value=min_datum, min_value=min_datum, max_value=max_datum, label_visibility="collapsed")

with f2:
    st.markdown(f"<p style='font-size:10px;font-weight:600;letter-spacing:0.1em;color:#aaa;text-transform:uppercase;margin-bottom:4px;'>{T['bis']}</p>", unsafe_allow_html=True)
    bis_datum = st.date_input("bis", value=max_datum, min_value=min_datum, max_value=max_datum, label_visibility="collapsed")

von = pd.to_datetime(von_datum).to_period("M").strftime("%Y-%m")
bis = pd.to_datetime(bis_datum).to_period("M").strftime("%Y-%m")

with f3:
    fc1, fc2 = st.columns([1, 2])
    with fc1:
        st.markdown(f"<p style='font-size:10px;font-weight:600;letter-spacing:0.1em;color:#aaa;text-transform:uppercase;margin-bottom:4px;'>{T['kunde_filter']}</p>", unsafe_allow_html=True)
        kunden_modus = st.selectbox("kunden_modus",
            [T["alle_kunden"], T["top10_kunden"]],
            label_visibility="collapsed")
    with fc2:
        hint = "5-stellig z.B. 17841" if sprache == "DE" else "5-digit e.g. 17841"
        st.markdown(f"<p style='font-size:10px;font-weight:600;letter-spacing:0.1em;color:#aaa;text-transform:uppercase;margin-bottom:4px;'>{T['kunden_suche']} ({hint})</p>", unsafe_allow_html=True)
        kunden_suche = st.text_input("suche", placeholder="z.B. 17841" if sprache == "DE" else "e.g. 17841", label_visibility="collapsed", max_chars=5)
        if kunden_suche and (not kunden_suche.isdigit() or len(kunden_suche) != 5):
            st.error("⚠️ Bitte eine gültige 5-stellige Kunden-ID eingeben" if sprache == "DE" else "⚠️ Please enter a valid 5-digit customer ID")
            kunden_suche = ""

# Filter anwenden
df_f = df[(df["YearMonth"] >= von) & (df["YearMonth"] <= bis)].copy()

# Kunden-Filter
if kunden_suche and kunden_suche.isdigit() and len(kunden_suche) == 5:
    df_f = df_f[df_f["Customer ID"] == kunden_suche.strip()]
elif kunden_modus == T["top10_kunden"]:
    top10_ids = (df_f.groupby("Customer ID")["TotalPrice"].sum()
                 .sort_values(ascending=False).head(10).index)
    df_f = df_f[df_f["Customer ID"].isin(top10_ids)]

st.markdown("<br>", unsafe_allow_html=True)

# ── BERECHNUNGEN ─────────────────────────────────────────────
umsatz       = df_f["TotalPrice"].sum()
bestellungen = df_f["Invoice"].nunique()
kunden_n     = df_f["Customer ID"].nunique()
produkte_n   = df_f["Description"].nunique()
avg_order    = umsatz / bestellungen if bestellungen > 0 else 0

monatlich    = df_f.groupby("YearMonth")["TotalPrice"].sum().reset_index()
monatlich.columns = ["Monat", "Umsatz"]
avg_u        = monatlich["Umsatz"].mean()
best_mon     = monatlich.loc[monatlich["Umsatz"].idxmax(), "Monat"]
best_val     = monatlich["Umsatz"].max()

df_2010 = df_f[df_f["YearMonth"].str.startswith("2010")]["TotalPrice"].sum()
df_2011 = df_f[df_f["YearMonth"].str.startswith("2011")]["TotalPrice"].sum()
yoy     = ((df_2011 - df_2010) / df_2010 * 100) if df_2010 > 0 else 0
yoy_str = f"▲ +{yoy:.1f}%" if yoy >= 0 else f"▼ {yoy:.1f}%"
yoy_col = GRUEN if yoy >= 0 else ROT

land_daten = df_f.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False).reset_index()
land_daten.columns = ["Land", "Umsatz"]
uk_key     = "United Kingdom"
uk_anteil  = (land_daten[land_daten["Land"] == uk_key]["Umsatz"].values[0] / umsatz * 100) if len(land_daten[land_daten["Land"] == uk_key]) > 0 else 0
land_ohne_uk = land_daten[land_daten["Land"] != uk_key]
top_export = land_ohne_uk.iloc[0]["Land"] if len(land_ohne_uk) > 0 else "–"

seg_anzahl  = rfm["Segment"].value_counts().reset_index()
seg_anzahl.columns = ["Segment", "Anzahl"]
champ_n     = seg_anzahl[seg_anzahl["Segment"] == "Champions"]["Anzahl"].values
champ_pct   = (champ_n[0] / seg_anzahl["Anzahl"].sum() * 100) if len(champ_n) > 0 else 0
top_seg_lbl = seg_anzahl.iloc[0]["Segment"]
top_seg_n   = seg_anzahl.iloc[0]["Anzahl"]
top_support = paare.iloc[0]["Support"]

# ── KPI-KARTEN ───────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-eyebrow'>{T['gesamtumsatz']}</div><div class='kpi-value'>£{umsatz/1e6:.2f} Mio.</div><div class='kpi-sub'>{T['gesamt_sub']}</div></div>", unsafe_allow_html=True)

with k2:
    st.markdown(f"<div class='kpi-card'><div class='kpi-eyebrow'>{T['bester_monat']}</div><div class='kpi-value'>£{best_val/1e3:.0f}K</div><div class='kpi-sub'>{best_mon}</div></div>", unsafe_allow_html=True)

with k3:
    st.markdown(f"<div class='kpi-card'><div class='kpi-eyebrow'>{T['wachstum']}</div><div class='kpi-value' style='color:{yoy_col};'>{yoy_str}</div><div class='kpi-sub'>{T['jahresvergleich']}</div></div>", unsafe_allow_html=True)

with k4:
    st.markdown(f"<div class='kpi-card'><div class='kpi-eyebrow'>{T['bestellungen']}</div><div class='kpi-value'>{bestellungen:,}</div><div class='kpi-sub'>Ø £{avg_order:,.0f}</div></div>", unsafe_allow_html=True)

with k5:
    st.markdown(f"<div class='kpi-card'><div class='kpi-eyebrow'>{T['kunden']}</div><div class='kpi-value'>{kunden_n:,}</div><div class='kpi-sub'>{produkte_n:,} {T['produkte']}</div></div>", unsafe_allow_html=True)

# ── INSIGHT-BOXEN ────────────────────────────────────────────
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
over_avg = (monatlich["Umsatz"] >= avg_u).sum()

val_k = f"{best_val/1e3:.0f}"
st.markdown(f"""
<div class='insights-row'>
    <div class='insight-box'>
        <div class='insight-num'>①</div>
        <div class='insight-title'>{T['insight1_titel']}</div>
        <div class='insight-text'>{T['insight1_text'].format(mon=best_mon, val=val_k, over=over_avg, total=len(monatlich))}</div>
    </div>
    <div class='insight-box'>
        <div class='insight-num'>②</div>
        <div class='insight-title'>{T['insight2_titel']}</div>
        <div class='insight-text'>{T['insight2_text'].format(uk=uk_anteil, land=top_export)}</div>
    </div>
    <div class='insight-box'>
        <div class='insight-num'>③</div>
        <div class='insight-title'>{T['insight3_titel']}</div>
        <div class='insight-text'>{T['insight3_text'].format(seg=top_seg_lbl, n=top_seg_n, pct=champ_pct)}</div>
    </div>
    <div class='insight-box'>
        <div class='insight-num'>④</div>
        <div class='insight-title'>{T['insight4_titel']}</div>
        <div class='insight-text'>{T['insight4_text'].format(sup=top_support)}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# UMSATZ
# ════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

u2009 = df_f[df_f["YearMonth"].str.startswith("2009")]["TotalPrice"].sum()
u2010 = df_f[df_f["YearMonth"].str.startswith("2010")]["TotalPrice"].sum()
u2011 = df_f[df_f["YearMonth"].str.startswith("2011")]["TotalPrice"].sum()
b2009 = df_f[df_f["YearMonth"].str.startswith("2009")]["Invoice"].nunique()
b2010 = df_f[df_f["YearMonth"].str.startswith("2010")]["Invoice"].nunique()
b2011 = df_f[df_f["YearMonth"].str.startswith("2011")]["Invoice"].nunique()
g2010 = ((u2010 - u2009) / u2009 * 100) if u2009 > 0 else 0
g2011 = ((u2011 - u2010) / u2010 * 100) if u2010 > 0 else 0

def pfeil(v):
    return (f"▲ +{v:.1f}%", GRUEN) if v >= 0 else (f"▼ {v:.1f}%", ROT)

p10, c10 = pfeil(g2010)
p11, c11 = pfeil(g2011)

jk1, jk2, jk3 = st.columns(3)
with jk1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-eyebrow'>{T['umsatz_2009']}</div><div class='kpi-value'>£{u2009/1e3:.0f}K</div><div class='kpi-sub'>{b2009:,} {T['basisjahr']}</div></div>", unsafe_allow_html=True)
with jk2:
    st.markdown(f"<div class='kpi-card'><div class='kpi-eyebrow'>{T['umsatz_2010']} &nbsp;<span style='color:{c10};font-size:12px;'>{p10}</span></div><div class='kpi-value'>£{u2010/1e3:.0f}K</div><div class='kpi-sub'>{b2010:,} {T['vs_2009']}</div></div>", unsafe_allow_html=True)
with jk3:
    st.markdown(f"<div class='kpi-card'><div class='kpi-eyebrow'>{T['umsatz_2011']} &nbsp;<span style='color:{c11};font-size:12px;'>{p11}</span></div><div class='kpi-value'>£{u2011/1e3:.0f}K</div><div class='kpi-sub'>{b2011:,} {T['vs_2010']}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_l, col_r = st.columns(2)
with col_l:
    monatlich["MA3"] = monatlich["Umsatz"].rolling(window=3, center=True).mean()
    st.markdown(f"<div class='chart-card'><div class='chart-title'>{T['mon_umsatz']}</div><div class='chart-subtitle'>{T['mon_sub']}</div>", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_bar(x=monatlich["Monat"], y=monatlich["Umsatz"],
                marker_color=[BLAU if u >= avg_u else BLAU_HELL for u in monatlich["Umsatz"]], name="Umsatz")
    fig.add_scatter(x=monatlich["Monat"], y=monatlich["MA3"], mode="lines",
                    line=dict(color="#1a1a1a", width=1.8, dash="dot"), name="3M-MA")
    fig.add_hline(y=avg_u, line_dash="dash", line_color=ORANGE, line_width=1.2,
                  annotation_text=f"Ø £{avg_u:,.0f}", annotation_font_color=ORANGE, annotation_position="right")
    fig.update_layout(legend=dict(orientation="h", y=1.08, x=0))
    st.plotly_chart(style(fig, 340), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_r:
    monatlich["Jahr"]     = monatlich["Monat"].str[:4]
    pivot_yoy             = monatlich.copy()
    pivot_yoy["Monat_Nr"] = pivot_yoy["Monat"].str[5:]
    pivot_wide            = pivot_yoy.pivot(index="Monat_Nr", columns="Jahr", values="Umsatz")
    if "2010" in pivot_wide.columns and "2011" in pivot_wide.columns:
        pivot_wide["YoY"] = (pivot_wide["2011"] - pivot_wide["2010"]) / pivot_wide["2010"] * 100
        yoy_vals  = pivot_wide["YoY"].dropna()
        cagr      = ((u2011 / u2010) - 1) * 100 if u2010 > 0 else 0
        st.markdown(f"<div class='chart-card'><div class='chart-title'>{T['yoy_titel']}</div><div class='chart-subtitle'>{T['yoy_sub'].format(cagr=cagr)}</div>", unsafe_allow_html=True)
        fig2 = go.Figure(go.Bar(
            x=yoy_vals.index, y=yoy_vals.values,
            marker_color=[GRUEN if v >= 0 else ROT for v in yoy_vals.values],
            text=[f"{v:+.1f}%" for v in yoy_vals.values],
            textposition="outside", textfont=dict(size=9, color="#888880"),
        ))
        fig2.add_hline(y=0, line_color="#cccccc", line_width=1)
        fig2.add_hline(y=cagr, line_dash="dash", line_color=ORANGE, line_width=1.5,
                       annotation_text=f"CAGR {cagr:+.1f}% p.a.", annotation_font_color=ORANGE, annotation_position="right")
        st.plotly_chart(style(fig2, 340), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ── SAISONALITÄT ─────────────────────────────────────────────
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

df_f["Monat_Nr"]   = df_f["InvoiceDate"].dt.month
df_f["Monat_Name"] = df_f["InvoiceDate"].dt.month.map(dict(enumerate(T["monate_label"], 1)))

sais = df_f.groupby("Monat_Nr").agg(Umsatz=("TotalPrice","sum"), Monat=("Monat_Name","first")).reset_index().sort_values("Monat_Nr")
best_monat = sais.loc[sais["Umsatz"].idxmax(), "Monat"]

s1, s2 = st.columns(2)
with s1:
    st.markdown(f"<div class='chart-card'><div class='chart-title'>{T['saison_mon']}</div><div class='chart-subtitle'>{T['saison_mon_sub'].format(mon=best_monat)}</div>", unsafe_allow_html=True)
    fig_s = go.Figure(go.Bar(x=sais["Monat"], y=sais["Umsatz"],
        marker_color=[BLAU if v == sais["Umsatz"].max() else BLAU_HELL for v in sais["Umsatz"]],
        text=sais["Umsatz"].apply(lambda x: f"£{x/1e3:.0f}K"),
        textposition="outside", textfont=dict(size=10, color="#888880")))
    st.plotly_chart(style(fig_s, 320), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with s2:
    df_f["Quartal"] = df_f["InvoiceDate"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})
    quart = df_f.groupby("Quartal")["TotalPrice"].sum().reset_index()
    quart.columns = ["Quartal", "Umsatz"]
    quart["Anteil"] = (quart["Umsatz"] / quart["Umsatz"].sum() * 100).round(1)
    st.markdown(f"<div class='chart-card'><div class='chart-title'>{T['saison_q']}</div><div class='chart-subtitle'>{T['saison_q_sub']}</div>", unsafe_allow_html=True)
    fig_q = go.Figure(go.Bar(x=quart["Quartal"], y=quart["Umsatz"],
        marker_color=[BLAU if v == quart["Umsatz"].max() else BLAU_HELL for v in quart["Umsatz"]],
        text=[f"£{v/1e3:.0f}K · {p:.0f}%" for v, p in zip(quart["Umsatz"], quart["Anteil"])],
        textposition="outside", textfont=dict(size=10, color="#888880")))
    st.plotly_chart(style(fig_q, 320), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# LÄNDER & PRODUKTE
# ════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    top_laender = land_ohne_uk.head(10)
    st.markdown(f"<div class='chart-card'><div class='chart-title'>{T['top_laender']}</div><div class='chart-subtitle'>{T['top_laender_sub']}</div>", unsafe_allow_html=True)
    fig = go.Figure(go.Bar(x=top_laender["Umsatz"], y=top_laender["Land"], orientation="h",
        marker_color=[BLAU if i == 0 else BLAU_HELL for i in range(len(top_laender))],
        text=top_laender["Umsatz"].apply(lambda x: f"£{x:,.0f}"),
        textposition="outside", textfont=dict(color="#888880", size=10)))
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(style(fig, 380), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    top_prod = df_f.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(10).reset_index()
    top_prod.columns = ["Produkt", "Umsatz"]
    st.markdown(f"<div class='chart-card'><div class='chart-title'>{T['top_produkte']}</div><div class='chart-subtitle'>{T['top_prod_sub']}</div>", unsafe_allow_html=True)
    fig2 = go.Figure(go.Bar(x=top_prod["Umsatz"], y=top_prod["Produkt"], orientation="h",
        marker_color=[BLAU if i == 0 else BLAU_HELL for i in range(len(top_prod))],
        text=top_prod["Umsatz"].apply(lambda x: f"£{x:,.0f}"),
        textposition="outside", textfont=dict(color="#888880", size=10)))
    fig2.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(style(fig2, 380), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# RFM
# ════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

rfm_tabelle = rfm.groupby("Segment").agg(
    N=("Customer ID","count"), Recency_avg=("Recency","mean"),
    Frequency_avg=("Frequency","mean"), Monetary_avg=("Monetary","mean"),
    Monetary_sum=("Monetary","sum")).round(1).reset_index()
rfm_tabelle["Kunden_%"] = (rfm_tabelle["N"] / rfm_tabelle["N"].sum() * 100).round(1)
rfm_tabelle = rfm_tabelle.sort_values("Monetary_sum", ascending=False).reset_index(drop=True)

SEG_FARBEN    = {"Champions":"#2a5298","Loyal Customers":"#4a7ab5","Recent Customers":"#e8792f","Needs Attention":"#c0392b","At Risk":"#c0392b","Lost":"#888880"}
RECENCY_GRENZE = 200

st.markdown(f"<div class='chart-card'><div class='chart-title'>{T['rfm_titel']}</div><div class='chart-subtitle'>{T['rfm_sub']}</div>", unsafe_allow_html=True)

fig_tbl = go.Figure(go.Table(
    columnwidth=[3, 1.2, 1.5, 1.5, 1.5, 1.5],
    header=dict(
        values=[f"<b>{T['seg']}</b>","<b>N</b>",f"<b>{T['kunden_%']}</b>",
                f"<b>{T['recency']}</b>",f"<b>{T['frequency']}</b>",f"<b>{T['monetary']}</b>"],
        fill_color="#ffffff", font=dict(color="#aaaaaa", size=10, family="Arial"),
        align=["left","right","right","right","right","right"], line_color="#e0e0dc", height=32),
    cells=dict(
        values=[
            rfm_tabelle["Segment"].tolist(),
            [f"{int(v):,}" for v in rfm_tabelle["N"]],
            [f"{v:.1f}%" for v in rfm_tabelle["Kunden_%"]],
            [f"{v:.0f} d" for v in rfm_tabelle["Recency_avg"]],
            [f"{v:.1f}" for v in rfm_tabelle["Frequency_avg"]],
            [f"£{v:,.0f}" for v in rfm_tabelle["Monetary_avg"]],
        ],
        fill_color="#ffffff",
        font=dict(
            color=[
                [SEG_FARBEN.get(s,"#888880") for s in rfm_tabelle["Segment"]],
                ["#555550"]*len(rfm_tabelle), ["#1a1a1a"]*len(rfm_tabelle),
                [ROT if v > RECENCY_GRENZE else "#1a1a1a" for v in rfm_tabelle["Recency_avg"]],
                ["#555550"]*len(rfm_tabelle), ["#555550"]*len(rfm_tabelle),
            ], size=12, family="Arial"),
        align=["left","right","right","right","right","right"],
        line_color="#f0f0ea", height=38)
))
fig_tbl.update_layout(height=38*len(rfm_tabelle)+60, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="#ffffff")
st.plotly_chart(fig_tbl, use_container_width=True, config={"displayModeBar": False})
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<div class='chart-card'><div class='chart-title'>{T['prio_titel']}</div><div class='chart-subtitle'>{T['prio_sub']}</div>", unsafe_allow_html=True)

cols = st.columns(2)
for i, (seg, farbe, text) in enumerate(T["empfehlungen"]):
    seg_row = rfm_tabelle[rfm_tabelle["Segment"] == seg]
    pct = f"{seg_row['Kunden_%'].values[0]:.0f}%" if len(seg_row) > 0 else ""
    with cols[i % 2]:
        st.markdown(f"""
        <div style='display:flex;gap:12px;margin-bottom:16px;'>
            <div style='width:14px;height:14px;min-width:14px;border-radius:3px;background:{farbe};margin-top:2px;'></div>
            <div>
                <div style='font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:2px;'>{seg} ({pct})</div>
                <div style='font-size:11px;color:#888880;line-height:1.5;'>{text}</div>
            </div>
        </div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# WARENKORBANALYSE
# ════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

st.markdown(f"<div class='chart-card'><div class='chart-title'>{T['warenkorb']}</div><div class='chart-subtitle'>{T['warenkorb_sub']}</div>", unsafe_allow_html=True)
fig_w = go.Figure(go.Bar(
    x=paare["Support"], y=paare["Pair"].astype(str), orientation="h",
    marker_color=[BLAU if i == 0 else BLAU_HELL for i in range(len(paare))],
    text=paare["Support"].apply(lambda x: f"{x:.2f}%"),
    textposition="outside", textfont=dict(color="#888880", size=10)))
fig_w.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="Support (%)")
st.plotly_chart(style(fig_w, 360), use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# SONDERPOSTEN
# ════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

sonder_alle = (
    sonder.groupby("StockCode")
    .agg(Anzahl=("StockCode","count"), Betrag=("TotalPrice","sum"))
    .reset_index()
)

top3_positiv = sonder_alle.sort_values("Betrag", ascending=False).head(3)
top3_negativ = sonder_alle.sort_values("Betrag", ascending=True).head(3)
sonder_combined = pd.concat([top3_positiv, top3_negativ]).reset_index(drop=True)
sonder_combined["Farbe"] = [BLAU, BLAU_HELL, BLAU_HELL, ROT, "#e8a0a0", "#e8a0a0"]
sonder_combined["Label"] = sonder_combined["Betrag"].apply(lambda x: f"£{x:,.0f}")

sp1, sp2 = st.columns(2)

with sp1:
    titel_sp = "Sonderposten – Top 3 positiv & negativ (Umsatz)" if sprache == "DE" else "Special Items – Top 3 positive & negative (Revenue)"
    sub_sp   = "Blau = größte positive Posten · Rot = größte negative Posten" if sprache == "DE" else "Blue = largest positive items · Red = largest negative items"
    st.markdown(f"<div class='chart-card'><div class='chart-title'>{titel_sp}</div><div class='chart-subtitle'>{sub_sp}</div>", unsafe_allow_html=True)
    fig_sp = go.Figure(go.Bar(
        x=sonder_combined["Betrag"], y=sonder_combined["StockCode"], orientation="h",
        marker_color=sonder_combined["Farbe"].tolist(),
        text=sonder_combined["Label"],
        textposition="outside", textfont=dict(color="#888880", size=10),
    ))
    fig_sp.add_vline(x=0, line_color="#cccccc", line_width=1)
    fig_sp.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(style(fig_sp, 320), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with sp2:
    titel_sp2 = "Sonderposten – Top 3 nach Anzahl Transaktionen" if sprache == "DE" else "Special Items – Top 3 by Transaction Count"
    sub_sp2   = "Häufigste Sonderposten-Buchungen im Datensatz" if sprache == "DE" else "Most frequent special item bookings in dataset"
    top3_anzahl = sonder_alle.sort_values("Anzahl", ascending=False).head(3)
    st.markdown(f"<div class='chart-card'><div class='chart-title'>{titel_sp2}</div><div class='chart-subtitle'>{sub_sp2}</div>", unsafe_allow_html=True)
    fig_sp2 = go.Figure(go.Bar(
        x=top3_anzahl["Anzahl"], y=top3_anzahl["StockCode"], orientation="h",
        marker_color=[ORANGE, "#fad9c0", "#fad9c0"],
        text=top3_anzahl["Anzahl"].apply(lambda x: f"{x:,}"),
        textposition="outside", textfont=dict(color="#888880", size=10),
    ))
    fig_sp2.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(style(fig_sp2, 320), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;font-size:10px;color:#cccccc;'>{T['footer']}</p>", unsafe_allow_html=True)