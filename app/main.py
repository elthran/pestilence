from flask import render_template, session, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import redirect

from .config.initialize import initialize
from .models import User, World, City, Disease, Highscore
from .models.forms.login import LoginForm
from .models.forms.register import RegisterForm

app = initialize(__name__, models=[World, User, City])


@app.route('/')
def root():
    """
    """
    print(session)
    if not current_user.is_authenticated:
        # Use a newly created Guest account.
        user = User("Guest")
        user.save()
        user.start_session()
        login_user(user, force=True, remember=True)
        session['is_guest'] = True
    else:
        session['is_guest'] = False

    session.permanent = True
    session['username'] = current_user.username
    session['user_id'] = current_user.id

    print(session)
    print(current_user)

    world = current_user.world
    if world:
        disease = world.diseases[0]
        world.pass_time()
    else:
        disease = None

    return render_template("home.html",
                           user=current_user,
                           world=world,
                           disease=disease,
                           highscores=Highscore.query.all())


@app.route('/register_account/', methods=['GET', 'POST'])
def register_account():
    """
    """
    if current_user.is_active:
        return redirect(url_for('root'))

    form = RegisterForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.set_password_hash(form.password.data)
        current_user.is_active = True
        return redirect(url_for('root'))

    return render_template("register.html", form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_active:
        return redirect(url_for('root'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('root'))

    return render_template("login.html", form=form)


@app.route('/logout/')
def logout():
    current_user.end_session()
    logout_user()
    return redirect(url_for('root'))


@app.route('/select_type/<string:type>')
def select_type(type):
    """
    """
    disease = current_user.world.diseases[0]
    disease.assign_type(type)
    return redirect(url_for('root'))


@app.route('/upgrade_trait/<string:trait>')
def upgrade_trait(trait):
    """
    """
    disease = current_user.world.diseases[0]
    disease.upgrade_trait(trait)
    return redirect(url_for('root'))


@app.route('/start_game/')
def start_game():
    """
    """
    user = current_user
    if current_user.is_authenticated is False:
        print(session)
        return redirect(url_for('root'))
    world = World.query.filter(User.id == user.id).filter(World.active == True).first()
    if world:
        # This user already has an active game
        return redirect(url_for('root'))
    world = World("Simple Earth", user.id)
    world.save()
    for name in ["Taipei", "Vancouver"]:
        city = City(name, world.id)
        city.save()
    disease = Disease("Poop-panda Disease", world.id)
    disease.save()
    return redirect(url_for('root'))
