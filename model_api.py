from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI() # создание приложения

with open('lgb_BEST.pkl', 'rb') as f:
    data = pickle.load(f)

model, scaler = data['model'], data['scaler'] 

request_count = 0

class PredictionInput(BaseModel):
    Age: int
    Driving_License: bool 
    Previously_Insured: bool
    Vehicle_Age: int
    Vehicle_Damage: bool
    Annual_Premium: float
    Vintage: int
    Gender_Male: bool
    Region_Code: int  # от 1 до 52 или 0 (если "другое")
    Policy_Sales_Channel: int  # от 1 до 163 или 0 (если "другое")




@app.get('/stats')
def stats():
    return {'Количество запросов': request_count}

@app.post('/predict_model') # Декоратор, который примениться прится при вызове ф-ии ниже
def predict_model(input_date: PredictionInput): # Ф-ия приема входных данных
    global request_count # Увеличиваем счетчик запросов 
    request_count += 1

    scale_array = scaler.transform(np.array([input_date.Age, input_date.Vehicle_Age,  input_date.Annual_Premium, input_date.Vintage]).reshape(1, -1)) # преобразования
    input_date.Age = scale_array[0][0]
    input_date.Annual_Premium = scale_array[0][2]
    input_date.Vintage = scale_array[0][3]

    
    features  = {
        'Age': input_date.Age,
        'Driving_License': input_date.Driving_License,
        'Previously_Insured': input_date.Previously_Insured,
        'Vehicle_Damage': input_date.Vehicle_Damage,
        'Annual_Premium': input_date.Annual_Premium,
        'Vintage': input_date.Vintage,
        'Gender_Male': input_date.Gender_Male
    } # Обработка входных данных в словарь

    
        
    excluded_columns = [
    'Policy_Sales_Channel_102.0',
    'Policy_Sales_Channel_1.0',
    'Policy_Sales_Channel_72.0',
    'Policy_Sales_Channel_112.0',
    'Policy_Sales_Channel_77.0',
    'Policy_Sales_Channel_84.0',
    'Policy_Sales_Channel_85.0',
    'Policy_Sales_Channel_141.0',
    'Policy_Sales_Channel_142.0',
    'Policy_Sales_Channel_143.0',
    'Policy_Sales_Channel_144.0',
    'Policy_Sales_Channel_149.0',
    'Policy_Sales_Channel_161.0',
    'Policy_Sales_Channel_162.0',
    'Policy_Sales_Channel_5.0',
    'Policy_Sales_Channel_6.0',
    'Region_Code_39.2']
    
    for i in range(1, 53):
        col_name = f'Region_Code_{i}.0'
        if col_name in excluded_columns:
            f = 0
        else:
            features[col_name] = input_date.Region_Code == i
    
    for i in range(1, 164):
        col_name = f'Policy_Sales_Channel_{i}.0'
        if col_name in excluded_columns:
            f = 0
        else:
            check_value = input_date.Policy_Sales_Channel == i
            features[col_name] = check_value



    prediction = model.predict([list(features.values())])
    result = 'Клиент заинтересован' if prediction[0] == 1 else 'Клиент не заинтересован'
    
    return result

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5100)
    
    
    