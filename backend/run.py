from src import create_app, db
from dotenv import load_dotenv
load_dotenv('.flaskenv')
app = create_app()

if __name__ == "__main__":
    app = create_app()
    app.run()

