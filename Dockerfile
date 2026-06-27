FROM python:3.14-slim
WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x server.sh
RUN chmod +x faststream.sh
ENTRYPOINT ["/app/server.sh"]