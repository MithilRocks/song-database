from flask import Blueprint, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from flask import current_app as app
from application.forms import SearchSongForm, AddSongForm
from application.models import db, Song, Artist, Album
from application.schemas import song_schema, songs_schema
import os

# Blueprint Configuration
song_bp = Blueprint(
    'song_bp', __name__,
    template_folder='templates'
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'mp3'

@song_bp.route('/',methods=['GET','POST'])
def songs():
    form = SearchSongForm(request.form) 
    message = ''
    clear_search = False
    if request.method == 'GET':
        songs = Song.query.all() 
        if len(songs) == 0:
            message = 'No songs available. Add songs to create playlist'
        return render_template('show_all.html', songs = songs_schema.dump(songs), form=form, message=message, clear_search=clear_search)
    if form.validate_on_submit():
        clear_search = True
        songs = Song.query.join(Song.artist, Song.album)\
                .filter(Song.title.contains(form.title.data)).filter(Artist.name.contains(form.artist.data))\
                .filter(Album.name.contains(form.album.data)).all()
        if len(songs) == 0:
            message = 'Your query returned 0 searches'
        return render_template('show_all.html', songs = songs_schema.dump(songs), form=form, message=message, clear_search=clear_search)
    else:
        clear_search = True
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(str.capitalize(fieldName)+" "+err)
    return render_template('show_all.html', form=form, message=message, clear_search=clear_search)

@song_bp.route('/song/add',methods=['GET','POST'])
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

@song_bp.route('/song/delete/<id>', methods=['GET','DELETE'])
def delete_song(id):
    song = Song.query.get(id)
    if not song:
        flash('Song does not exist')
        return redirect('/')
    db.session.delete(song)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], song.destination))
    db.session.commit()
    return redirect('/')

@song_bp.route('/song/play/<id>', methods=['GET'])
def play_song(id):
    song = Song.query.get(id)
    if not song:
        flash('Song does not exist')
        return redirect('/')
    return render_template('play_music.html', song=song)
