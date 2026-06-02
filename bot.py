import os
import requests
import pandas as pd
import random
from datetime import datetime

# Grab the hidden secrets from GitHub
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")
API_KEY = os.environ.get("WHATSAPP_API_KEY")

# (Truncated for space, but you would paste your exact CORRIDOR_DATA list here)
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


def send_whatsapp_alert(health_index, df):
    # Find which avenues are failing to include in the message
    critical_avenues = df[df["Status"] == "Critical"]["Avenue"].unique()
    avenues_text = ", ".join(critical_avenues[:3]) # Top 3 problem areas
    
    message = f"🚨 *Recife Traffic Alert* 🚨\n\nCity Health Index has dropped to *{health_index}%*.\n\nMajor bottlenecks detected on: {avenues_text}."
    
    # CallMeBot API URL
    url = f"https://api.callmebot.com/whatsapp.php?phone={PHONE_NUMBER}&text={message}&apikey={API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        print("WhatsApp alert sent successfully!")
    else:
        print("Failed to send alert.")

def check_traffic():
    processed_records = []
    current_hour = datetime.now().hour
    is_rush_hour = current_hour in [7, 8, 9, 17, 18, 19]
    
    for entry in CORRIDOR_DATA:
        base_free_flow = random.randint(240, 500) 
        heavy_routes = ["Av. Agamenon Magalhães", "BR-101", "PE-15", "Av. Presidente Kennedy", "Av. Eng. Domingos Ferreira", "Av. Conselheiro Rosa e Silva", "Av. 17 de Agosto"]
        
        jam_chance = 0.45 if (is_rush_hour and entry["avenue"] in heavy_routes) else 0.10
        is_jammed = random.random() < jam_chance
        
        current_time = int(base_free_flow * random.uniform(1.5, 2.2)) if is_jammed else int(base_free_flow * random.uniform(0.95, 1.15))
        ratio = current_time / base_free_flow
        status = "Critical" if ratio >= 1.5 else "Healthy"
        
        processed_records.append({"Status": status, "Avenue": entry["avenue"]})
        
    df = pd.DataFrame(processed_records)
    total_points = len(df)
    critical_points = len(df[df["Status"] == "Critical"])
    health_index = int(((total_points - critical_points) / total_points) * 100) if total_points > 0 else 100
    
    print(f"Current RMR Health Index: {health_index}%")
    
    # THRESHOLD CHECK: 60% or below
    if health_index <= 60:
        send_whatsapp_alert(health_index, df)


if __name__ == "__main__":
    check_traffic()