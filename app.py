import streamlit as st
import pandas as pd
import pydeck as pdk
import random
from datetime import datetime

# --- 1. PAGE SETUP & CONSTANTS ---
st.set_page_config(page_title="Recife Expanded Metro Traffic Grid", layout="wide")

THRESHOLD_RATIO = 1.5  # Critical threshold: 50% or more delay than free flow

# Comprehensive high-density coordinate grid mapping major RMR corridors sequentially
CORRIDOR_DATA = [
    # --- Av. Agamenon Magalhães ---
    {"avenue": "Av. Agamenon Magalhães", "point": "Agamenon - Segment 1: Próx. ao Shopping Tacaruna", "lat": -8.0375, "lon": -34.8715},
    {"avenue": "Av. Agamenon Magalhães", "point": "Agamenon - Segment 2: Cruzamento com Av. Norte", "lat": -8.0442, "lon": -34.8788},
    {"avenue": "Av. Agamenon Magalhães", "point": "Agamenon - Segment 3: Altura do Parque Amorim", "lat": -8.0515, "lon": -34.8912},
    {"avenue": "Av. Agamenon Magalhães", "point": "Agamenon - Segment 4: Praça do Derby", "lat": -8.0562, "lon": -34.8966},
    {"avenue": "Av. Agamenon Magalhães", "point": "Agamenon - Segment 5: Viaduto da Ilha do Leite", "lat": -8.0664, "lon": -34.8998},

    # --- Av. Conselheiro Rosa e Silva ---
    {"avenue": "Av. Conselheiro Rosa e Silva", "point": "Rosa e Silva - Segment 1: Início (Espinheiro / Av. Norte)", "lat": -8.0465, "lon": -34.8930},
    {"avenue": "Av. Conselheiro Rosa e Silva", "point": "Rosa e Silva - Segment 2: Altura do Clube Náutico (Aflitos)", "lat": -8.0392, "lon": -34.8988},
    {"avenue": "Av. Conselheiro Rosa e Silva", "point": "Rosa e Silva - Segment 3: Parnamirim (Próx. Parque da Jaqueira)", "lat": -8.0345, "lon": -34.9045},

    # --- Av. 17 de Agosto ---
    {"avenue": "Av. 17 de Agosto", "point": "17 de Agosto - Segment 1: Início (Praça de Parnamirim)", "lat": -8.0340, "lon": -34.9065},
    {"avenue": "Av. 17 de Agosto", "point": "17 de Agosto - Segment 2: Altura da Praça de Casa Forte", "lat": -8.0333, "lon": -34.9188},
    {"avenue": "Av. 17 de Agosto", "point": "17 de Agosto - Segment 3: Monteiro (Próx. Parque do Caiara)", "lat": -8.0255, "lon": -34.9255},

    # --- Av. Domingos Ferreira ---
    {"avenue": "Av. Eng. Domingos Ferreira", "point": "Domingos Ferreira - Segment 1: Início (Pina / Próx. Transbordo)", "lat": -8.0905, "lon": -34.8855},
    {"avenue": "Av. Eng. Domingos Ferreira", "point": "Domingos Ferreira - Segment 2: Altura do Carrefour", "lat": -8.1061, "lon": -34.8906},
    {"avenue": "Av. Eng. Domingos Ferreira", "point": "Domingos Ferreira - Segment 3: Cruzamento Pe. Carapuceiro", "lat": -8.1189, "lon": -34.8950},
    {"avenue": "Av. Eng. Domingos Ferreira", "point": "Domingos Ferreira - Segment 4: Final (Próx. ao Shopping Recife / Divisa)", "lat": -8.1320, "lon": -34.9001},

    # --- Av. Boa Viagem ---
    {"avenue": "Av. Boa Viagem", "point": "Av. Boa Viagem - Segment 1: Pina (Início)", "lat": -8.0935, "lon": -34.8872},
    {"avenue": "Av. Boa Viagem", "point": "Av. Boa Viagem - Segment 2: Altura do Segundo Jardim", "lat": -8.1064, "lon": -34.8923},
    {"avenue": "Av. Boa Viagem", "point": "Av. Boa Viagem - Segment 3: Próx. à Pracinha de Boa Viagem", "lat": -8.1271, "lon": -34.9021},
    {"avenue": "Av. Boa Viagem", "point": "Av. Boa Viagem - Segment 4: Final (Próx. ao Hotel Atlante Plaza)", "lat": -8.1385, "lon": -34.9068},

    # --- Av. Ayrton Senna ---
    {"avenue": "Av. Ayrton Senna (Jaboatão)", "point": "Ayrton Senna - Segment 1: Divisa Boa Viagem / Piedade", "lat": -8.1462, "lon": -34.9102},
    {"avenue": "Av. Ayrton Senna (Jaboatão)", "point": "Ayrton Senna - Segment 2: Altura do Shopping Guararapes", "lat": -8.1631, "lon": -34.9168},
    {"avenue": "Av. Ayrton Senna (Jaboatão)", "point": "Ayrton Senna - Segment 3: Trecho Candeias (Próx. à Curva do S)", "lat": -8.1815, "lon": -34.9224},

    # --- Rodovia PE-15 ---
    {"avenue": "PE-15", "point": "PE-15 - Segment 1: Complexo de Salgadinho (Olinda)", "lat": -8.0285, "lon": -34.8690},
    {"avenue": "PE-15", "point": "PE-15 - Segment 2: Altura do Terminal Integrado PE-15", "lat": -8.0011, "lon": -34.8765},
    {"avenue": "PE-15", "point": "PE-15 - Segment 3: Cidade Tabajara (Limite Paulista)", "lat": -7.9625, "lon": -34.8672},
    {"avenue": "PE-15", "point": "PE-15 - Segment 4: Centro de Paulista", "lat": -7.9412, "lon": -34.8744},

    # --- Av. Presidente Kennedy ---
    {"avenue": "Av. Presidente Kennedy", "point": "Pres. Kennedy - Segment 1: Início (Vila Popular / Olinda)", "lat": -8.0270, "lon": -34.8760},
    {"avenue": "Av. Presidente Kennedy", "point": "Pres. Kennedy - Segment 2: Altura de Peixinhos", "lat": -8.0132, "lon": -34.8845},
    {"avenue": "Av. Presidente Kennedy", "point": "Pres. Kennedy - Segment 3: Próx. ao Terminal de Xambá", "lat": -7.9995, "lon": -34.8911},

    # --- BR-101 (Trecho Urbano RMR) ---
    {"avenue": "BR-101", "point": "BR-101 - Segment 1: Altura da Guabiraba", "lat": -7.9712, "lon": -34.9255},
    {"avenue": "BR-101", "point": "BR-101 - Segment 2: Viaduto da Macaxeira", "lat": -8.0165, "lon": -34.9351},
    {"avenue": "BR-101", "point": "BR-101 - Segment 3: Entorno da UFPE", "lat": -8.0520, "lon": -34.9498},
    {"avenue": "BR-101", "point": "BR-101 - Segment 4: Altura do Ibura / Barro", "lat": -8.0864, "lon": -34.9472},
    {"avenue": "BR-101", "point": "BR-101 - Segment 5: Prazeres (Jaboatão)", "lat": -8.1511, "lon": -34.9415},

    # --- BR-232 / Saída Oeste Outskirts ---
    {"avenue": "BR-232", "point": "BR-232 - Segment 1: Início (Próx. ao Hospital Pelópidas Silveira)", "lat": -8.0931, "lon": -34.9752},
    {"avenue": "BR-232", "point": "BR-232 - Segment 2: Altura do Curado / CEASA", "lat": -8.0825, "lon": -34.9570},
    {"avenue": "BR-232", "point": "BR-232 - Segment 3: Conexão com BR-101", "lat": -8.0779, "lon": -34.9495},

    # --- Av. Eng. Abdias de Carvalho Outskirts ---
    {"avenue": "Av. Abdias de Carvalho", "point": "Abdias de Carvalho - Segment 1: Altura da Chesf (San Martin)", "lat": -8.0691, "lon": -34.9411},
    {"avenue": "Av. Abdias de Carvalho", "point": "Abdias de Carvalho - Segment 2: Cruzamento General San Martin", "lat": -8.0645, "lon": -34.9252},
    {"avenue": "Av. Abdias de Carvalho", "point": "Abdias de Carvalho - Segment 3: Próx. à Ilha do Retiro (Sport Club)", "lat": -8.0610, "lon": -34.9044},

    # --- Av. Dr. José Rufino Outskirts ---
    {"avenue": "Av. Dr. José Rufino", "point": "Av. José Rufino - Segment 1: Estância", "lat": -8.0792, "lon": -34.9295},
    {"avenue": "Av. Dr. José Rufino", "point": "Av. José Rufino - Segment 2: Areias / Barro", "lat": -8.0898, "lon": -34.9450},
    {"avenue": "Av. Dr. José Rufino", "point": "Av. José Rufino - Segment 3: Tejipió / Limite Jaboatão (Cavaleiro)", "lat": -8.0945, "lon": -34.9620},

    # --- Av. Beberibe Outskirts ---
    {"avenue": "Av. Beberibe", "point": "Av. Beberibe - Segment 1: Arruda (Próx. ao Estádio)", "lat": -8.0261, "lon": -34.8915},
    {"avenue": "Av. Beberibe", "point": "Av. Beberibe - Segment 2: Largo de Beberibe", "lat": -8.0112, "lon": -34.9002},
    {"avenue": "Av. Beberibe", "point": "Av. Beberibe - Segment 3: Altura de Porto da Madeira / Dois Unidos", "lat": -7.9998, "lon": -34.9085},

    # --- Av. Caxangá ---
    {"avenue": "Av. Caxangá", "point": "Av. Caxangá - Segment 1: Início (Madalena)", "lat": -8.0492, "lon": -34.9081},
    {"avenue": "Av. Caxangá", "point": "Av. Caxangá - Segment 2: Altura do Getúlio Vargas", "lat": -8.0431, "lon": -34.9282},
    {"avenue": "Av. Caxangá", "point": "Av. Caxangá - Segment 3: Próx. ao Parque de Exposição", "lat": -8.0368, "lon": -34.9455},
    {"avenue": "Av. Caxangá", "point": "Av. Caxangá - Segment 4: Final (Integrado da Caxangá / BR-101)", "lat": -8.0315, "lon": -34.9587},

    # --- Av. Norte Miguel Arraes ---
    {"avenue": "Av. Norte Miguel Arraes", "point": "Av. Norte - Segment 1: Cruzamento Cruz Cabugá", "lat": -8.0450, "lon": -34.8732},
    {"avenue": "Av. Norte Miguel Arraes", "point": "Av. Norte - Segment 2: Altura da Encruzilhada", "lat": -8.0352, "lon": -34.8911},
    {"avenue": "Av. Norte Miguel Arraes", "point": "Av. Norte - Segment 3: Largo de Casa Amarela", "lat": -8.0241, "lon": -34.9192},
    {"avenue": "Av. Norte Miguel Arraes", "point": "Av. Norte - Segment 4: Integração Macaxeira / Nova Descoberta", "lat": -8.0195, "lon": -34.9312},

    # --- Av. Mascarenhas de Morais ---
    {"avenue": "Av. Mascarenhas de Morais", "point": "Mascarenhas - Segment 1: Próx. à Imbiribeira", "lat": -8.0871, "lon": -34.9122},
    {"avenue": "Av. Mascarenhas de Morais", "point": "Mascarenhas - Segment 2: Passarela do Aeroporto", "lat": -8.1255, "lon": -34.9215},
    {"avenue": "Av. Mascarenhas de Morais", "point": "Mascarenhas - Segment 3: Limite Jaboatão (Prazeres)", "lat": -8.1450, "lon": -34.9248},

    # --- Via Mangue ---
    {"avenue": "Via Mangue", "point": "Via Mangue - Segment 1: Alça do Pina", "lat": -8.0902, "lon": -34.8904},
    {"avenue": "Via Mangue", "point": "Via Mangue - Segment 2: Trecho Central (Manguezal)", "lat": -8.1121, "lon": -34.8992},

    # --- Av. Recife ---
    {"avenue": "Av. Recife", "point": "Av. Recife - Segment 1: Entrada por Areias", "lat": -8.0772, "lon": -34.9311},
    {"avenue": "Av. Recife", "point": "Av. Recife - Segment 2: Cruzamento da Av. Ipsep", "lat": -8.1001, "lon": -34.9245},
]

# --- 2. DATA PROCESSING GENERATOR ---
@st.cache_data(ttl=60)
def generate_high_density_data():
    processed_records = []
    for entry in CORRIDOR_DATA:
        base_free_flow = random.randint(240, 500) # 4 to 8.5 minutes base
        
        heavy_routes = [
            "Av. Agamenon Magalhães", "BR-101", "PE-15", 
            "Av. Presidente Kennedy", "Av. Eng. Domingos Ferreira",
            "Av. Conselheiro Rosa e Silva", "Av. 17 de Agosto"
        ]
        jam_chance = 0.50 if entry["avenue"] in heavy_routes else 0.25
        
        is_jammed = random.random() < jam_chance
        if is_jammed:
            current_time = int(base_free_flow * random.uniform(1.5, 3.0))
        else:
            current_time = int(base_free_flow * random.uniform(0.95, 1.25))
            
        ratio = current_time / base_free_flow
        status = "Critical" if ratio >= THRESHOLD_RATIO else "Healthy"
        color = [230, 57, 70, 210] if status == "Critical" else [46, 139, 87, 210]
        
        processed_records.append({
            "Avenue": entry["avenue"],
            "Checkpoint": entry["point"],
            "Latitude": entry["lat"],
            "Longitude": entry["lon"],
            "Free Flow (min)": round(base_free_flow / 60, 1),
            "Current Time (min)": round(current_time / 60, 1),
            "Delay Ratio": round(ratio, 2),
            "Status": status,
            "Color": color
        })
    return pd.DataFrame(processed_records)

# Load data matrix
raw_df = generate_high_density_data()

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.title("RMR Filter Panel")
st.sidebar.markdown("Filter specific arterial grids or outer ring segments.")

avenues_available = sorted(raw_df["Avenue"].unique())
selected_avenues = st.sidebar.multiselect("Select Avenues to View", avenues_available, default=avenues_available)
df = raw_df[raw_df["Avenue"].isin(selected_avenues)].reset_index(drop=True)

# --- 4. GLOBAL HEALTH OVERVIEW ---
st.title("🚦 Recife Metro High-Density Traffic Grid")
st.markdown(f"Real-time macro monitoring covering **{len(df)} checkpoints** across the RMR network.")

total_points = len(df)
critical_points = len(df[df["Status"] == "Critical"])
health_index = int(((total_points - critical_points) / total_points) * 100) if total_points > 0 else 100

# --- NEW: Recife Standard City-Wide Status Logic ---
if health_index >= 75:
    city_status, color, icon = "Normal / Mild Flow", "green", "🟢"
elif health_index >= 50:
    city_status, color, icon = "Moderate Congestion", "orange", "🟡"
else:
    city_status, color, icon = "Severe Gridlock", "red", "🔴"

# Display the Human-Readable Status
st.markdown(f"### Current City Status: {icon} **<span style='color:{color}'>{city_status}</span>**", unsafe_allow_html=True)

# Explanation for newcomers
st.info("💡 **How to read this dashboard (Recife Standards):** The Health Index represents the percentage of roads flowing without major delays. A score below **75%** indicates moderate, expected rush-hour congestion, while dropping below **50%** means severe, widespread city gridlock.")

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
with kpi_col1:
    st.metric(label="RMR Network Health Index", value=f"{health_index}%", delta="Target: >80%")
with kpi_col2:
    st.metric(label="Total Monitored Segments", value=total_points)
with kpi_col3:
    st.metric(label="Active Bottlenecks Triggered", value=critical_points, delta=f"{critical_points} Alert States", delta_color="inverse")

critical_list = df[df["Status"] == "Critical"]["Checkpoint"].tolist()
if critical_list:
    st.error(f"⚠️ **{len(critical_list)} Segments Exceeded Threshold:** {', '.join(critical_list[:3])} ... and more have matched your alert parameters.")
else:
    st.success("✅ Operational Flow: All outer and inner ring routes are flowing within normal health thresholds.")

st.markdown("---")

# --- 5. VISUALIZATION DIVIDER: MAP VS DATA GRID ---
col_map, col_list = st.columns([3, 2])

with col_map:
    st.subheader("Geographical Distribution Map")
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position=["Longitude", "Latitude"],
        get_color="Color",
        get_radius=380,
        pickable=True,
        auto_highlight=True,
    )
    
    view_state = pdk.ViewState(
        latitude=-8.0650, 
        longitude=-34.9100, 
        zoom=11.0, 
        pitch=25
    )
    
    st.pydeck_chart(pdk.Deck(
        map_provider="carto",
        map_style="light",
        layers=[layer], 
        initial_view_state=view_state,
        tooltip={"text": "{Avenue}\n{Checkpoint}\nDelay Factor: {Delay Ratio}x\nTime: {Current Time (min)} min"}
    ))

with col_list:
    st.subheader("Top Worst Performing Segments")
    worst_segments = df.sort_values(by="Delay Ratio", ascending=False).head(8)
    
    for _, row in worst_segments.iterrows():
        status_emoji = "🔴" if row["Status"] == "Critical" else "🟢"
        st.markdown(f"**{status_emoji} {row['Checkpoint']}**")
        st.caption(f"Flow Delay: {row['Delay Ratio']}x — Live: {row['Current Time (min)']}m / Ideal: {row['Free Flow (min)']}m")
        st.progress(min(float(row["Delay Ratio"]) / 3.0, 1.0))

st.markdown("---")

# --- 6. DATA MATRIX EXPANDER ---
with st.expander("Inspect Raw RMR Metrics Registry"):
    st.dataframe(df.drop(columns=["Color"]), width="stretch")
    st.caption(f"System synchronized at: {datetime.now().strftime('%H:%M:%S')}")