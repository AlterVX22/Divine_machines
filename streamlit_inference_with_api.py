import streamlit as st
import requests
import numpy as np

# @st.cache_resource
# def load_model():
#     with open('baseline.pkl', 'rb') as f:
#         data = pickle.load(f)
#     return data['model'], data['scaler']

# model, scaler = load_model()
 
def predict_model(data):
    url = 'http://127.0.0.1:5100/predict_model' # Ссылка на пост-запрос к API модельки
    
    dct_data = {'Age': data[0],
        'Driving_License': data[1],
        'Previously_Insured': data[2],
        'Vehicle_Damage': data[3],
        'Annual_Premium': data[4],
        'Vintage': data[5],
        'Gender_Male': data[6]
    }
    
    response = requests.post(url, json=dct_data) # Делаем пост-запрос в формате json по ссылке
    
    if response.status_code == 200: # Если всее отработало ништяк
        return response.json()
    else:
        return {'error': f'Запрос провалился. Вот код ошибки: {response.status_code}'}
 
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
    # scale_array = scaler.transform(np.array([age, annual_premium, vintage]).reshape(1, -1))
    # norm_age = scale_array[0][0]
    # norm_premium = scale_array[0][1]
    # norm_vintage = scale_array[0][2]

    

    # Сбор признаков в нужном порядке
    input_data = [
        age,
        driving_license,
        previously_insured,
        vehicle_damage,
        annual_premium,
        vintage,
        gender_male
    ]

    # prediction = model.predict(input_data)[0]
    prediction = predict_model(input_data)

    # st.success(f"Результат предсказания (Сосал?): {'ДА' if prediction == 1 else 'НЕТ'}")
    st.write(prediction)