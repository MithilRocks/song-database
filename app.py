from application import create_app
from application.models import Artist, Album, Song

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Artist=Artist, Album=Album, Song=Song)

if __name__ == '__main__':
   app.run(debug=True)