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

## Launch

1. from the project directory go to the `/server/` folder.
2. open server folder in `cmd`.
3. run the command `python manage.py runserver`.