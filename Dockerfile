# 1. Python ka light version use karenge
FROM python:3.9-slim

# 2. Container ke andar folder setup
WORKDIR /app

# 3. Zaroori system tools (psutil ke liye chahiye hote hain)
RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

# 4. Requirements copy aur install karo
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Poora app code copy karo
COPY app/ .

# 6. Port 5000 expose karo
EXPOSE 5000

# 7. App start karne ki command
CMD ["python", "app.py"]
