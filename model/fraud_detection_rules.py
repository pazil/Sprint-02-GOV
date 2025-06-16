import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def classify_call(row):
    """
    Classifies a support call based on a rule-based scoring system.
    """
    score = 0
    
    # Rule 1: Frequency
    if row['frequencia_chamados_6_meses'] > 2:
        score += 30
        
    # Rule 2: Error Type
    if row['tipo_erro_reportado'] in ["vazamento de tinta", "danificou a impressora"]:
        score += 40
    elif row['tipo_erro_reportado'] == "falha de reconhecimento":
        score += 20
        
    # Rule 3: Registration
    if not row['cartucho_registrado']:
        score += 30
        
    # Final Classification
    if score > 70:
        return "Alta Probabilidade de Falsificação"
    elif 40 <= score <= 70:
        return "Suspeita Moderada"
    else:
        return "Baixa Probabilidade"

def generate_synthetic_data(num_records=1000):
    """
    Generates synthetic data aligned with the rule-based model.
    """
    np.random.seed(42)
    customers = [f"C{i:04d}" for i in range(1, 201)]
    
    # Add states to each region for more granular analysis
    regions_and_states = {
        "Nordeste": ["BA", "PE", "CE", "MA"],
        "Sul": ["RS", "SC", "PR"],
        "Sudeste": ["SP", "RJ", "MG", "ES"],
        "Norte": ["AM", "PA", "TO", "AC"],
        "Centro-Oeste": ["GO", "MT", "MS", "DF"]
    }
    regions = list(regions_and_states.keys())
    
    error_types = ["vazamento de tinta", "falha de reconhecimento", "baixa qualidade de impressão", "danificou a impressora", "outro"]
    
    data = []
    
    # Change region weights to avoid the "NE 3x Sul" scenario. Sudeste now has more.
    region_weights_fake = [0.25, 0.20, 0.35, 0.10, 0.10] # NE, Sul, Sudeste, Norte, CO

    for _ in range(num_records):
        # Generate base data
        customer_id = np.random.choice(customers)
        is_fake = np.random.rand() < 0.35  # 35% of calls are related to fake products

        if is_fake:
            # High-risk profile
            frequencia = np.random.randint(3, 6)
            tipo_erro = np.random.choice(["vazamento de tinta", "danificou a impressora", "falha de reconhecimento"], p=[0.5, 0.3, 0.2])
            cartucho_registrado = False
            cartridge_type = "falsificado"
            # Adjusted NPS for fakes
            nps = np.random.randint(0, 4) # 0-3
            returned = True
            # Generate region based on new weights
            region = np.random.choice(regions, p=region_weights_fake)
        else:
            # Low-risk profile
            frequencia = np.random.randint(1, 3)
            tipo_erro = np.random.choice(["baixa qualidade de impressão", "falha de reconhecimento", "outro"], p=[0.5, 0.3, 0.2])
            cartucho_registrado = True
            is_original = np.random.rand() < 0.8
            if is_original:
                cartridge_type = "original"
                # Adjusted NPS for original to not match the example
                nps = np.random.randint(6, 11) # NPS will be around 80
            else:
                cartridge_type = "generico"
                # Adjusted NPS for generic to not match the example
                nps = np.random.randint(3, 8) # NPS will be around 50
            returned = np.random.choice([True, False], p=[0.1, 0.9])
            # Generate region randomly for non-fakes
            region = np.random.choice(regions)
            
        # Select a random state from the chosen region
        state = np.random.choice(regions_and_states[region])
        call_date = datetime.now() - timedelta(days=np.random.randint(1, 365))
            
        data.append({
            "id_chamado": f"CH{1000 + _}",
            "customer_id": customer_id,
            "frequencia_chamados_6_meses": frequencia,
            "tipo_erro_reportado": tipo_erro,
            "cartucho_registrado": cartucho_registrado,
            "call_date": call_date.strftime("%Y-%m-%d"),
            "region": region,
            "state": state, # Add state column
            "cartridge_type": cartridge_type,
            "nps": nps,
            "returned": returned,
        })
        
    df = pd.DataFrame(data)
    
    # Apply the classification logic to the generated data
    df['classificacao_risco'] = df.apply(classify_call, axis=1)
    
    # Save the data
    df.to_csv('data/synthetic_data.csv', index=False)
    print(f"Generated {num_records} records and saved to 'data/synthetic_data.csv'")

if __name__ == "__main__":
    generate_synthetic_data() 