import streamlit as st
import pickle
import numpy as np

@st.cache_resource
def load_model():
    with open('baseline.pkl', 'rb') as f:
        data = pickle.load(f)
    return data['model'], data['scaler']

model, scaler = load_model()
 
st.title("Предсказание по автострахованию")

# Ввод данных пользователем
age = st.number_input("Возраст", min_value=18, max_value=100, value=30)
driving_license = st.checkbox("Наличие водительского удостоверения")
previously_insured = st.checkbox("Была ли ранее страховка")
vehicle_damage = st.checkbox("Было ли повреждение транспортного средства")
annual_premium = st.number_input("Годовая премия", value=0.0)
vintage = st.number_input("Vintage", value=0.0)
gender_male = st.radio("Пол", ["Мужчина", "Женщина"]) == "Мужчина"

# Кнопка для запуска предсказания
if st.button("Предсказать"):
    # Преобразование возраста
    scale_array = scaler.transform(np.array([age, annual_premium, vintage]).reshape(1, -1))
    norm_age = scale_array[0][0]
    norm_premium = scale_array[0][1]
    norm_vintage = scale_array[0][2]

    

    # Сбор признаков в нужном порядке
    input_data = np.array([[
        norm_age,
        driving_license,
        previously_insured,
        vehicle_damage,
        norm_premium,
        norm_vintage,
        gender_male
    ]])

    prediction = model.predict(input_data)[0]

    st.success(f"Результат предсказания (Сосал?): {'ДА' if prediction == 1 else 'НЕТ'}")