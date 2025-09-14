from app.models import db
from app import create_app

app = create_app('DevelopmentConfig')

# Create tables
with app.app_context():
    db.create_all()
    # db.drop_all()

app.run()