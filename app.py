from flask import Flask, request, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields, Schema
from flask_restful import Resource, Api
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
import os 

app = Flask(__name__)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'songs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return self.name

class Album(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return self.name

class Song(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))

    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))
    artist = db.relationship("Artist", backref="songs")

    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    album = db.relationship("Album", backref="songs")

    destination = db.Column(db.String(500))

    def __repr__(self):
        return '<Song %s>' % self.title

def all_artists():
    return Artist.query

def all_albums():
    return Album.query

class AddSongForm(FlaskForm):
    title = StringField()
    artists = QuerySelectField(query_factory=all_artists, get_label='name')
    albums = QuerySelectField(query_factory=all_albums)

class ArtistSchema(Schema):
    id = fields.fields.Int()
    name = fields.fields.String()

class AlbumSchema(Schema):
    id = fields.fields.Int()
    name = fields.fields.String()

class SongSchema(Schema):
    id = fields.fields.Int()
    title = fields.fields.String()
    artist = fields.fields.Nested(ArtistSchema)
    album = fields.fields.Nested(AlbumSchema)
    
song_schema = SongSchema()
artist_schema = ArtistSchema()
album_schema = AlbumSchema()
songs_schema = SongSchema(many=True)

class SongListResource(Resource):
    def get(self):
        songs = Song.query.all()
        return make_response(render_template('show_all.html', songs = songs_schema.dump(songs)), 200)

    def post(self):
        new_song = Song(
            title=request.form['title'],
            artist=Artist.query.filter_by(id=request.form['artist']).first(),
            album=Album.query.filter_by(id=request.form['album']).first()
        )
        db.session.add(new_song)
        db.session.commit()
        return song_schema.dump(new_song)

class SongResource(Resource):
    def get(self, song_id):
        song = Song.query.get(song_id)
        return song_schema.dump(song)

    def delete(self, song_id):
        Song.query.filter_by(id=song_id).delete()
        db.session.commit()
        return {}

    def put(self, song_id):
        song = Song.query.filter_by(id=song_id).first()
        if song is not None:
            for key, value in request.form.items():
                if key == 'title':
                    song.title = value
                elif key == 'artist':
                    song.artist = Artist.query.filter_by(id=request.form['artist']).first()
                elif key == 'album':
                    song.album = Album.query.filter_by(id=request.form['album']).first()
            db.session.commit()
        return song_schema.dump(song)

class ArtistListResource(Resource):
    def post(self):
        new_artist = Artist(
            name=request.form['name'],
        )
        db.session.add(new_artist)
        db.session.commit()
        return artist_schema.dump(new_artist)

class AlbumListResource(Resource):
    def post(self):
        new_album = Album(
            name=request.form['name'],
        )
        db.session.add(new_album)
        db.session.commit()
        return album_schema.dump(new_album)

# api.add_resource(SongListResource, '/songs')
# api.add_resource(ArtistListResource, '/artists')
# api.add_resource(AlbumListResource, '/albums')
# api.add_resource(SongResource, '/song/<string:song_id>')

@app.route('/songs',methods=['GET','POST'])
def songs():
    if request.method == 'GET':
        songs = Song.query.all() 
        return render_template('show_all.html', songs = songs_schema.dump(songs))

@app.route('/add_song',methods=['GET','POST'])
def add_song():
    form = AddSongForm()
    if form.validate_on_submit():
        return '{}'.format(form.artists.data)
    return render_template('add_song.html',form=form)

if __name__ == '__main__':
   app.run(debug=True)