#!/bin/bash

# Запускаем API в фоне
python3 model_api.py &

# Ждём немного, если нужно (по желанию)
sleep 2

# Запускаем Streamlit-приложение
streamlit run streamlit_inference_with_api.py