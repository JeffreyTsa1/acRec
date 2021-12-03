#wsgi - web server gateway interrface
from app.engine import app as application

# app = application.run()
if __name__ == "__main__":
    application.run()