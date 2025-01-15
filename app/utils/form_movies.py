def form_movies_data(movies: list) -> list[dict]:
    movies_data = [
        {
            "title": movie.title,
            "url_movie": movie.url_movie,
            "description": movie.description,
            "photo": movie.photo,
            "release_year": movie.release_year,
            "director": movie.director,
            "actors": movie.actors,
            "duration": movie.duration,
            "genre_name": movie.genre_name,
        }
        for movie in movies
    ]
    return movies_data
