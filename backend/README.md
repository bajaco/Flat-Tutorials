# Backend

The API serving as the backend was created with Flask-SQLAlchemy

## Installation and usage

1. Clone
2. While in the backend directory create a virtual envelope: `python -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a .flaskenv file:
`touch .flaskenv`
Contents should be similar to the following:

`FLASK_APP=src`
`FLASK_ENV=development`
`AUTH0_DOMAIN= YOUR_AUTH0_DOMAIN`
`ALGORITHMS = ['RS256']`
`API_AUDIENCE = YOUR_AUTH0_AUDIENCE`
`DATABASE_NAME = 'flat-tutorials'`
`TEST_DATABASE_NAME = 'flat-tutorials-test'`
`DATABASE_USER = 'postgres'`
`DATABASE_LOCATION = 'localhost:5432'`
`SECRET_KEY = YOUR_SECRET_KEY`

6. Create database. As postgres user: `createdb flat-tutorials`
7. Upgrade database: `python manage.py db upgrade`
8. Run: `python run.py`

### Testing

1. The test_template_generator.py file is not important, it was simply used to generate logical test names.
2. Create a copy of the database: `pg_dump flat-tutorials | psql flat-tutorials-test`
3. Create an auth.json file: `cp auth_example.json auth.json`
4. Use this link: (`https://agyx.auth0.com/authorize?audience=http://localhost:5000/&scope=openid profile email&response_type=token&client_id=5saEDf04PA0D0TZOG67sUCMtg5Dtpmpd&redirect_uri=http://localhost:5000/`) to get JWTs to populate auth.json.
5. Add the JWTs to auth.json
6. Add src to your python path (system-dependant)
7. Run the tests: `python src/test_app.py`
