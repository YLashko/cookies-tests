FROM python:3.12-alpine

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY . ./

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
