import os


NUMBER_OF_RECOMMENDATIONS = 10

MOVIELENS_MODEL_PATH = '/models/knn_movie_title_only_100_plus_ratings_27mln'
MOVIELENS_MOVIES_PATH = '/datasets/movies.csv'

MODEL_PATH = os.getcwd() + MOVIELENS_MODEL_PATH
MOVIES_PATH = os.getcwd() + MOVIELENS_MOVIES_PATH


# these paths are used for debugging in VSCode
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.getcwd() + '/title_flask_recommender' \
        + MOVIELENS_MODEL_PATH

if not os.path.exists(MOVIES_PATH):
    MOVIES_PATH = os.getcwd() + '/title_flask_recommender' \
        + MOVIELENS_MOVIES_PATH
