FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/
COPY model.pkl /app/
COPY house_price_model.pkl /app/

EXPOSE 9000

CMD ["python", "app.py"]
