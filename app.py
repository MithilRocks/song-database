from flask import Flask, request, render_template, make_response, redirect, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields, Schema
from flask_restful import Resource, Api
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, FileField, validators
from werkzeug.utils import secure_filename
import os 

app = Flask(__name__)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'songs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = os.path.join(basedir,'songs')

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
    title = StringField('Song name')
    artists = QuerySelectField(query_factory=all_artists, get_label='name')
    albums = QuerySelectField(query_factory=all_albums)
    file = FileField()

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
    destination = fields.fields.String()
    
song_schema = SongSchema()
artist_schema = ArtistSchema()
album_schema = AlbumSchema()
songs_schema = SongSchema(many=True)

@app.route('/',methods=['GET','POST'])
def songs():
    if request.method == 'GET':
        songs = Song.query.all() 
        return render_template('show_all.html', songs = songs_schema.dump(songs))

@app.route('/song/add',methods=['GET','POST'])
def add_song():
    form = AddSongForm()
    if form.validate_on_submit():

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        new_song = Song(
            title=form.title.data,
            artist=form.artists.data,
            album=form.albums.data,
            destination = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        )
        db.session.add(new_song)
        db.session.commit()
        return redirect('/')
    return render_template('add_song.html',form=form)

@app.route('/song/delete/<id>', methods=['GET','DELETE'])
def delete_song(id):
    song = Song.query.get(id)
    if not song:
        flash('Song does not exist')
        return redirect('/')
    db.session.delete(song)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
   app.run(debug=True)