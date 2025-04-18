# Divine_machines <br>
<br>

 ## Запуск
 Для запуска используйте следующие команды в терминале:
 ```
 python model_api.py
 streamlit run streamlit_for_inference_with_api.py
 ```
 
 Для создания образа(image) в Docker используйте команду:
 ```
 docker build -t divine_machines   
```

## Модель
Используется модель градиентного бустинга из библиотеки LightGBM <br>
Факторы, которые влияют на вероятность взять страховку:

1) Возраст клиента; <br>
2) Пол; <br>
3) Регион; <br>
4) Наличие водительского удостоверения; <br>
5) Размер годовой премии; <br>
6) Канал продаж; <br>
7) Было ли повреждение у автомобиля в прошлом; <br>
8) Vintage - Количество дней, в течение которых Клиент был связан с компанией. 

[**Сссылка на набор данных (Kaggle)**](https://www.kaggle.com/competitions/playground-series-s4e7/data?select=train.csv)
