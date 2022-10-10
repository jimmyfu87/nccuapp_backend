

FROM python:3.7.4-slim-stretch


COPY ./app /iWantgo/app
COPY ./config_docker.py /iWantgo/app/env/config.py
COPY ./static /iWantgo/static
COPY ./templates /iWantgo/templates
COPY ./requirements.txt /iWantgo
COPY ./main.py /iWantgo

WORKDIR /iWantgo

RUN pip install -r requirements.txt

EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload"]
CMD ["python", "main.py"]

