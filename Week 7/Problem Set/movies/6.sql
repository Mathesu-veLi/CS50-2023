SELECT AVG(ratings.rating) AS rating_average FROM ratings INNER JOIN movies ON ratings.movie_id=movies.id WHERE movies.year = 2012;
