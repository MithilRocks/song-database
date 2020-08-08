from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    # Initialize Plugins
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        # create database
        db.create_all()

        # Include our Routes
        from .songs import songs
        from .artists import artists
        from .albums import albums
        
        # Register Blueprints
        app.register_blueprint(songs.song_bp)
        app.register_blueprint(artists.artist_bp)
        app.register_blueprint(albums.album_bp)

        return app