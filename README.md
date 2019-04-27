It's a python recommendation engine wrapped in flask, so it could be easily used as a microservice (proper Nginx-like server/containerization is needed, though).

Recommender's model is based on MovieLens data with 10,448 movies and 27,225,144 recommendations (movies with 100+ ratings).
One can get predictions based on a title or id. The first option is useful for model QA purposes
while the second could be used for production.


# How to run the server
Run these two commands:
1) `source venv/bin/activate`
2) `flask run`

The server will be up and running and available at [http://localhost:5000/](http://localhost:5000/).
One can check short API endpoints manual below 


# Endpoints
## /make_recommendations_by_id

The endpoint can serve POST and GET requests and awaits for `object_id`.
Such id-based recommendations could be used in a production environment, for making title-based
recommendations check the endpoints described below. 

The endpoint can be used as follows:
- `curl -X POST 'http://127.0.0.1:5000/make_recommendations_by_id' -H 'Content-Type: application/json' -d '{"object_id":"1"}'`
- [`http://127.0.0.1:5000/make_recommendations_by_id?object_id=1`](http://127.0.0.1:5000/make_recommendations_by_id?object_id=1)

One can find ids for each title in `datasets/movies.csv`.

## /make_recommendations_by_title

The endpoint can serve POST and GET requests. `title` argument needs to be passed with GET request or as a body of a POST request.
Title-based recommendations are great for testing the quality of model's predictions. However, when you pass a title to this endpoint, it
will search for similar titles and select the first one. So if one wants to get predictions for some particular title,
consider using `make_recommendations_by_id` endpoint.

This endpoint can be used as follows:
- `http://127.0.0.1:5000/make_recommendations_by_title?title=Big Lebo`
- [`http://127.0.0.1:5000/make_recommendations_by_title?title=Matrix`](http://127.0.0.1:5000/make_recommendations_by_title?title=Matrix)
- `curl -X POST 'http://127.0.0.1:5000/make_recommendations_by_title' -H 'Content-Type: application/json' -d '{"title":"Big Lebo"}'`
- `curl -X POST 'http://127.0.0.1:5000/make_recommendations_by_title' -H 'Content-Type: application/json' -d '{"title":"Matrix"}'`


## /recommender

Basically it's a human-friendly html version of `make_recommendations_by_title` endpoint. It is accessible at [`http://127.0.0.1:5000/recommender`](http://127.0.0.1:5000/recommender)


# Prerequisites (usage without venv)
One should install [python](https://docs.python-guide.org/starting/install3/linux/) and [pip](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/) before running the server

Altogether one should run:
1) `sudo apt-get update`
2) `sudo apt-get install python3.6`
3) `sudo apt install python3-pip`

One needs to setup a proper server instead of running flask server for production purposes.
