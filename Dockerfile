

FROM python:3.7


COPY ./app /iWantgo/app
COPY ./static /iWantgo/static
COPY ./templates /iWantgo/templates
COPY ./requirements.txt /iWantgo

WORKDIR /iWantgo

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload"]

