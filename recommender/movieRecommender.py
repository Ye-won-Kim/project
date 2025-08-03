import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self, movies_path, ratings_path, tags_path, links_path):
        self.movies = pd.read_csv(movies_path)
        self.ratings = pd.read_csv(ratings_path)
        self.tags = pd.read_csv(tags_path)
        self.links = pd.read_csv(links_path)
        self.movie_stats = None
        self.rating_matrix = None
        self.movie_similarity = None
        self._prepare_data()
    def _prepare_data(self):
        # 영화제목(연도) 분리
        self.movies[['title', 'year']] = self.movies['title'].str.extract(r'^(.*)\s\((\d{4})\)$')

        # 유저-영화 평점 매트릭스
        self.rating_matrix = self.ratings.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)

        # 영화 간 유사도 계산
        self.movie_similarity = cosine_similarity(self.rating_matrix.T)
        
        # 영화별 평균 평점과 평점 수 집계
        self.movie_stats = self.ratings.groupby('movieId')['rating'].agg(['mean', 'count']).reset_index()
        self.movie_stats.columns = ['movieId', 'average_rating', 'rating_count']

    def get_movieId(self, title):
        if len(self.movies[self.movies.title==title]) > 0:
            movieId = self.movies[self.movies.title==title].movieId.values[0]
            return movieId
        else:
            return ''
    
    def get_titles(self, query):
        matched = self.movies[self.movies['title'].str.lower().str.contains(query, na=False)]
        return sorted(matched['title'].head(10).tolist())
    
    def get_similar_movies(self, target_movieId, n=10):
        similar_scores = list(enumerate(self.movie_similarity[target_movieId-1], start=1))
        sorted_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True) 
        # lambda x: x[1]는 각 튜플의 두 번째 요소(유사도 값)를 기준으로 정렬
        top_similar_movies = sorted_scores[1:n+1]

        rank = 1
        result = []
        for movieId, sim in top_similar_movies:
            # 해당 movieId가 movies에 존재하지 않는 경우는 skip
            if self.movies[self.movies.movieId == movieId].empty:
                continue
            movie = self.movies[self.movies.movieId ==(movieId)]
            rating = self.movie_stats[self.movie_stats.movieId ==(movieId)].average_rating.values[0]
            count = self.movie_stats[self.movie_stats.movieId ==(movieId)].rating_count.values[0]
            tag = self.get_tags(movieId)
            tmdbId = self.get_tmdbId(movieId)
            result.append({
                'Rank': int(rank),
                'Title': movie.title.values[0],
                'Year' : movie.year.values[0],
                'Genres': movie.genres.values[0],
                'Similarity': float(round(sim,2)),
                'Average Rating': float(rating),
                'Rating Count': int(count),
                'Tag' : tag,
                'TmdbId' : int(tmdbId)
            })
            rank = rank+1
        return result
    
    def get_tags(self, movieId):
        tag = []
        if self.tags[self.tags.movieId ==(movieId)].tag.size > 0:
            tag = self.tags[self.tags.movieId ==(movieId)].tag.value_counts().index.tolist()
        return tag
    
    def get_tmdbId(self, movieId):
        return self.links[self.links.movieId == (movieId)].tmdbId.values[0]