SELECT movies.title FROM stars
INNER JOIN movies, people, ratings
ON stars.movie_id=movies.id
AND stars.person_id=people.id
AND ratings.movie_id=movies.id
WHERE people.name='Chadwick Boseman'
ORDER BY ratings.rating DESC
LIMIT 5;

