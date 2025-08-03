from flask import Flask, request, jsonify, render_template
from recommender.movieRecommender import MovieRecommender

app = Flask(__name__)

movieRecommender = MovieRecommender('ml-latest-small/movies.csv', 'ml-latest-small/ratings.csv', 'ml-latest-small/tags.csv')

@app.route("/")
def home():
    return render_template("index.html")

# 제목으로 영화 추천
@app.route("/movieRecommend", methods=['POST'])
def movieRecommend():
    data = request.get_json()
    movieTitle = data.get('movieTitle')
    movieId = movieRecommender.get_movieId(movieTitle)
    if movieId!='':
        result = movieRecommender.get_similar_movies(movieId)
        return jsonify({'result': result})
    else:
        return jsonify({'result':''})

# 자동완성
@app.route("/movieTitle", methods=["POST"])
def movieTitle():
    query = request.get_json().get('query', '').lower()
    titles = movieRecommender.get_titles(query)
    return jsonify(titles)

if __name__ == "__main__":
    app.run(debug=True)