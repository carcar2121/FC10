from pathlib import Path
import re
import pandas as pd
import streamlit as st

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="FC10 | Enciclopedia Histórica del Fútbol",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ESTILOS VISUALES AVANZADOS (MARINA / DARK)
# ==========================================
st.markdown("""
<style>
    /* Estilos globales */
    .stApp {
        background-color: #030a17;
        color: #f8fafc;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Encabezado Principal / Hero */
    .fc-hero {
        background: linear-gradient(135deg, #091c38 0%, #0d2a54 50%, #1e40af 100%);
        border: 1px solid #1e3a8a;
        border-radius: 20px;
        padding: 40px;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        margin-bottom: 30px;
    }
    .fc-hero h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 10px;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .fc-hero p {
        font-size: 1.15rem;
        color: #cbd5e1;
        max-width: 800px;
        line-height: 1.6;
    }

    /* Tarjetas de Contenido y Estadísticas */
    .fc-card {
        background: linear-gradient(145deg, #071528, #0a1f3d);
        border: 1px solid #1e3a8a;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #0a2540 0%, #0d2a54 100%);
        border: 1px solid #2563eb;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Ocultar elementos predeterminados de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# CARGA DE DATOS DESDE EXCEL
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
EXCEL_PATH = BASE_DIR / "data" / "FC10_ganadores_futbol.xlsx"

@st.cache_data
def load_data():
    if not EXCEL_PATH.exists():
        return pd.DataFrame()
    try:
        df = pd.read_excel(EXCEL_PATH)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return pd.DataFrame()

raw_df = load_data()

def process_records(df):
    if df.empty:
        return pd.DataFrame(columns=["Competición", "Año", "Ganador"])
    
    records = []
    for col in df.columns:
        comp_name = col.replace("Ganadores de ", "").strip()
        for val in df[col].dropna():
            text = str(val).strip()
            match = re.match(r"^(\d{4})[\s\-–]+(.+)$", text)
            if match:
                records.append({
                    "Competición": comp_name,
                    "Año": int(match.group(1)),
                    "Ganador": match.group(2).strip()
                })
            else:
                records.append({
                    "Competición": comp_name,
                    "Año": None,
                    "Ganador": text
                })
    return pd.DataFrame(records)

records_df = process_records(raw_df)

# ==========================================
# BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.markdown("### ⚽ FC10 Navigation")
    st.markdown("---")
    selected = st.radio(
        "Menú Principal",
        ["Inicio", "Palmarés y Ganadores", "Estadísticas Globales", "Acerca de FC10"]
    )
    st.markdown("---")
    st.markdown("<p style='font-size: 0.85rem; color: #94a3b8;'>Plataforma oficial de consulta histórica del balompié mundial y regional.</p>", unsafe_allow_html=True)

# ==========================================
# CONTENIDO DE LAS SECCIONES
# ==========================================

if selected == "Inicio":
    st.markdown("""
    <div class="fc-hero">
        <h1>⚽ FC10 · Enciclopedia Histórica</h1>
        <p>El archivo definitivo que recopila la gloria de los torneos y galardones más prestigiosos del fútbol internacional: Balón de Oro, Bota de Oro, UEFA Champions League y Liga MX.</p>
    </div>
    """, unsafe_allow_html=True)

    if raw_df.empty:
        st.warning("⚠️ No se detectó el archivo de datos en la ruta `data/FC10_ganadores_futbol.xlsx`. Verifica su ubicación.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-container"><h3>Registros</h3><h2>{}</h2></div>'.format(len(records_df)), unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-container"><h3>Competiciones</h3><h2>{}</h2></div>'.format(records_df["Competición"].nunique() if not records_df.empty else 0), unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-container"><h3>Protagonistas</h3><h2>{}</h2></div>'.format(records_df["Ganador"].nunique() if not records_df.empty else 0), unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-container"><h3>Estado</h3><h2>Activo 🟢</h2></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### 🏆 Competencias Registradas en el Sistema")
        c_a, c_b = st.columns(2)
        with c_a:
            st.markdown("""
            <div class="fc-card">
                <h4>🌟 Galardones Individuales</h4>
                <p>Consulta los años, leyendas y goleadores históricos que se han consagrado con el <strong>Balón de Oro</strong> y la <strong>Bota de Oro</strong> a nivel mundial.</p>
            </div>
            """, unsafe_allow_html=True)
        with c_b:
            st.markdown("""
            <div class="fc-card">
                <h4>🛡️ Torneos de Clubes</h4>
                <p>Explora el dominio de los gigantes europeos en la <strong>Champions League</strong> y la emoción de cada torneo Apertura y Clausura de la <strong>Liga MX</strong>.</p>
            </div>
            """, unsafe_allow_html=True)

elif selected == "Palmarés y Ganadores":
    st.markdown("## 🏆 Palmarés Histórico y Filtrado Avanzado")
    st.markdown("Consulta y filtra de manera dinámica todos los ganadores por categoría o mediante búsqueda directa.")
    
    if records_df.empty:
        st.warning("No hay registros disponibles para mostrar.")
    else:
        f1, f2 = st.columns([1, 2])
        with f1:
            comp_filtro = st.selectbox("Filtrar por Competición", ["Todas", "Balón de Oro", "Bota de Oro", "Champions League", "Liga MX"])
        with f2:
            busqueda = st.text_input("🔍 Búsqueda inteligente por Jugador o Equipo", placeholder="Ej. Lionel Messi, Real Madrid, Erling Haaland...")
        
        df_show = records_df.copy()
        if comp_filtro != "Todas":
            df_show = df_show[df_show["Competición"] == comp_filtro]
        
        if busqueda.strip():
            df_show = df_show[df_show["Ganador"].str.contains(busqueda.strip(), case=False, na=False)]
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df_show, use_container_width=True, hide_index=True)

elif selected == "Estadísticas Globales":
    st.markdown("## 📊 Análisis y Estadísticas Globales")
    st.markdown("Desglose analítico de los datos históricos registrados en la plataforma.")
    
    if records_df.empty:
        st.warning("No hay datos suficientes para generar estadísticas.")
    else:
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown('<div class="metric-container"><h3>Total Entradas</h3><h2>{}</h2></div>'.format(len(records_df)), unsafe_allow_html=True)
        with m2:
            st.markdown('<div class="metric-container"><h3>Categorías</h3><h2>{}</h2></div>'.format(records_df["Competición"].nunique()), unsafe_allow_html=True)
        with m3:
            st.markdown('<div class="metric-container"><h3>Promedio por Torneo</h3><h2>{:.1f}</h2></div>'.format(len(records_df) / records_df["Competición"].nunique()), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.markdown("""
            <div class="fc-card">
                <h3>📈 Distribución por Competición</h3>
                <p style="color: #cbd5e1; font-size: 0.9rem;">Cantidad absoluta de registros históricos recopilados por cada galardón o torneo oficial.</p>
            </div>
            """, unsafe_allow_html=True)
            conteo_comp = records_df["Competición"].value_counts()
            st.bar_chart(conteo_comp)
            
        with col_g2:
            st.markdown("""
            <div class="fc-card">
                <h3>📋 Tabla Resumen de Frecuencia</h3>
                <p style="color: #cbd5e1; font-size: 0.9rem;">Participación porcentual y conteo exacto por categoría deportiva.</p>
            </div>
            """, unsafe_allow_html=True)
            
            resumen_df = records_df["Competición"].value_counts().reset_index()
            resumen_df.columns = ["Competición", "Total Registros"]
            resumen_df["Porcentaje"] = ((resumen_df["Total Registros"] / len(records_df)) * 100).round(1).astype(str) + "%"
            st.dataframe(resumen_df, use_container_width=True, hide_index=True)

elif selected == "Acerca de FC10":
    st.markdown("## ℹ️ Acerca de la Plataforma")
    st.markdown("""
    <div class="fc-card">
        <h3>FC10 · Enciclopedia Histórica del Fútbol</h3>
        <p>Desarrollado como una solución moderna, veloz y elegante para la gestión y consulta de datos deportivos mediante tecnologías de vanguardia como Streamlit y Pandas.</p>
        <hr style="border-color: #1e3a8a;">
        <p><strong>Diseño visual:</strong> Estética Marina / Dark Mode optimizada para una lectura profesional y cómoda.</p>
        <p><strong>Versión del sistema:</strong> 2.5 Pro</p>
    </div>
    """, unsafe_allow_html=True)