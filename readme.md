Steps for fresh install on new PC:
1. $ `bin/install`
2. Set app.config['SQLALCHEMY_DATABASE_URI'] to use correct password
3. $ `source bin/activate`
4. $ `bin/flask build`
4. $ `bin/flask run`


Questions:
1. Why `app = Flask(name.split('.')[0], static_url_path='/', static_folder='dist')`
 