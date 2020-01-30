from sqlalchemy.exc import DatabaseError


def add_auto_commit(app, db):
    @app.after_request
    def session_commit(response):
        if response.status_code >= 400:
            # I'm not sure if this is correct?
            # Maybe should redirect to 404?
            return response
        try:
            db.session.commit()
        except DatabaseError:
            db.session.rollback()
            raise
        # db.session.remove() # is called for you by flask-sqlalchemy
        return response
