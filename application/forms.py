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
    title = StringField('Song name', validators=[validators.DataRequired(message='Song name required'), validators.Regexp('^[a-zA-Z0-9 \']*$', message="Must contain only letters numbers or underscore")])
    artists = QuerySelectField(query_factory=all_artists, get_label='name')
    albums = QuerySelectField(query_factory=all_albums, get_label='name')
    file = FileField('MP3 file', validators=[FileRequired()])

class SearchSongForm(FlaskForm):
    title = StringField('Title', [validators.Regexp('^[a-zA-Z0-9 \']*$', message="Must contain only letters numbers or underscore"), validators.Optional()])
    artist = StringField('Artist', [validators.Regexp('^[a-zA-Z0-9 \']*$', message="Must contain only letters numbers or underscore"), validators.Optional()])
    album = StringField('Album', [validators.Regexp('^[a-zA-Z0-9 \']*$', message="Must contain only letters numbers or underscore"), validators.Optional()])

class AddArtistForm(FlaskForm):
    name = StringField('Artist', validators=[validators.DataRequired(message='Artist name required'), validators.Regexp('^[a-zA-Z0-9 \']*$', message="Must contain only letters numbers or underscore")])

class AddAlbumForm(FlaskForm):
    name = StringField('Album', validators=[validators.DataRequired(message='Album name required'), validators.Regexp('^[a-zA-Z0-9 \']*$', message="Must contain only letters numbers or underscore")])