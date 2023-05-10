# MovieRatingsApp

This project is a movie database application made with Python Flask, PostgreSQL and Bootstrap in addition to CSS and HTML. The app enables browsing, registration, rating, and administration of movies, with features like requesting movie additions, password changes, genre sorting, search functionality, and review management.

## Instructions

You can test the application at [Fly.io](https://movieratingsapp.fly.dev). You might have to refresh the site to get the application running. Accessing admin rights in the application happens with the user in the table above.

| Username  | Password |
| - | - |
| admin  | admin  |

To run the application locally you need to have Flask and PostgreSQL installed. Specify database URL and secret key in the [app.py](https://github.com/isakpulkki/MovieRatingsApp/blob/main/app.py). After that run the following commands.

```bash
# Create virtual environment
$ python3 -m venv venv

# Activate the virtual environment 
$ source venv/bin/activate

# Install the requirements
$ pip install -r ./requirements.txt

# Configure the database
$ psql < schema.sql

# Run the application
$ flask run
```

## Features

* Everyone can see, browse the movies and register an account
* Users can log in, rate the movies and delete their ratings
* Users can request a movie to be added to the database
* Users can change their password
* Admins can accept the requests and add movies directly themselves
* Admins can also delete movies and inappropriate ratings
* Movies can be sorted by their genre
* Movies can also be searched
* Users, movies and reviews can not be added with invalid inputs

User experience has been taken into consideration when creating the application, user receiving proper error messages. Application also has safety features, for example invalid inputs, accessing unauthorized pages and passwords are encrypted.

