import streamlit as st
import requests


 
def predict_model(data):
    url = 'http://127.0.0.1:5100/predict_model' # Ссылка на пост-запрос к API модельки
    
    dct_data = {
        'Age': data[0],
        'Driving_License': data[1],
        'Previously_Insured': data[2],
        'Vehicle_Age': data[3],
        'Vehicle_Damage': data[4],
        'Annual_Premium': data[5],
        'Vintage': data[6],
        'Gender_Male': data[7],
        'Region_Code': data[8],
        'Policy_Sales_Channel': data[9]
    }
 
    response = requests.post(url, json=dct_data) # Делаем пост-запрос в формате json по ссылке
    
    if response.status_code == 200: # Если всее отработало ништяк
        return response.json()
    else:
        return {'error': f'Запрос провалился. Код ошибки: {response.status_code}'}, 
        
st.title("Предсказание по автострахованию")

# Ввод данных пользователем
age = st.number_input("Возраст", min_value=1, max_value=200)
driving_license = st.checkbox("Наличие водительского удостоверения")
previously_insured = st.checkbox("Была ли ранее страховка")
vehicle_age = st.number_input("Возраст автомобиля (в годах)", min_value=0, value=0)
vehicle_damage = st.checkbox("Было ли повреждение транспортного средства")
annual_premium = st.number_input("Годовая премия", min_value=0.0, value=0.0)
vintage = st.number_input("Vintage", value=0, min_value=0)
gender_male = st.radio("Пол", ["Мужчина", "Женщина"]) == "Мужчина"


region_code_selection = st.selectbox("Код региона", options=[f"{i}" for i in range(1, 53)] + ["Другое"])
region_code = int(region_code_selection) if region_code_selection != "Другое" else 0


# Policy Sales Channel
channel_selection = st.selectbox("Канал продаж полиса", options=[f"{i}" for i in range(1, 164)] + ["Другое"])
policy_sales_channel = int(channel_selection) if channel_selection != "Другое" else 0


# Кнопка для запуска предсказания
if st.button("Предсказать"):


    # Сбор признаков в нужном порядке
    input_data = [
        int(age),
        bool(driving_license),
        bool(previously_insured),
        int(vehicle_age),
        bool(vehicle_damage),
        float(annual_premium),
        int(vintage),
        bool(gender_male),
        int(region_code),
        int(policy_sales_channel)
    ]

    
    prediction = predict_model(input_data)

    

    st.write(prediction)