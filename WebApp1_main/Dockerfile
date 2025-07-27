FROM python:3.9

WORKDIR /app

COPY Docker_requirements.txt .

RUN pip install --upgrade pip==25.0.1
RUN pip install -r Docker_requirements.txt

COPY . .

EXPOSE 5001

CMD ["streamlit", "run", "WebApp1.py", "--server.port=5001", "--server.address=0.0.0.0"]