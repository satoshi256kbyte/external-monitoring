# 
FROM python:3.11

ENV WORKDIR /code

# 
WORKDIR ${WORKDIR}

# 
COPY Pipfile Pipfile.lock ${WORKDIR}

# 
RUN pip install pipenv --no-cache-dir
RUN pipenv install --system --deploy

# 
COPY ./app  ${WORKDIR}/app

EXPOSE 8080

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]