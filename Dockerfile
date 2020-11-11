FROM python:3.8

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./update_file /app/update_file

ENV PYTHONPATH=/app

CMD ["python", "-m", "update_file"]
