import streamlit as st
import openai
from PIL import Image
import base64
from io import BytesIO

# ✅ Configuração inicial da página (tem que ser o primeiro comando!)
st.set_page_config(page_title="✨ Bia ✨")

# ✅ Função para converter imagem local em base64
def get_image_base64(img_path):
    img = Image.open(img_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    return img_base64

# ✅ Carrega imagem e renderiza HTML com estilo circular centralizado
img_base64 = get_image_base64("BIA.png")
st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{img_base64}' width='120' style='border-radius: 50%; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); margin-bottom: 10px;' />
        <h2>✨ Bia ✨</h2>
        <p style='font-size: 16px;'>Ei, eu sou a BIA (Bold Inteligência Artificial), sua assistente da Bold!<br>
        Tô aqui para DESCOMPLICAR seu dia: Atividades mais rápidas, Conversas eficientes e tirar dúvidas!</p>
    </div>
    """,
    unsafe_allow_html=True
)


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
