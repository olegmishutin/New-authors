# New authors.

This project was created for my portfolio.

## Project setup.

1. Install packages:
    - download the source code and unzip it.
    - from the project directory go to the `/server/` folder.
    - open `cmd` from server folder.
    - run `pip install -r requirements.txt`.


2. Change db settings:
    - from the project directory go to the `/server/New_authors/` folder.
    - open `settings.py` file.
    - enter your data into this code and save the file:
      ```
      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.postgresql',
              'NAME': 'your_database_name',
              'USER': 'your_database_user',
              'PASSWORD': 'your_database_password',
              'HOST': 'localhost',
              'PORT': 'your_postgres_port',
          }
      }
      ```

## Launch

1. from the project directory go to the `/server/` folder.
2. open server folder in `cmd`.
3. run the command `python manage.py runserver`.