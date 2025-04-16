FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \ 
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 8501
EXPOSE 5100

CMD ["bash", "-c", "python model_api.py & sleep 3 && streamlit run streamlit_inference_with_api.py --server.address=0.0.0.0"]