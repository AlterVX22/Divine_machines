import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI() # создание приложения

with open('baseline.pkl', 'rb') as f:
    data = pickle.load(f)

model, scaler = data['model'], data['scaler'] 

request_count = 0

class PredictionInput(BaseModel):
    Age: int
    Driving_License: bool 
    Previously_Insured: bool
    Vehicle_Damage: bool
    Annual_Premium: float
    Vintage: float
    Gender_Male: bool

@app.get('/stats')
def stats():
    return {'Количество запросов': request_count}

@app.post('/predict_model') # Декоратор, который примениться прится при вызове ф-ии ниже
def predict_model(input_date: PredictionInput): # Ф-ия приема входных данных
    global request_count # Увеличиваем счетчик запросов 
    request_count += 1
    
    scale_array = scaler.transform(np.array([input_date.Age, input_date.Annual_Premium, input_date.Vintage]).reshape(1, -1)) # Выполняю преобразования
    input_date.Age = scale_array[0][0]
    input_date.Annual_Premium = scale_array[0][1]
    input_date.Vintage = scale_array[0][2]
    
    new_data = {
        'Age': input_date.Age,
        'Driving_License': input_date.Driving_License,
        'Previously_Insured': input_date.Previously_Insured,
        'Vehicle_Damage': input_date.Vehicle_Damage,
        'Annual_Premium': input_date.Annual_Premium,
        'Vintage': input_date.Vintage,
        'Gender_Male': input_date.Gender_Male
    } # Обработка входных данных в словарь
    
    prediction = model.predict([list(new_data.values())])
    result = 'Клиент заинтересован' if prediction[0] == 1 else 'Клиент не заинтересован'
    
    return result

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5100)
    
    
    