import streamlit as st
from PIL import Image
import easyocr
import numpy as np

# --- Конфигурация ---
st.set_page_config(page_title="OCR Проверка на съставки", layout="centered")

st.title("📷 Разпознаване на съставки от снимка")
st.write("Качи снимка на етикет и ще проверим за потенциално вредни съставки.")

# --- Списък с вредни съставки ---
harmful_ingredients = [
    "e621", "e622", "e623",
    "palm oil", "palmitate", "palm fat",
    "аспартам", "aspartame",
    "msg", "monosodium glutamate",
    "консерванти", "preservatives",
    "оцветители", "colorants"
]

# --- Качване на изображение ---
uploaded_file = st.file_uploader("Качи снимка", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Качено изображение", use_container_width=True)

    # --- OCR ---
    with st.spinner("🔍 Разпознаване на текст..."):
        reader = easyocr.Reader(['bg', 'en'])  # Български + Английски
        result = reader.readtext(np.array(image), detail=0)

    # Обединяване на текста
    extracted_text = " ".join(result).lower()

    st.subheader("📄 Разпознат текст:")
    st.write(extracted_text)

    # --- Търсене на вредни съставки ---
    found = []
    for ingredient in harmful_ingredients:
        if ingredient in extracted_text:
            found.append(ingredient)

    # --- Резултати ---
    st.subheader("⚠️ Анализ на съставките:")

    if found:
        st.error("Намерени потенциално вредни съставки:")
        for item in found:
            st.write(f"❌ {item}")
    else:
        st.success("Не са открити известни вредни съставки.")

    # --- Допълнително ---
    st.info("ℹ️ Забележка: Това е базова проверка и не замества експертна оценка.")
