# Build backend stage
FROM python:3.10-slim-buster AS backend
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY models /models/
COPY logs /logs/
COPY data /data/
COPY data .
EXPOSE 5000
CMD ["python", "app.py"]

# Build frontend stage
FROM node:14 AS frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build
EXPOSE 3000

# Build final stage
FROM python:3.10-slim-buster
WORKDIR /app
COPY --from=backend /app .
COPY --from=frontend /app/build /static
EXPOSE 5000 3000
# CMD ["sh", "start.sh"]