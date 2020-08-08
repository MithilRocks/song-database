from flask import Flask, request, render_template, make_response, redirect, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields, Schema
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, FileField, validators
from werkzeug.utils import secure_filename
import os 

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'songs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = os.path.join(basedir,'static')

db = SQLAlchemy(app)
ma = Marshmallow(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'mp3'

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
        return self.title

def all_artists():
    return Artist.query

def all_albums():
    return Album.query

class AddSongForm(FlaskForm):
    title = StringField('Song name', validators=[validators.input_required(message='Song name required')])
    artists = QuerySelectField(query_factory=all_artists, get_label='name')
    albums = QuerySelectField(query_factory=all_albums)
    file = FileField()

class SearchSongForm(FlaskForm):
    title = StringField()
    artist = StringField()
    album = StringField()

class AddArtistForm(FlaskForm):
    name = StringField('Artist', validators=[validators.input_required(message='Artist name required')])

class AddAlbumForm(FlaskForm):
    name = StringField('Album', validators=[validators.input_required(message='Album name required')])

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
    form = SearchSongForm() 
    message = ''
    if request.method == 'GET':
        songs = Song.query.all() 
        if len(songs) == 0:
            message = 'No songs available. Add songs to create playlist'
    if form.validate_on_submit():
        songs = Song.query.join(Song.artist, Song.album)\
                .filter(Song.title.contains(form.title.data)).filter(Artist.name.contains(form.artist.data))\
                .filter(Album.name.contains(form.album.data)).all()
        if len(songs) == 0:
            message = 'Your query returned 0 searches'
    return render_template('show_all.html', songs = songs_schema.dump(songs), form=form, message=message)

@app.route('/song/add',methods=['GET','POST'])
def add_song():
    form = AddSongForm()
    if form.validate_on_submit():

        if 'file' not in request.files:
            flash('No file part')
            return render_template('add_song.html',form=form)
            
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template('add_song.html',form=form)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_song = Song(
                title=form.title.data,
                artist=form.artists.data,
                album=form.albums.data,
                destination = filename
            )
            db.session.add(new_song)
            db.session.commit()
        else:
            flash('Only mp3 files allowed')
            return render_template('add_song.html',form=form)
        return redirect('/')
    return render_template('add_song.html',form=form)

@app.route('/artist/add',methods=['GET','POST'])
def add_artist():
    form = AddArtistForm()
    if form.validate_on_submit():
        new_artist = Artist(
            name=form.name.data
        )
        db.session.add(new_artist)
        db.session.commit()
        return redirect('/song/add')
    return render_template('add_artist.html',form=form)

@app.route('/album/add',methods=['GET','POST'])
def add_album():
    form = AddAlbumForm()
    if form.validate_on_submit():
        new_album = Album(
            name=form.name.data
        )
        db.session.add(new_album)
        db.session.commit()
        return redirect('/song/add')
    return render_template('add_album.html',form=form)

@app.route('/song/delete/<id>', methods=['GET','DELETE'])
def delete_song(id):
    song = Song.query.get(id)
    if not song:
        flash('Song does not exist')
        return redirect('/')
    db.session.delete(song)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], song.destination))
    db.session.commit()
    return redirect('/')

@app.route('/song/play/<id>', methods=['GET'])
def play_song(id):
    song = Song.query.get(id)
    if not song:
        flash('Song does not exist')
        return redirect('/')
    return render_template('play_music.html', song=song)

if __name__ == '__main__':
   app.run(debug=True)