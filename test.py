import requests, os

os.environ.setdefault('API_TOKEN',
                      'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNTg3YTllM2IwMWYwZmRjMzUxNWQ0NjNiYTc4OGI3NyIsInN1YiI6IjYyODc2NjE1ZjEwYTFhMzNhYjI5NTM2MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.75cuaSAiF2WkTIJUOUtneWPNjYYeMSRnnSp56889rHI')

# get a movie data from TMDB
title = "joker"
headers = {"Authorization": f'Bearer {os.environ.get("API_TOKEN")}'}
url = "https://api.themoviedb.org/3/search/movie"
params = {"query": title, }
response = requests.get(url=url, params=params, headers=headers)
print(response.json())
