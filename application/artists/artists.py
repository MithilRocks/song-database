from flask import Blueprint, render_template, redirect
from flask import current_app as app
from application.forms import AddArtistForm
from application.models import Artist, db

# Blueprint Configuration
artist_bp = Blueprint(
    'artist_bp', __name__,
    template_folder='templates'
)

@artist_bp.route('/artist/add',methods=['GET','POST'])
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
