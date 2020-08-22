FROM python:3
WORKDIR /usr/src/rest-app

COPY rest-app.py ./
COPY requirements.txt ./
COPY metrics.py ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "/usr/src/rest-app/rest-app.py"]
