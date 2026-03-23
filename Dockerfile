FROM node:18-bullseye

RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PORT=8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]