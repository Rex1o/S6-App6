FROM python:3.9

WORKDIR /app

COPY Docker_requirements.txt .
RUN pip install --upgrade pip==25.0.1
RUN pip install -r Docker_requirements.txt

COPY . .

# Pour débuguer et afficher les logs (print, etc.)
ENV PYTHONUNBUFFERED=1

EXPOSE 5004

# Mode debug temporaire pour voir les erreurs
CMD ["python", "-u", "MQTT_App.py"]
# CMD ["tail", "-f", "/dev/null"]        # Pour débuger