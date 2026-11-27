from pathlib import Path
import re
import pandas as pd
import streamlit as st
 
# ============================================================
# FC10 | ENCICLOPEDIA HISTÓRICA DEL FÚTBOL
# ============================================================
 
BASE_DIR = Path(__file__).resolve().parent
 
CSV_PATHS = [
    BASE_DIR / "data" / "FC10_ganadores_futbol.csv",
    BASE_DIR / "FC10_ganadores_futbol.csv",
]
 
COMMUNITY_URL = "https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=d1_RKkjT-02kscIk7Mr-aMAwOq-IwwpMmEXR7soT7LNUQlRTMEhJRkxHSTJWNFBFMldJTUJYTjc3SS4u%22"
 
st.set_page_config(
    page_title="FC10 | La historia del fútbol",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# ============================================================
# DISEÑO VISUAL
# ============================================================
 
st.markdown("""
<style>
 
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap%27);
 
:root {
    --navy: #081a33;
    --blue: #1769e0;
    --pale: #f3f6fa;
    --ink: #14243b;
    --muted: #6c7b90;
}
 
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
 
.stApp {
    background: #f5f7fb;
    color: var(--ink);
}
 
.block-container {
    max-width: 1200px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}
 
header[data-testid="stHeader"] {
    background: transparent;
}
 
#MainMenu, footer {
    visibility: hidden;
}
 
.brand-fallback {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 34px;
    letter-spacing: -2px;
    color: var(--navy);
}
 
.brand-caption {
    color: #718096;
    font-size: 9px;
    letter-spacing: 2.4px;
    margin-top: -7px;
}
 
.nav-label {
    color: #718297;
    font-size: 11px;
    letter-spacing: 1.8px;
    font-weight: 700;
    text-transform: uppercase;
    padding-top: 15px;
    text-align: right;
}
 
div[role="radiogroup"] {
    gap: 8px;
    justify-content: flex-end;
}
 
div[role="radiogroup"] label {
    background: white;
    border: 1px solid #e5eaf1;
    border-radius: 22px;
    padding: 7px 14px;
}
 
div[role="radiogroup"] label p {
    font-size: 12px;
    font-weight: 600;
}
 
.hero {
    background: linear-gradient(
        115deg,
        #07182f 0%,
        #102e55 65%,
        #1556a8 100%
    );
    border-radius: 22px;
    padding: 58px 58px 52px;
    color: white;
    position: relative;
    overflow: hidden;
}
 
.hero:after {
    content: "FC10";
    position: absolute;
    right: 28px;
    bottom: -48px;
    font-family: 'Playfair Display', serif;
    font-size: 190px;
    font-weight: 700;
    color: rgba(255,255,255,.045);
    letter-spacing: -15px;
}
 
.eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #8db9ff;
    text-transform: uppercase;
    margin-bottom: 18px;
}
 
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(38px,5vw,62px);
    line-height: 1.08;
    letter-spacing: -1.5px;
    margin: 0 0 18px;
    color: white;
}
 
.hero p {
    color: #d7e2f1;
    max-width: 570px;
    font-size: 15px;
    line-height: 1.8;
    margin: 0;
}
 
.section-kicker {
    color: #1769e0;
    font-size: 10px;
    letter-spacing: 2.5px;
    font-weight: 700;
    text-transform: uppercase;
    margin: 0 0 8px;
}
 
.section-title {
    font-family: 'Playfair Display', serif;
    color: #10233e;
    font-size: 34px;
    font-weight: 600;
    margin: 0 0 8px;
}
 
.section-sub {
    color: #748197;
    font-size: 14px;
    margin: 0 0 22px;
}
 
.panel {
    background: white;
    border: 1px solid #e8edf4;
    border-radius: 16px;
    padding: 22px;
    height: 100%;
}
 
.panel-label {
    color: #78869a;
    font-size: 10px;
    letter-spacing: 1.5px;
    font-weight: 700;
    text-transform: uppercase;
}
 
.panel-number {
    font-family: 'Playfair Display', serif;
    color: #10233e;
    font-size: 36px;
    font-weight: 700;
    margin-top: 7px;
}
 
.panel-note {
    color: #8793a4;
    font-size: 12px;
    margin-top: 2px;
}
 
.record-card {
    background: white;
    border: 1px solid #e7edf4;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 10px;
}
 
.record-year {
    color: #1769e0;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}
 
.record-winner {
    color: #10233e;
    font-size: 17px;
    font-weight: 700;
    margin-top: 5px;
}
 
.record-comp {
    color: #7a8798;
    font-size: 11px;
    margin-top: 4px;
}
 
.story-box {
    background: #edf3fb;
    border-left: 3px solid #1769e0;
    padding: 18px 20px;
    border-radius: 0 12px 12px 0;
    color: #53647a;
    font-size: 13px;
    line-height: 1.7;
}
 
.footer {
    border-top: 1px solid #e3e9f1;
    padding-top: 22px;
    margin-top: 45px;
    color: #8793a4;
    font-size: 11px;
}
 
.stButton>button,
.stLinkButton>a {
    border-radius: 22px !important;
    font-weight: 700 !important;
}
 
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px !important;
}
 
div[data-testid="stDataFrame"] {
    border: 1px solid #e7edf4;
    border-radius: 12px;
    overflow: hidden;
}
 
@media(max-width:700px) {
    .hero {
        padding: 34px 25px;
    }
 
    .section-title {
        font-size: 28px;
    }
 
    .nav-label {
        display: none;
    }
}
 
</style>
""", unsafe_allow_html=True)
 
 
# ============================================================
# CARGA DE BASE DE DATOS
# ============================================================
 
def load_data():
 
    path = next(
        (p for p in CSV_PATHS if p.exists()),
        None
    )
 
    if not path:
        return pd.DataFrame(), None, "No se encontró el CSV."
 
    try:
 
        raw = pd.read_csv(
            path,
            encoding="utf-8-sig"
        )
 
        if len(raw.columns) == 1:
 
            raw = pd.read_csv(
                path,
                encoding="utf-8-sig",
                sep=";"
            )
 
        raw.columns = [
            str(c).strip()
            for c in raw.columns
        ]
 
        return raw, path, None
 
    except Exception as exc:
 
        return (
            pd.DataFrame(),
            path,
            f"No se pudo leer el CSV: {exc}"
        )
 
 
def split_year_value(value):
 
    if pd.isna(value):
        return None, ""
 
    text = str(value).strip()
 
    match = re.match(
        r"^(\d{4})\s+(.+)$",
        text
    )
 
    if match:
 
        return (
            int(match.group(1)),
            match.group(2).strip()
        )
 
    match = re.match(
        r"^(\d{4})[-/]\s*(.+)$",
        text
    )
 
    if match:
 
        return (
            int(match.group(1)),
            match.group(2).strip()
        )
 
    return None, text
 
 
def normalize_records(raw):
 
    mapping = {
 
        "Ganadores de Balón de Oro":
            "Balón de Oro",
 
        "Ganadores de Champions League":
            "Champions League",
 
        "Ganadores de Bota de Oro":
            "Bota de Oro",
 
        "Ganadores de Liga MX":
            "Liga MX",
    }
 
    records = []
 
    for col, competition in mapping.items():
 
        if col not in raw.columns:
            continue
 
        for value in raw[col].dropna():
 
            year, winner = split_year_value(value)
 
            if winner:
 
                records.append({
 
                    "Competición": competition,
 
                    "Año": year,
 
                    "Ganador": winner
 
                })
 
    df = pd.DataFrame(records)
 
    if not df.empty:
 
        df = df.sort_values(
            ["Año", "Competición"],
            ascending=[False, True],
            na_position="last"
        )
 
    return df
 
 
raw, csv_path, csv_error = load_data()
 
records = (
    normalize_records(raw)
    if not raw.empty
    else pd.DataFrame(
        columns=[
            "Competición",
            "Año",
            "Ganador"
        ]
    )
)
 
 
# ============================================================
# CABECERA Y LOGOTIPO
# ============================================================
 
logo_candidates = [
 
    BASE_DIR / "assets" / "logo_fc10.png",
 
    BASE_DIR / "assets" / "fc10_logo.png",
 
    BASE_DIR / "logo_fc10.png",
 
]
 
logo = next(
    (p for p in logo_candidates if p.exists()),
    None
)
 
left, right = st.columns([1, 3])
 
with left:
 
    if logo:
 
        st.image(
            str(logo),
            width=155
        )
 
    else:
 
        st.markdown(
            """
<div class="brand-fallback">FC10</div>
<div class="brand-caption">
                FOOTBALL CHRONICLES
</div>
            """,
            unsafe_allow_html=True
        )
 
with right:
 
    st.markdown(
        """
<div class="nav-label">
            LA ENCICLOPEDIA HISTÓRICA DEL FÚTBOL
</div>
        """,
        unsafe_allow_html=True
    )
 
st.markdown(
    "<hr style='border:0;border-top:1px solid #e3e9f1;margin:12px 0 22px;'>",
    unsafe_allow_html=True
)
 
 
# ============================================================
# NAVEGACIÓN
# ============================================================
 
pages = [
 
    "Inicio",
 
    "Nosotros",
 
    "Palmarés",
 
    "Récords y estadísticas",
 
    "Comunidad"
 
]
 
selected = st.radio(
    "Navegación",
    pages,
    horizontal=True,
    label_visibility="collapsed",
    key="main_navigation"
)
 
st.write("")
 
 
# ============================================================
# FUNCIONES VISUALES
# ============================================================
 
def section(kicker, title, subtitle=""):
 
    st.markdown(
        f"""
<div class="section-kicker">
            {kicker}
</div>
 
        <h2 class="section-title">
            {title}
</h2>
 
        <p class="section-sub">
            {subtitle}
</p>
        """,
        unsafe_allow_html=True
    )
 
 
def card_metric(label, number, note):
 
    st.markdown(
        f"""
<div class="panel">
 
            <div class="panel-label">
                {label}
</div>
 
            <div class="panel-number">
                {number}
</div>
 
            <div class="panel-note">
                {note}
</div>
 
        </div>
        """,
        unsafe_allow_html=True
    )
 
 
def show_records(df):
 
    if df.empty:
 
        st.info(
            "Todavía no hay registros disponibles en esta categoría."
        )
 
        return
 
    for _, row in df.iterrows():
 
        year = (
            str(int(row["Año"]))
            if pd.notna(row["Año"])
            else "—"
        )
 
        st.markdown(
            f"""
<div class="record-card">
 
                <div class="record-year">
                    {year}
</div>
 
                <div class="record-winner">
                    {row["Ganador"]}
</div>
 
                <div class="record-comp">
                    {row["Competición"]}
</div>
 
            </div>
            """,
            unsafe_allow_html=True
        )
 
 
# ============================================================
# PÁGINA DE INICIO
# ============================================================
 
if selected == "Inicio":
 
    st.markdown(
        """
<div class="hero">
 
            <div class="eyebrow">
                FC10 · Archivo histórico
</div>
 
            <h1>
                La historia del fútbol,
<br>
                en un solo lugar.
</h1>
 
            <p>
                Una enciclopedia para explorar campeones,
                premios, equipos, récords y protagonistas
                que han marcado el deporte. Consulta los
                registros y descubre el contexto detrás
                de cada época.
</p>
 
        </div>
        """,
        unsafe_allow_html=True
    )
 
    st.write("")
 
    section(
        "Explora FC10",
        "Un archivo para descubrir",
        "Consulta los grandes registros del fútbol y encuentra la información que buscas."
    )
 
    if csv_error:
 
        st.warning(csv_error)
 
    total = len(records)
 
    winners = (
        records["Ganador"].nunique()
        if total
        else 0
    )
 
    years = (
        records["Año"].dropna()
        if total
        else pd.Series(dtype=float)
    )
 
    c1, c2, c3 = st.columns(3)
 
    with c1:
 
        card_metric(
            "Registros cargados",
            f"{total:,}",
            "Datos disponibles en el archivo"
        )
 
    with c2:
 
        card_metric(
            "Ganadores / equipos",
            f"{winners:,}",
            "Nombres distintos registrados"
        )
 
    with c3:
 
        card_metric(
            "Años cubiertos",
            (
                f"{int(years.min())}–{int(years.max())}"
                if len(years)
                else "—"
            ),
            "Rango detectado en el CSV"
        )
 
    st.write("")
 
    c1, c2 = st.columns([1.35, 1])
 
    with c1:
 
        section(
            "Archivo",
            "Últimos registros",
            "Los datos más recientes de las cuatro colecciones."
        )
 
        show_records(
            records.head(5)
        )
 
    with c2:
 
        section(
            "Colecciones",
            "Explora por categoría"
        )
 
        for name in [
 
            "Balón de Oro",
 
            "Bota de Oro",
 
            "Champions League",
 
            "Liga MX"
 
        ]:
 
            count = (
                int(
                    (records["Competición"] == name).sum()
                )
                if total
                else 0
            )
 
            st.markdown(
                f"""
<div class="record-card">
 
                    <div class="record-winner">
                        {name}
</div>
 
                    <div class="record-comp">
                        {count} registros en el archivo
</div>
 
                </div>
                """,
                unsafe_allow_html=True
            )
 
 
# ============================================================
# NOSOTROS
# ============================================================
 
elif selected == "Nosotros":
 
    section(
        "FC10",
        "Una memoria del fútbol",
        "Un espacio para consultar datos, reconocer protagonistas y entender por qué ciertos momentos se volvieron parte de la historia."
    )
 
    st.markdown(
        """
<div class="panel">
 
            <h3 style="font-family:'Playfair Display',serif;color:#10233e;margin-top:0;">
                ¿Qué es FC10?
</h3>
 
            <p style="color:#5e6e83;line-height:1.9;">
                FC10 es una enciclopedia digital dedicada a reunir
                información histórica del fútbol. Su objetivo es
                que cualquier aficionado pueda consultar campeones,
                temporadas, premios, equipos, jugadores y
                acontecimientos importantes desde un mismo sitio.
</p>
 
            <h3 style="font-family:'Playfair Display',serif;color:#10233e;">
                ¿Qué encontrarás?
</h3>
 
            <p style="color:#5e6e83;line-height:1.9;">
                Registros de competiciones y premios, estadísticas
                organizadas y, progresivamente, artículos que
                expliquen el contexto de finales, temporadas,
                récords y figuras del fútbol.
</p>
 
            <h3 style="font-family:'Playfair Display',serif;color:#10233e;">
                Nuestro criterio
</h3>
 
            <p style="color:#5e6e83;line-height:1.9;">
                Los datos se presentan como registros consultables.
                Los artículos históricos se incorporarán cuando
                hayan sido investigados y contrastados con fuentes
                confiables.
</p>
 
        </div>
        """,
        unsafe_allow_html=True
    )
 
 
# ============================================================
# PALMARÉS
# ============================================================
 
elif selected == "Palmarés":
 
    section(
        "Archivo de campeones",
        "Palmarés",
        "Busca por competición, año o ganador."
    )
 
    competitions = [
 
        "Todas",
 
        "Balón de Oro",
 
        "Bota de Oro",
 
        "Champions League",
 
        "Liga MX"
 
    ]
 
    f1, f2, f3 = st.columns([1.2, 1, 1.5])
 
    with f1:
 
        comp = st.selectbox(
            "Competición",
            competitions
        )
 
    with f2:
 
        years_available = (
 
            sorted(
                [
                    int(y)
                    for y in records["Año"].dropna().unique()
                ],
                reverse=True
            )
 
            if not records.empty
 
            else []
 
        )
 
        year_options = (
            ["Todos"]
            + [str(y) for y in years_available]
        )
 
        year = st.selectbox(
            "Año",
            year_options
        )
 
    with f3:
 
        query = st.text_input(
            "Buscar ganador o equipo",
            placeholder="Ej. Lionel Messi"
        )
 
    filtered = records.copy()
 
    if comp != "Todas":
 
        filtered = filtered[
            filtered["Competición"] == comp
        ]
 
    if year != "Todos":
 
        filtered = filtered[
            filtered["Año"] == int(year)
        ]
 
    if query.strip():
 
        filtered = filtered[
            filtered["Ganador"].str.contains(
                query.strip(),
                case=False,
                na=False
            )
        ]
 
    st.caption(
        f"{len(filtered)} resultados"
    )
 
    if filtered.empty:
 
        st.info(
            "No hay resultados con esos filtros. Prueba con otra búsqueda."
        )
 
    else:
 
        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True,
            height=min(
                620,
                45 + 38 * len(filtered)
            )
        )
 
    st.markdown(
        """
<div class="story-box">
 
            <strong>Ver la historia:</strong>
 
            Las fichas narrativas de cada edición se
            incorporarán progresivamente, con contexto,
            protagonistas, momentos decisivos y fuentes.
            No se muestran relatos ficticios ni información
            sin verificar.
 
        </div>
        """,
        unsafe_allow_html=True
    )
 
 
# ============================================================
# RÉCORDS Y ESTADÍSTICAS
# ============================================================
 
elif selected == "Récords y estadísticas":
 
    section(
        "Los números del fútbol",
        "Récords y estadísticas",
        "Explora los datos disponibles y compara las colecciones del archivo."
    )
 
    if records.empty:
 
        st.warning(
            "No hay datos que analizar. Revisa que el CSV esté dentro de la carpeta data."
        )
 
    else:
 
        c1, c2, c3 = st.columns(3)
 
        with c1:
 
            card_metric(
                "Registros",
                f"{len(records):,}",
                "Total de filas interpretadas"
            )
 
        with c2:
 
            card_metric(
                "Ganadores distintos",
                f"{records['Ganador'].nunique():,}",
                "Nombres diferentes"
            )
 
        valid_years = records["Año"].dropna()
 
        with c3:
 
            card_metric(
                "Año más antiguo",
                (
                    str(int(valid_years.min()))
                    if len(valid_years)
                    else "—"
                ),
                "Según el CSV"
            )
 
        st.write("")
 
        section(
            "Distribución",
            "Registros por competición"
        )
 
        counts = (
 
            records["Competición"]
            .value_counts()
            .reindex(
                [
                    "Balón de Oro",
                    "Bota de Oro",
                    "Champions League",
                    "Liga MX"
                ]
            )
            .fillna(0)
            .astype(int)
 
        )
 
        st.bar_chart(
            counts,
            color="#1769e0"
        )
 
        section(
            "Consulta",
            "Ganadores más repetidos",
            "Conteo de apariciones en las cuatro colecciones; no equivale necesariamente a títulos de una misma competición."
        )
 
        repeated = (
 
            records["Ganador"]
            .value_counts()
            .head(10)
            .rename_axis("Nombre")
            .reset_index(name="Apariciones")
 
        )
 
        st.dataframe(
            repeated,
            use_container_width=True,
            hide_index=True
        )
 
 
# ============================================================
# COMUNIDAD
# ============================================================
 
elif selected == "Comunidad":
 
    section(
        "La comunidad FC10",
        "Propón una historia",
        "Las mejores propuestas podrán convertirse en artículos del archivo."
    )
 
    st.markdown(
        """
<div class="panel">
 
            <h3 style="font-family:'Playfair Display',serif;color:#10233e;margin-top:0;">
                ¿Qué historia del fútbol te gustaría leer?
</h3>
 
            <p style="color:#5e6e83;line-height:1.9;">
                Puedes sugerir una final, una temporada, un jugador,
                un equipo, un récord o un acontecimiento que merezca
                ser contado. Revisaremos las propuestas y
                seleccionaremos historias para publicar.
</p>
 
            <p style="color:#5e6e83;line-height:1.9;">
                No necesitas crear una cuenta. Solo abre el
                formulario y envía tu idea.
</p>
 
        </div>
        """,
        unsafe_allow_html=True
    )
 
    st.write("")
 
    st.link_button(
        "Enviar mi propuesta",
        COMMUNITY_URL,
        use_container_width=False
    )
 
 
# ============================================================
# PIE DE PÁGINA
# ============================================================
 
st.markdown(
    """
<div class="footer">
 
        <strong style="color:#10233e;">
            FC10
</strong>
 
        · La enciclopedia histórica del fútbol
 
        <br>
 
        Datos, historias y momentos que marcaron el deporte.
 
    </div>
    """,
    unsafe_allow_html=True
)
 
 
if csv_error and selected != "Inicio":
 
    with st.expander("Diagnóstico del archivo"):
 
        st.error(csv_error)
 
        st.write(
            "Ruta esperada:",
            str(CSV_PATHS[0])
        )
