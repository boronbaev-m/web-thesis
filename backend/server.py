from app import create_app, db
from app.models import User, Code

app = create_app()

def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
