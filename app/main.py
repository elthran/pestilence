from flask import render_template, session, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
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
    if not current_user.is_authenticated:
        # Use a newly created Guest account.
        user = User("Guest")
        user.save()
        user.start_session()
        login_user(user, force=True, remember=True)

    session.permanent = True
    session['username'] = current_user.username
    session['user_id'] = current_user.id

    if current_user.is_active:
        session['is_anonymous'] = False
    else:
        session['is_anonymous'] = True

    print(f"User {current_user} is currently in session {session}.")

    world = current_user.world
    if world:
        disease = world.diseases[0]
        world.pass_time()
    else:
        disease = None

    current_user.session.session_heartbeat()

    return render_template("home.html",
                           user=current_user,
                           world=world,
                           disease=disease,
                           highscores=Highscore.query.all())


@app.route('/register_account/', methods=['GET', 'POST'])
@login_required
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
@login_required
def login():
    if current_user.is_active:
        flash(f"You are currently logged in as {current_user.username}. "
              f"If you wish to log in as a different account, please log out first.")
        return redirect(url_for('root'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            # Delete current Guest account if it's useless
            guest_account = current_user if not current_user.is_active else None
            login_user(user)
            if guest_account and (guest_account.time_modified - guest_account.time_created).seconds < 60:
                pass
                # Want to delete but need to cascade delete
                # guest_account.delete()
            return redirect(url_for('root'))

    return render_template("login.html", form=form)


@app.route('/logout/')
@login_required
def logout():
    current_user.end_session()
    logout_user()
    return redirect(url_for('root'))


@app.route('/select_type/<string:type>')
@login_required
def select_type(type):
    """
    """
    disease = current_user.world.diseases[0]
    disease.assign_type(type)
    return redirect(url_for('root'))


@app.route('/upgrade_trait/<string:trait>')
@login_required
def upgrade_trait(trait):
    """
    """
    disease = current_user.world.diseases[0]
    disease.upgrade_trait(trait)
    return redirect(url_for('root'))


@app.route('/start_game/')
@login_required
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
