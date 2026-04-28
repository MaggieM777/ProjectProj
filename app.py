import streamlit as st
import math
import random
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Тригонометрични функции - 11 клас")

st.title("📐 Тригонометрични функции - упражнения")

# --- Сесия ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "questions_answered" not in st.session_state:
    st.session_state.questions_answered = 0
if "history" not in st.session_state:
    st.session_state.history = []

# --- Генериране на задачи ---
def generate_question():
    q_type = random.choice(["sin", "cos", "tan"])

    angle = random.choice([0, 30, 45, 60, 90])

    if q_type == "sin":
        correct = round(math.sin(math.radians(angle)), 2)
        question = f"sin({angle}°) = ?"
    elif q_type == "cos":
        correct = round(math.cos(math.radians(angle)), 2)
        question = f"cos({angle}°) = ?"
    else:
        if angle == 90:
            return generate_question()
        correct = round(math.tan(math.radians(angle)), 2)
        question = f"tg({angle}°) = ?"

    return question, correct


# --- Нова задача ---
if "current_question" not in st.session_state:
    st.session_state.current_question = generate_question()

question, correct_answer = st.session_state.current_question

st.subheader("📝 Задача:")
st.write(question)

user_answer = st.text_input("Въведи отговора (закръгли до 2 знака):")

if st.button("Провери"):
    try:
        user_value = float(user_answer)

        is_correct = abs(user_value - correct_answer) < 0.01

        st.session_state.questions_answered += 1

        if is_correct:
            st.success("✅ Вярно!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Грешно! Верният отговор е {correct_answer}")

        # запис за статистика
        st.session_state.history.append({
            "Въпрос": question,
            "Твоят отговор": user_value,
            "Правилен": correct_answer,
            "Верен ли е": is_correct
        })

        # нова задача
        st.session_state.current_question = generate_question()

    except:
        st.warning("⚠️ Моля въведи число!")


# --- Резултати ---
st.sidebar.title("📊 Резултати")
st.sidebar.write(f"Решени задачи: {st.session_state.questions_answered}")
st.sidebar.write(f"Верни отговори: {st.session_state.score}")

if st.session_state.questions_answered > 0:
    accuracy = (st.session_state.score / st.session_state.questions_answered) * 100
    st.sidebar.write(f"Успеваемост: {accuracy:.2f}%")

# --- Графика ---
if len(st.session_state.history) > 0:
    df = pd.DataFrame(st.session_state.history)

    correct_count = df["Верен ли е"].sum()
    wrong_count = len(df) - correct_count

    st.subheader("📈 Статистика")

    fig, ax = plt.subplots()
    ax.bar(["Верни", "Грешни"], [correct_count, wrong_count])
    ax.set_ylabel("Брой задачи")
    st.pyplot(fig)

    st.dataframe(df)
