from flask import Blueprint, redirect, render_template
from flask import current_app as app
from application.forms import AddAlbumForm
from application.models import Album, db

# Blueprint Configuration
album_bp = Blueprint(
    'album_bp', __name__,
    template_folder='templates'
)

@album_bp.route('/album/add',methods=['GET','POST'])
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
