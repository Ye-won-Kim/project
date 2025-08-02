import requests

class tmdbApi:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.themoviedb.org/3/movie/'

    def get_movie_info(self, tmdb_id):
        url = f'{self.base_url}{tmdb_id}?api_key={self.api_key}&language=en-US'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_poster_url(self, tmdb_id):
        data = self.get_movie_info(tmdb_id)
        if data and 'poster_path' in data:
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        return None