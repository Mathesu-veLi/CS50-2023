SELECT people.name FROM stars INNER JOIN movies, people ON movies.id=stars.movie_id AND people.id=stars.person_id WHERE movies.title LIKE 'Toy Story%';
