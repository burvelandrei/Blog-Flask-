from flask import Flask, render_template, request, redirect, url_for
from db.db_connect import get_session
from db.models import Publication, Comment, create_tables
from sqlalchemy.exc import NoResultFound

app = Flask(__name__)


def validate_string(value):
    return isinstance(value, str) and len(value) > 0


PUBLICTION_REQUIRED_FIELDS = {
    "title": validate_string,
    "text_publication": validate_string
}

LEXICON_RU = {
    "title": "Наименование публикации",
    "text_publication": "Текст публикации"
}


@app.route("/")
def index():
  with get_session() as session:
    publications = session.query(Publication).all()

    return render_template(
        "index.html",
        publications=publications,
    )

@app.route('/publication/<int:publication_id>/')
def publication(publication_id):
    with get_session() as session:
        try:
            publication = session.query(Publication).filter_by(id=publication_id).one()
        except NoResultFound:
            return render_template('404.html'), 404

        comments = session.query(Comment).filter_by(text_publication_id=publication_id)

        return render_template(
           'publication.html',
            publication=publication,
            comments=comments,
        )

@app.route('/publication/add', methods=['GET', 'POST'])
def add_publication():
    if request.method == 'GET':
        return render_template('add_publication.html', publication={})
    elif request.method == 'POST':
        if not request.form or not all(
            key in request.form for key in PUBLICTION_REQUIRED_FIELDS
        ):
            return {'error': 'All required fields are required'}, 400

        if set(PUBLICTION_REQUIRED_FIELDS) - set(request.form):
            return render_template(
                'add_publication.html',
                error='Something is wrong!',
                publication=request.form,
            )

        for key in PUBLICTION_REQUIRED_FIELDS:
            if not PUBLICTION_REQUIRED_FIELDS[key](request.form[key]):
                return render_template(
                    'add_publication.html',
                    error=f'{LEXICON_RU[key]} не заполнен!!!',
                    publication=request.form,
                )

        with get_session() as session:
            publication = Publication(**request.form)
            session.add(publication)
            session.commit()
            return redirect(
                url_for('publication', publication_id=publication.id)
            )


@app.route('/publication/<int:publication_id>/comments', methods=['POST'])
def add_comment(publication_id):
    if not request.form or 'content' not in request.form:
        return {'error': 'Content is required'}, 400

    with get_session() as session:
        comment = Comment(
            text_publication_id=publication_id,
            text_comment=request.form['content'],
        )
        session.add(comment)
        session.commit()

    return redirect(url_for('publication', publication_id=publication_id))



@app.route('/publication/<int:publication_id>/delete', methods=['POST'])
def delete_publication(publication_id):
    with get_session() as session:
        publication_to_delete = session.query(Publication).filter_by(id=publication_id).one()
        session.delete(publication_to_delete)
        session.commit()

    return redirect(url_for('index'))


@app.route('/publication/<int:publication_id>/change', methods=['GET', 'POST'])
def change_publication(publication_id):
    if request.method == 'GET':
      with get_session() as session:
        publication = session.query(Publication).filter_by(id=publication_id).one()
        return render_template('change_publication.html', publication=publication)
    elif request.method == 'POST':
        with get_session() as session:
          session.query(Publication).filter_by(id=publication_id).update(request.form)
          session.commit()
          return redirect(
              url_for('publication', publication_id=publication_id)
          )

if __name__ == "__main__":
    app.run(debug=True)
