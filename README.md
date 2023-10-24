# qq2
Back in 2021, I made [qqueue](https://github.com/whitgroves/qqueue) based on the ["breakable toy" pattern](https://www.amazon.com/Apprenticeship-Patterns-Guidance-Aspiring-Craftsman/dp/0596518382) to practice web development. This is another take at that concept, with the goal of putting more production-level practices ... into practice.

## Quickstart
```
$ git clone https://github.com/whitgroves/qq2.git
$ cd qq2
$ echo SECRET_KEY=(generate or make one up) > .env
```
With Docker 🐋:
```
$ docker build -t qq2 .
$ docker run -p 80:80 --env-file .env qq2
```
The old-fashioned way 👴:
```
$ python3 -m venv .venv
$ source .venv/Scripts/activate
(venv) $ pip install -r requirements.txt
(venv) $ python3 -m init_db
(venv) $ flask run --port=80
```
After that navigate to [`localhost`](http://localhost/) to view the app.