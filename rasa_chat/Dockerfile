FROM python:3.9 as DEV
EXPOSE 5005
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["rasa", "run", "-m", "models", "--enable-api", "--cors", "*", "--debug", "actions"]
