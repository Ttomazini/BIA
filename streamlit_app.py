import streamlit as st
import openai
from PIL import Image

# Exibir imagem da BIA
bia_image = Image.open("BIA.png")  # nome com letras maiúsculas, igual ao arquivo no repositório
st.image(bia_image, width=150)

# Configuração inicial da página
st.set_page_config(page_title="✨ Bia ✨")
st.title("✨ Bia ✨")
st.write("Ei, eu sou a BIA (Bold Inteligência Artificial), sua assistente da Bold! Tô aqui para DESCOMPLICAR seu dia: Atividades mais rápidas, Conversas eficientes e tirar dúvidas!")

# Configuração da API Key via arquivo secreto
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ID do assistente criado na plataforma OpenAI
assistant_id = "asst_HgFhlVBy2xLofnuBdDBMVzli"

# Inicializar a conversa (thread)
if "thread_id" not in st.session_state:
    thread = openai.beta.threads.create()
    st.session_state.thread_id = thread.id

# Exibir histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input para pergunta
if prompt := st.chat_input("Digite sua pergunta aqui"):

    # Exibir pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Enviar pergunta para o Assistente
    openai.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt
    )

    run = openai.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id
    )

    # Aguarda a resposta
    with st.spinner("BIA está respondendo..."):
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break

    # Recuperar resposta
    messages = openai.beta.threads.messages.list(thread_id=st.session_state.thread_id)
    resposta = messages.data[0].content[0].text.value

    # Exibir resposta
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)
