SELECT movies.title FROM stars
INNER JOIN movies, people
ON stars.movie_id = movies.id
AND people.id = stars.person_id
WHERE people.name = 'Bradley Cooper'
AND title IN (
    SELECT title FROM movies
    INNER JOIN stars, people
    ON stars.movie_id = movies.id
    AND people.id = stars.person_id
    WHERE people.name = 'Jennifer Lawrence'
    );
