import flask
import pandas as pd
from flask import jsonify, render_template, request
from surprise import dump

import settings

app = flask.Flask(__name__)


def load_model(path=None):
    '''Wrapper with logging. Initializes the main machine
    learning model.
    '''
    app.logger.debug('Loading model...')

    if path is None:
        path = settings.MODEL_PATH

    _, model = dump.load(path)
    app.logger.debug('Model has been loaded successfully')
    return model


def load_movies(path=None):
    '''Wrapper with logging. Initializes movies dataframe.
    '''
    app.logger.debug('Loading movies dataframe...')

    if path is None:
        path = settings.MOVIES_PATH

    movies = pd.read_csv(path)
    app.logger.debug('Movies dataframe has been loaded successfully')
    return movies


def preprocess_request():
    '''Preprocesses incoming requests and returns a set of predictions.
    Can work with raw GET/POST requests and forms.
    '''
    app.logger.debug('Preprocessing payload...')

    # get request parameters from get/post requests or a form
    params = flask.request.json
    if not params:
        params = flask.request.args

    if not params:
        params = flask.request.form

    # if parameters are found, save title and number parameters
    title = params.get('title') or params.get

    # if we're missing one of the parameters we can't make predictions
    if not title:
        return {}

    title_found, list_of_recommendations = make_recommendations(
        title=title, num_rec=int(settings.NUMBER_OF_RECOMMENDATIONS)
    )

    response = {
        'query': title,
        'number_of_recommendations': settings.NUMBER_OF_RECOMMENDATIONS,
        'title:': title_found,
        'recommendations:': list_of_recommendations,
    }

    app.logger.debug('Preprocessing complete')
    return response


def make_recommendations_by_id(_id, num_rec=10):
    '''Makes recommendation for a particular id.
    Returns a list of recommended ids.
    '''
    try:
        inner_id = model.trainset.to_inner_iid(_id)
    except ValueError:
        try:
            inner_id = model.trainset.to_inner_iid(int(_id))
        except ValueError:
            return []

    neighbors = model.get_neighbors(inner_id, k=num_rec)

    # Convert inner ids of the neighbors into names.
    return [
        model.trainset.to_raw_iid(inner_id)
        for inner_id in neighbors
    ]


def get_id_by_title(name):
    try:
        return movies.loc[
            movies['title'].str.contains(name), 'movieId'
        ].iloc[0]
    except IndexError:
        return None


def get_title_by_id(_id):
    try:
        return movies.loc[movies['movieId'] == _id, 'title'].iloc[0]
    except IndexError:
        return None


def make_recommendations(title=None, _id=None, num_rec=10):
    '''Makes recommendation for a particular title.
    Returns the title found and a list of recommended titles.
    '''
    if not title and not _id:
        app.logger.debug(
            "I can make recommendations by _id or title."
            "For example: make_recommendations(\'Batman\')"
            "or make_recommendations(_id=12))"
        )
        return

    if title:
        # Retrieve inner id of the movie
        try:
            raw_id = get_id_by_title(title)
        except IndexError:
            app.logger.error(
                'Error: there is no "{}" title in the dataset'.format(title)
            )
            return
    else:
        raw_id = _id

    # get inner id of the title
    # inner id is a feature of Surprise library
    inner_id = model.trainset.to_inner_iid(raw_id)
    # get neighbors for the id from the model
    neighbors = model.get_neighbors(inner_id, k=num_rec)
    # convert inner ids of the neighbors into names
    neighbors = (
        model.trainset.to_raw_iid(inner_id)
        for inner_id in neighbors
    )
    return get_title_by_id(raw_id), [
        get_title_by_id(rid) for rid in neighbors
    ]


@app.route("/make_recommendations_by_id", methods=['POST', 'GET'])
def predict_by_id():
    # get request parameters from get/post requests or a form
    params = flask.request.json
    if not params:
        params = flask.request.args

    if not params:
        params = flask.request.form

    # if parameters are found, save title and number parameters
    object_id = params.get('object_id') or params.get

    # if we're missing one of the parameters we can't make predictions
    if not object_id:
        return {}

    ids = make_recommendations_by_id(object_id)
    return jsonify({
        'ids': ids,
        'titles': [get_title_by_id(_id) for _id in ids]
    })


@app.route("/make_recommendations_by_title", methods=['POST', 'GET'])
def make_recommendations_by_title():
    return jsonify(preprocess_request())


@app.route('/recommender')
def load_recommender():
    return render_template('recommender.html')


@app.route('/results', methods=['POST'])
def get_html_result():
    if request.method == 'POST':
        try:
            return render_template(
                "results.html",
                results=preprocess_request()
            )
        except (ValueError, TypeError):
            return render_template(
                'excluded_title.html',
                query=flask.request.form.get('title')
            )


# load model and movies database
model = load_model()
movies = load_movies()


# start the flask app, allow remote connections
if __name__ == '__main__':
    app.logger.debug('*** Starting web service...')
    app.run(
        debug=True,
        host='0.0.0.0:5000'
    )
