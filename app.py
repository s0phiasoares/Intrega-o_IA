import os
import streamlit as st
from google import genai
from google.genai import types

def converter_para_gemini(historico):
    mensagens_gemini = []


    for mensagem in historico:
        papel = mensagem["role"]
        conteudo = mensagem["content"]


        if papel == "assistant":
            papel_gemini = "model"
        else:
            papel_gemini = "user"


        mensagens_gemini.append(
            types.Content(
                role=papel_gemini,
                parts=[types.Part.from_text(text=conteudo)]
            )
        )


    return mensagens_gemini


def gerar_resposta():
    try:
        resposta = cliente.models.generate_content(
            model=MODELO,
            contents=converter_para_gemini(st.session_state.historico),
            config=types.GenerateContentConfig(
                system_instruction=INSTRUCAO_SISTEMA,
                temperature=0.4,
            )
        )
    
    
        return resposta.text
        except:
            return "Ocorreu um erro ao se comunicar com o Gemini, tente novamente mias tarde!"

MODELO = "gemini-2.5-flash"

INSTRUCAO_SISTEMA = """
Você é um minion.
Responda em Português do Brasil, com clareza e seja criativo com as respostas.
Enquanto mais a pergunta for besta, a resposta vai ser mais divertida.
Se faltar informação, faça 1 pergunta curta antes de responder.
"""

st.set_page_config(page_title="Minions chatbot", page_icon="🍌")
st.title("Chatbot com os minions 🪢🟡")
st.subheader("Para tu os Minions, askete qualquer coisa! Poopaye pergunta muito bobo, okay? Bananaaa! 🤪🍌") 

chave_api = st.sidebar.text_input("Insira sua chave de API", type="password")

if not chave_api:
    st.warning("⚠️ Você precisa inserir uma chave de API para continuar.")
    st.stop()

cliente = genai.Client(api_key=chave_api)

if "historico" not in st.session_state:
    st.session_state.historico = []

for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])


entrada_usuario = st.chat_input("Digite sua pergunta: ")

if entrada_usuario:
    st.session_state.historico.append(
        {
           "role" : "user",
           "content":entrada_usuario
        }
    )
    with st.chat_message("user"): #ADICIONANDO A MENSAGEM AO CHAT
        st.markdown(entrada_usuario)

    with st.chat_message("assistant"):
        resposta_ia = gerar_resposta()
        st.markdown(resposta_ia)

    st.session_state.historico.append(
        {
            "role":"assistant",
            "content":resposta_ia
        }
    )
