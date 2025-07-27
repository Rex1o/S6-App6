FROM python:3.9

WORKDIR /app

COPY Docker_requirements.txt .

RUN pip install --upgrade pip==25.0.1
RUN pip install --no-cache-dir -r Docker_requirements.txt

COPY ./CoAP_App.py .

# Port standard pour CoAP
EXPOSE 5683/udp

CMD ["python", "CoAP_App.py"]