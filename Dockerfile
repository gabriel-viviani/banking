# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./src /code/src

#
ENV DATABASE_URL=$DATABASE_URL 

# 
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "log-level", "debug"]
