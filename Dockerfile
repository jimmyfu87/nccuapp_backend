

FROM python:3.7


COPY ./app /fastapi_project/app
COPY ./requirements.txt /fastapi_project

WORKDIR /fastapi_project

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload"]

