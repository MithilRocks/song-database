from . import db

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

""" def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db() """