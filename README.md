# New authors.

This project was created for my portfolio.

## Project setup.

1. Install packages:
    - download the source code and unzip it.
    - from the project directory go to the `/server/` folder.
    - open `cmd` from server folder.
    - write `python -m venv venv`.
    - after write `venv\Scripts\activate`.
    - run `pip install -r requirements.txt`.


2. Change db settings:
    - edit `database_settings.ini` file by entering your data:
      ```
      [DATABASE]
      NAME=
      USER=postgres
      PASSWORD=
      HOST=localhost
      PORT=5432
      ```
      
3. Make migrations:
   - open `cmd` from server folder.
   - write `venv\Scripts\activate`.
   - after write `python manage.py makemigrations`.
   - finaly write `python manage.py migrate`.

## Launch

1. open server folder in `cmd`.
2. run the command `python manage.py runserver` with activated venv.