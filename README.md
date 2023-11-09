# qq2
[![Test](https://github.com/whitgroves/qq2/actions/workflows/run-tests.yml/badge.svg)](https://github.com/whitgroves/qq2/actions/workflows/run-tests.yml)
[![Deploy](https://github.com/whitgroves/qq2/actions/workflows/deploy-to-ecs.yml/badge.svg)](https://github.com/whitgroves/qq2/actions/workflows/deploy-to-ecs.yml)

Back in 2021, I made [qqueue](https://github.com/whitgroves/qqueue) based on the ["breakable toy" pattern](https://www.amazon.com/Apprenticeship-Patterns-Guidance-Aspiring-Craftsman/dp/0596518382) to practice web development. This is another take at that concept, with the goal of putting more production-level practices ... into practice.

## Quickstart
Clone the repo and setup an `.env` file for the app's `SECRET_KEY`:
```
$ git clone https://github.com/whitgroves/qq2.git
$ cd qq2
$ echo SECRET_KEY=(generate or make one up) > .env
```
Then deploy with Docker 🐋:
```
$ docker compose up -d
```
Or the old-fashioned way 👴:
```
$ python3 -m venv .venv
$ source .venv/Scripts/activate
(venv) $ pip install -r requirements.txt
(venv) $ flask run --port=80
```
After that navigate to [`localhost`](http://localhost/) to view the app.