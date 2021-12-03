#wsgi - web server gateway interrface
from app.engine import app

if __name__ == "__main__":
    app.run()