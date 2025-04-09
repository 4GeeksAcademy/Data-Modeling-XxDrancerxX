import os
from flask_admin import Admin
from models import db, User, Post, Friends, Likes, Comments, Character, Planet, Favorites
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Friends, db.session))
    admin.add_view(ModelView(Likes, db.session))
    admin.add_view(ModelView(Comments, db.session))
    admin.add_view(ModelView(Character, db.session))  # Added
    admin.add_view(ModelView(Planet, db.session))  # Added
    admin.add_view(ModelView(Favorites, db.session))  # Added