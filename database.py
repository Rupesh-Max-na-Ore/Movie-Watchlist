import datetime
import sqlite3

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id),
    UNIQUE(user_username, movie_id)
);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"
INSERT_USER = "INSERT INTO users (username) VALUES (?);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = """SELECT movies.* FROM movies
JOIN watched ON movies.id = watched.movie_id
JOIN users ON users.username = watched.user_username
WHERE users.username = ?;"""
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (?, ?);"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?;"
SEARCH_MOVIES = "SELECT * FROM movies WHERE title LIKE ? COLLATE NOCASE;"
GET_ALL_USERS = "SELECT username FROM users;"
# For faster searching and filtering when number of movies get large
CREATE_RELEASE_INDEX = (
    "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp);"
)

# Establish connection to the SQLite database file named "data.db".
connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)
        connection.execute(CREATE_RELEASE_INDEX)


def add_user(username):
    with connection:
        connection.execute(INSERT_USER, (username,))


def add_movie(title, release_timestamp):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming=False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()


def search_movies(search_term):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH_MOVIES, (f"%{search_term}%",))
        return cursor.fetchall()


def watch_movie(username, movie_id):
    with connection:
        # Add user if not exists
        connection.execute(
            "INSERT OR IGNORE INTO users (username) VALUES (?);", (username,)
        )
        # Check if already watched
        cursor = connection.cursor()
        cursor.execute(
            "SELECT 1 FROM watched WHERE user_username = ? AND movie_id = ?;",
            (username, movie_id),
        )
        if cursor.fetchone():
            print(
                f"User '{username}' has already marked movie ID {movie_id} as watched."
            )
            return
        connection.execute(INSERT_WATCHED_MOVIE, (username, movie_id))


def get_watched_movies(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        return cursor.fetchall()


def get_all_users():
    with connection:
        cursor = connection.cursor()
        cursor.execute(GET_ALL_USERS)
        return [row[0] for row in cursor.fetchall()]
