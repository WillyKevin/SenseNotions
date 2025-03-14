
import streamlit as st
import pandas as pd
from PIL import Image
import io
import os
from pymongo import MongoClient
import certifi
from pymongo.server_api import ServerApi

# 🔗 Conectar ao MongoDB com tempo limite aumentado
MONGO_URI = "mongodb+srv://WillyKevin:Sense2025@clustersense.me11j.mongodb.net/?retryWrites=true&w=majority"
try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), server_api=ServerApi('1'), serverSelectionTimeoutMS=50000)
    db = client["ClusterSense"]
    collection = db["Insetos"]
    st.success("Conexão com MongoDB estabelecida com sucesso!")
except Exception as e:
    st.error(f"Erro ao conectar ao MongoDB: {e}")

# 📂 Criar pasta local para salvar arquivos
SAVE_DIR = "dados_agrosense"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# 🔍 Verificar arquivos já salvos para evitar duplicatas
existing_files = set(os.listdir(SAVE_DIR))

# 📥 **Botão para Buscar Dados e Salvar**
if st.button("Carregar e Salvar Dados do MongoDB"):
    try:
        documents = list(collection.find())  # Obtém todos os documentos da coleção
        
        if not documents:
            st.warning("Nenhum dado encontrado no MongoDB!")
        else:
            total_image_size = 0  # Para armazenar tamanho total das imagens
            total_table_size = 0  # Para armazenar tamanho total das tabelas
            
            st.write("## 🔍 Dados Recuperados e Salvos")

            for doc in documents:
                img_id = str(doc["ID"])
                timestamp = doc["Data_Hora"].replace(":", "-").replace(" ", "_")  # Evita problemas com nomes de arquivos
                
                # 🔹 Definir nomes dos arquivos para evitar duplicatas
                img_filename = f"imagem_{img_id}_{timestamp}.jpg"
                csv_identificacao = f"identificacao_{img_id}_{timestamp}.csv"
                csv_atributos = f"atributos_{img_id}_{timestamp}.csv"

                # 🖼 Salvar Imagem (se ainda não existir)
                if img_filename not in existing_files:
                    img_bytes = doc["Imagem"]
                    total_image_size += len(img_bytes)  # Soma tamanho das imagens
                    image = Image.open(io.BytesIO(img_bytes))
                    image.save(os.path.join(SAVE_DIR, img_filename))
                    existing_files.add(img_filename)
                    st.success(f"Imagem {img_filename} salva!")

                # 📊 Salvar Tabela de Identificação (se ainda não existir)
                if csv_identificacao not in existing_files:
                    df_blue = pd.DataFrame(doc["Tabela_Identificacao"])
                    df_blue.to_csv(os.path.join(SAVE_DIR, csv_identificacao), index=False)
                    total_table_size += df_blue.memory_usage(deep=True).sum()
                    existing_files.add(csv_identificacao)
                    st.success(f"Tabela Identificação {csv_identificacao} salva!")

                # 📊 Salvar Tabela de Atributos (se ainda não existir)
                if csv_atributos not in existing_files:
                    df_green = pd.DataFrame(doc["Tabela_Atributos"])
                    df_green.to_csv(os.path.join(SAVE_DIR, csv_atributos), index=False)
                    total_table_size += df_green.memory_usage(deep=True).sum()
                    existing_files.add(csv_atributos)
                    st.success(f"Tabela Atributos {csv_atributos} salva!")
            
            # 📏 Exibir tamanhos totais
            st.write("## 📊 Tamanhos Totais")
            st.write(f"📷 **Tamanho total das imagens:** {total_image_size / 1024:.2f} KB")
            st.write(f"📄 **Tamanho total das tabelas:** {total_table_size / 1024:.2f} KB")

    except Exception as e:
        st.error(f"Erro ao buscar e salvar dados: {e}")

