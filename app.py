"""
app.py

This is the main entry point for the Movie Watchlist application.
It provides a command-line interface for users to manage a movie watchlist,
including adding movies, viewing upcoming and all movies, marking movies as watched,
adding users, and searching for movies.

The application interacts with a separate 'database' module to perform all data operations.

Main Features:
- Add new movies with a title and release date.
- View upcoming movies (movies with a release date in the future).
- View all movies in the database.
- Mark a movie as watched by a user.
- View watched movies for a specific user.
- Add new users to the application.
- Search for movies by partial title.

The application runs in a loop, presenting a menu to the user and executing the selected action.

Note:
- Dates are handled as POSIX timestamps for storage and converted to human-readable format for display.
- User input is validated for menu selection, but not for other fields (e.g., date format).
- All database operations are delegated to the 'database' module.

"""

import datetime

import database

menu = """Please select one of the following options:
1) Add new movies.
2) View upcoming movies.
3) View all movies.
4) Watch a movie.
5) View watched movies.
6) Add user to the app.
7) Search movies.
8) Exit.
Your selection: """

WELCOME = "Welcome to the watchlist app!"

print(WELCOME)
database.create_tables()


def prompt_add_movie():
    title = input("Movie title: ")
    release_date = input("Release date (dd-mm-YYYY): ")
    # Parse the entered release date string into a datetime object using the specified format
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    # Convert the datetime object to a POSIX timestamp (float, seconds since epoch)
    timestamp = parsed_date.timestamp()

    database.add_movie(title, timestamp)


def print_movie_list(heading, movies):
    print(f"-- {heading} movies --")
    for _id, title, release_date in movies:
        movie_date = datetime.datetime.fromtimestamp(release_date)
        human_date = movie_date.strftime("%b %d, %Y")
        print(f"{_id}: {title} (on {human_date})")
    print("---- \n")


def prompt_watch_movie():
    username = input("Username: ")
    movie_id = input("Movie ID: ")
    database.watch_movie(username, movie_id)


def prompt_add_user():
    username = input("Username: ")
    database.add_user(username)


def prompt_show_watched_movies():
    username = input("Username: ")
    movies = database.get_watched_movies(username)  # False is default
    if movies:
        print_movie_list("Watched", movies)
    else:
        print(f"{username} has watched no movies yet!")


def prompt_search_movies():
    search_term = input("Enter the partial movie title: ")
    movies = database.search_movies(search_term)
    if movies:
        print_movie_list("Movies found", movies)
    else:
        print(f"No matching movies found for |{search_term}| !")


while (user_input := input(menu)) != "8":
    if user_input == "1":
        prompt_add_movie()
    elif user_input == "2":
        movies = database.get_movies(True)
        print_movie_list("Upcoming", movies)
    elif user_input == "3":
        movies = database.get_movies()  # False is default
        print_movie_list("All", movies)
    elif user_input == "4":
        prompt_watch_movie()
    elif user_input == "5":
        prompt_show_watched_movies()
    elif user_input == "6":
        prompt_add_user()
    elif user_input == "7":
        prompt_search_movies()
    else:
        print("Invalid input, please try again!")
