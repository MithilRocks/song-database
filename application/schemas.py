from flask_marshmallow import fields
from . import ma

class ArtistSchema(ma.Schema):
    id = fields.fields.Int()
    name = fields.fields.String()

class AlbumSchema(ma.Schema):
    id = fields.fields.Int()
    name = fields.fields.String()

class SongSchema(ma.Schema):
    id = fields.fields.Int()
    title = fields.fields.String()
    artist = fields.fields.Nested(ArtistSchema)
    album = fields.fields.Nested(AlbumSchema)
    destination = fields.fields.String()
    
song_schema = SongSchema()
artist_schema = ArtistSchema()
album_schema = AlbumSchema()
songs_schema = SongSchema(many=True)
