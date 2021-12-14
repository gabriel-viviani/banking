# Banking Challenge

This repo contain the solution to the [proposed DOCK TECH challenge](https://github.com/cdt-baas/desafio-dev-api-rest)

##### This repo depends on the following:
 - [Poetry dependency manager](https://python-poetry.org/docs/)
 - Python 3.9 `brew install python`
 
## To Run it locally:
### Setup instructions
After getting poetry installed you should create a virtual environment and activate it
`$ python3 -m venv env`
`$ source env/bin/activate`
Then install dependencies using poetry:
`$ poetry install`

### Run instructions
To execute the solution you have to provide a valid postgres connection:
`$ DATABASE_URL="postgresql://user:password@localhost:5432/database"`
`$ uvicorn src.main:app --reload`
After that you would be able to see following output:
```sh
INFO:     Started server process [35568]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
##### A mock data was created and pre-inserted using a proper [orm mapper](https://www.sqlalchemy.org/). Needed person data pre inserted can be viewed at `http://127.0.0.1:8000/docs#/people/get_people_people__get`

`/openapi.json` especification is at `http://127.0.0.1:8000/docs`

### Running using Dockerfile:
Execute following commands:
```sh
cd ~/banking-challenge
docker build -t banking-challenge
docker run -p 80:80 -e DB_URL=postgresql://user:pw@host:5432/db banking-challenge
```
##### Now you can access [docs at](http://0.0.0.0/docs)

## Considerations:
* A basic layered design patter was used to keep dependency only for inner layer
* A much better approach would be use a complex messaging/events architecture as [described here](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/) or at [cosmic python.](https://www.cosmicpython.com/book/chapter_11_external_events.html)
* It's simple test relates a admin view where user who is getting and inserting data at resources has access to all data. Otherwise will be a huge security issue an user accessing other's data.
* I've used [simple postgres dockerfile](https://docs.docker.com/samples/postgresql_service/) to support application. You can also ask me for already provisioned db url's.


