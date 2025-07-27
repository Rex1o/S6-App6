FROM python:3.9

WORKDIR /app

COPY Docker_requirements.txt .
RUN pip install --upgrade pip==25.0.1
RUN pip install -r Docker_requirements.txt

# install ping
RUN apt-get update && apt-get install -y iputils-ping
RUN apt-get install -y net-tools

COPY . .

# Pour débuguer et afficher les logs (print, etc.)
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "-u", "main.py"]
# CMD ["tail", "-f", "/dev/null"]        # Pour débuger