
# import streamlit as st
# import pandas as pd
# from PIL import Image
# from datetime import datetime
# from pymongo import MongoClient
# import io
# import certifi
# from pymongo.server_api import ServerApi

# # Configuração do tema escuro
# st.set_page_config(page_title="AgroSense", layout="wide")

# st.markdown("""
#     <style>
#         body {
#             background-color: #121212;
#             color: white;
#         }
#         .navbar {
#             background-color: #FFD700;
#             padding: 10px;
#             text-align: left;
#             font-size: 24px;
#             font-weight: bold;
#             color: black;
#         }
#         .stButton>button {
#             background-color: #FFD700;
#             color: black;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # 🔗 Conectar ao MongoDB com tempo limite aumentado
# MONGO_URI = "mongodb+srv://WillyKevin:Sense2025@clustersense.me11j.mongodb.net/?retryWrites=true&w=majority"
# try:
#     client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), server_api=ServerApi('1'), serverSelectionTimeoutMS=50000)
#     db = client["ClusterSense"]
#     collection = db["Insetos"]
#     st.success("Conexão com MongoDB estabelecida com sucesso!")
# except Exception as e:
#     st.error(f"Erro ao conectar ao MongoDB: {e}")

# # Navbar
# st.markdown('<div class="navbar">AgroSense</div>', unsafe_allow_html=True)

# # 📤 Modal de Upload
# st.sidebar.header("Upload de Imagens")
# uploaded_files = st.sidebar.file_uploader("Escolha imagens", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# # Estruturas para armazenar dados
# image_data = []
# table_data = []

# # Processamento das imagens carregadas
# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         image = Image.open(uploaded_file)
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         date, time = timestamp.split(" ")

#         image_data.append((len(table_data) + 1, image))
#         table_data.append({"ID": len(table_data) + 1, "Nome": uploaded_file.name, "Data": date, "Hora": time})

# # 🟦 **Tabela Azul** (numeração automática das imagens)
# df_blue = pd.DataFrame(table_data)
# st.write("### Imagens Anotadas")
# st.dataframe(df_blue)

# # 🟩 **Tabela Verde** (informações adicionais manualmente preenchidas)
# st.write("### Informações Detalhadas")

# # Se ainda não existir no session_state, cria a estrutura inicial
# if "df_green" not in st.session_state:
#     st.session_state.df_green = pd.DataFrame(columns=["ID", "Detalhes"])

# # Criar nova tabela apenas com IDs das imagens carregadas
# new_entries = pd.DataFrame({"ID": [row["ID"] for row in table_data], "Detalhes": [""] * len(table_data)})

# # Atualiza o dataframe do session_state sem sobrescrever os detalhes já preenchidos
# df_existing = st.session_state.df_green.set_index("ID")  # Converte para índice
# df_new = new_entries.set_index("ID")  # Converte para índice

# # Garante que novos IDs sejam adicionados, mantendo os detalhes antigos
# df_combined = df_existing.combine_first(df_new).reset_index()

# # Atualiza o session_state para refletir os novos dados
# st.session_state.df_green = df_combined

# # Exibe a tabela editável sem perder valores antigos
# edited_df = st.data_editor(st.session_state.df_green, num_rows="fixed", disabled=["ID"])

# # Salva a versão editada de volta no session_state
# st.session_state.df_green = edited_df

# # 🖼 Exibir imagens com contador
# if image_data:
#     st.write("### Carrossel de Imagens")
#     for img_id, img in image_data:
#         st.image(img, use_column_width=True, caption=f"Imagem {img_id}")

# # 💾 **Salvar no MongoDB**
# def save_to_mongo(df_blue, edited_df, image_data):
#     if not df_blue.empty and not edited_df.empty:
#         try:
#             for img_id, img in image_data:
#                 img_byte_arr = io.BytesIO()
                
#                 # 🔹 Reduz tamanho da imagem e comprime para evitar timeout
#                 img = img.resize((500, 500))  
#                 img.save(img_byte_arr, format='JPEG', quality=50)  
#                 img_bytes = img_byte_arr.getvalue()
                
#                 doc = {
#                     "ID": img_id,
#                     "Imagem": img_bytes,
#                     "Tabela_Identificacao": df_blue.to_dict(orient="records"),
#                     "Tabela_Atributos": edited_df.to_dict(orient="records"),
#                     "Data_Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 }

#                 # 🔹 Inserir cada documento individualmente para evitar sobrecarga
#                 collection.insert_one(doc)
#                 st.success(f"Imagem {img_id} enviada com sucesso!")

#         except Exception as e:
#             st.error(f"Erro ao salvar no MongoDB: {e}")
#     else:
#         st.warning("Nenhuma imagem ou tabela para salvar!")

# # 📤 **Botão para enviar dados ao MongoDB**
# if st.button("Enviar Informações", key="send_button", use_container_width=True):
#     save_to_mongo(df_blue, edited_df, image_data)

# # ⬇️ **Opção de Download**
# if not df_blue.empty:
#     st.download_button("Baixar Tabelas", df_blue.to_csv().encode("utf-8"), "tabelas.csv", "text/csv", key="download_csv", use_container_width=True)

import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
from pymongo import MongoClient
import io
import certifi
from pymongo.server_api import ServerApi

# Configuração do tema escuro
st.set_page_config(page_title="AgroSense", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .navbar {
            background-color: #FFD700;
            padding: 10px;
            text-align: left;
            font-size: 24px;
            font-weight: bold;
            color: black;
        }
        .stButton>button {
            background-color: #FFD700;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

# 🔗 Conectar ao MongoDB com tempo limite aumentado
MONGO_URI = "mongodb+srv://WillyKevin:Sense2025@clustersense.me11j.mongodb.net/?retryWrites=true&w=majority"
try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), server_api=ServerApi('1'), serverSelectionTimeoutMS=50000)
    db = client["ClusterSense"]
    collection = db["Insetos"]
    st.success("Conexão com MongoDB estabelecida com sucesso!")
except Exception as e:
    st.error(f"Erro ao conectar ao MongoDB: {e}")

# Navbar
st.markdown('<div class="navbar">AgroSense</div>', unsafe_allow_html=True)

# 📤 Modal de Upload
st.sidebar.header("Upload de Imagens")
uploaded_files = st.sidebar.file_uploader("Escolha imagens", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# Estruturas para armazenar dados
image_data = []
table_data = []

# Processamento das imagens carregadas
if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date, time = timestamp.split(" ")

        image_data.append((len(table_data) + 1, image))
        table_data.append({"ID": len(table_data) + 1, "Nome": uploaded_file.name, "Data": date, "Hora": time})

# 🟦 **Tabela Azul** (numeração automática das imagens)
df_blue = pd.DataFrame(table_data)
st.write("### Imagens Anotadas")
st.dataframe(df_blue)

# 🟩 **Tabela Verde** (informações adicionais manualmente preenchidas)
st.write("### Informações Detalhadas")

# Se ainda não existir no session_state, cria a estrutura inicial
if "df_green" not in st.session_state:
    st.session_state.df_green = pd.DataFrame(columns=["ID", "Detalhes"])

# Criar nova tabela apenas com IDs das imagens carregadas
new_entries = pd.DataFrame({"ID": [row["ID"] for row in table_data], "Detalhes": [""] * len(table_data)})

# Atualiza o dataframe do session_state sem sobrescrever os detalhes já preenchidos
df_existing = st.session_state.df_green.set_index("ID")  # Converte para índice
df_new = new_entries.set_index("ID")  # Converte para índice

# Garante que novos IDs sejam adicionados, mantendo os detalhes antigos
df_combined = df_existing.combine_first(df_new).reset_index()

# Atualiza o session_state para refletir os novos dados
st.session_state.df_green = df_combined

# Exibe a tabela editável sem perder valores antigos
edited_df = st.data_editor(st.session_state.df_green, num_rows="fixed", disabled=["ID"])

# Salva a versão editada de volta no session_state
st.session_state.df_green = edited_df

# 🖼 Exibir imagens com contador
if image_data:
    st.write("### Carrossel de Imagens")
    for img_id, img in image_data:
        st.image(img, use_column_width=True, caption=f"Imagem {img_id}")

# 💾 **Salvar no MongoDB**
def save_to_mongo(df_blue, edited_df, image_data):
    if not df_blue.empty and not edited_df.empty:
        try:
            for img_id, img in image_data:
                img_byte_arr = io.BytesIO()
                
                # 🔹 Reduz tamanho da imagem e comprime para evitar timeout
                img = img.resize((500, 500))  
                img.save(img_byte_arr, format='JPEG', quality=50)  
                img_bytes = img_byte_arr.getvalue()
                
                doc = {
                    "ID": img_id,
                    "Imagem": img_bytes,
                    "Tabela_Identificacao": df_blue.to_dict(orient="records"),
                    "Tabela_Atributos": edited_df.to_dict(orient="records"),
                    "Data_Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # 🔹 Inserir cada documento individualmente para evitar sobrecarga
                collection.insert_one(doc)
                st.success(f"Imagem {img_id} enviada com sucesso!")

        except Exception as e:
            st.error(f"Erro ao salvar no MongoDB: {e}")
    else:
        st.warning("Nenhuma imagem ou tabela para salvar!")

# 📤 **Botão para enviar dados ao MongoDB**
if st.button("Enviar Informações", key="send_button", use_container_width=True):
    save_to_mongo(df_blue, edited_df, image_data)

# ⬇️ **Opção de Download**
if not df_blue.empty and not edited_df.empty:
    combined_df = df_blue.merge(edited_df, on="ID", how="left")
    st.download_button("Baixar Tabelas", combined_df.to_csv().encode("utf-8"), "tabelas.csv", "text/csv", key="download_csv", use_container_width=True)
