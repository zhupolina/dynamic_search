import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Картины Клода Моне — Поиск",
    layout="wide"
)

st.markdown("""
<style>

/* Основной фон */
html, body, .main, .stApp {
    background-color: #e8f6ff !important;
    color: #222 !important;
    font-family: 'Times New Roman', serif !important;
}

/* Заголовки */
h1, h2, h3, h4, h5, h6 {
    color: #ff69b4 !important;
    font-weight: 700 !important;
    font-family: 'Times New Roman', serif !important;
}

/* Обычный текст */
p, label, span, div {
    color: #222 !important;
    font-family: 'Times New Roman', serif !important;
}

/* Текст результатов поиска */
.stMarkdown, .markdown-text-container {
    color: #222 !important;
    font-family: 'Times New Roman', serif !important;
}

/* Поле ввода */
input[type="text"] {
    background-color: #ffffff !important;
    border: 2px solid #ffb6d9 !important;
    color: #222 !important;
    border-radius: 10px !important;
    font-family: 'Times New Roman', serif !important;
}

/* Кнопки */
button, .stButton > button {
    background-color: #ffb6d9 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    border: 2px solid #ff69b4 !important;
    padding: 8px 16px !important;
    font-weight: 600 !important;
    font-family: 'Times New Roman', serif !important;
}

button:hover, .stButton > button:hover {
    background-color: #ff8fc8 !important;
    border-color: #ff1493 !important;
}

/* Кастомные блоки */
.custom-box {
    background-color: #d7efff !important;
    border: 2px solid #ffb6d9 !important;
    border-radius: 15px !important;
    padding: 15px !important;
    color: #222 !important;
    font-family: 'Times New Roman', serif !important;
}

/* Списки */
ul, li {
    color: #222 !important;
    font-family: 'Times New Roman', serif !important;
}

/* Горизонтальная линия */
hr {
    border: 1px solid #ffb6d9 !important;
}

/* Ссылки */
a { 
    text-decoration: none !important;
    font-family: 'Times New Roman', serif !important;
}

/* Стеклянная кнопка "Назад на главную" */
.glass-btn {
    width: 100%;
    padding: 12px 20px;
    font-size: 18px;
    font-family: 'Times New Roman', serif;
    font-weight: 600;
    color: #ff1493;
    text-align: center;
    border-radius: 15px;
    border: 2px solid rgba(255, 182, 217, 0.6);
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 8px 20px rgba(255, 105, 180, 0.25);
    cursor: pointer;
    transition: all 0.25s ease;
}

.glass-btn:hover {
    background: rgba(255, 255, 255, 0.45);
    box-shadow: 0 8px 25px rgba(255, 105, 180, 0.4);
    border-color: rgba(255, 105, 180, 0.9);
    color: #ff007f;
}

.glass-btn:active {
    transform: scale(0.97);
}

</style>
""", unsafe_allow_html=True)

if 'GROQ_API_KEY' in st.secrets:
    GROQ_API_KEY = st.secrets['GROQ_API_KEY']
else:
    st.error("Ключ GROQ_API_KEY не найден в секретах.")
    GROQ_API_KEY = None

st.title("Поиск актуальной информации о творчестве Клода Моне")

def search_news(query):
    """Поиск новостей через Groq API"""
    if not GROQ_API_KEY:
        return None

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""Найди самые актуальные новости и информацию по запросу, кроме самих новостей не пиши ничего, не относящегося к новости: {query}
    Верни ответ в формате:
    - Новость 1
    - Новость 2
    - Новость 3"""

    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama-3.1-8b-instant",
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Ошибка API: {response.status_code}"
    except Exception as e:
        return f"Ошибка: {str(e)}"

search_query = st.text_input("Ваш запрос:", placeholder="Например: Самая популярная картина Клода Моне")

if search_query:
    with st.spinner("Ищем информацию..."):
        results = search_news(search_query)
        if results:
            st.subheader("Результаты поиска:")
            st.write(results)
        else:
            st.error("Не удалось выполнить поиск")

st.header("Примеры запросов:")
st.markdown("""
- **Самая дорогая картина Клода Моне**  
- **Популярные серии картин Клода Моне**  
- **Последний аукцион по продаже картин Клода Моне**  
- **Жанры, в которых работал Моне**  
""")

st.markdown("""
<a href="https://creative-marscapone-486.notion.site/2b1c3df492be8046aaadca5da0034963?pvs=73" target="_blank">
    <div class="glass-btn">Назад на главную страницу</div>
</a>
""", unsafe_allow_html=True)
