from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from application.models import Artist, Album
from wtforms import StringField, FileField, validators

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'mp3'

def all_artists():
    return Artist.query

def all_albums():
    return Album.query

class AddSongForm(FlaskForm):
    title = StringField('Song name', validators=[validators.input_required(message='Song name required')])
    artists = QuerySelectField(query_factory=all_artists, get_label='name')
    albums = QuerySelectField(query_factory=all_albums, get_label='name')
    file = FileField('MP3 file', validators=[FileRequired()])

class SearchSongForm(FlaskForm):
    title = StringField()
    artist = StringField()
    album = StringField()

class AddArtistForm(FlaskForm):
    name = StringField('Artist', validators=[validators.input_required(message='Artist name required')])

class AddAlbumForm(FlaskForm):
    name = StringField('Album', validators=[validators.input_required(message='Album name required')])