FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update

WORKDIR /install

COPY ./requirements.txt ./constraints.txt ./
RUN pip install -r requirements.txt -c constraints.txt
RUN pip install gunicorn

# Create directories app_home and static directories
WORKDIR /code

COPY manage.py pytest.ini makefile.py ./
COPY src src

CMD ["python3.10", "makefile.py", "--action=app"]