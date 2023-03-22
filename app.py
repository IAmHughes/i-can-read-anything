from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from forms import RegistrationForm, LoginForm, ProfileForm
from models import db
from models.user import UserLanguage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

from models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        login_user(user)
        return redirect(url_for('profile'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # Update email and password
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)

        # Update bio
        current_user.bio = form.bio.data

        # Update languages and proficiencies
        if form.language.data and form.proficiency.data:
            language_id = int(form.language.data)
            language = languages[language_id]
            proficiency = form.proficiency.data
            user_language = UserLanguage.query.filter_by(user_id=current_user.id, language=language).first()

            if user_language:
                user_language.proficiency = proficiency
            else:
                new_user_language = UserLanguage(user_id=current_user.id, language=language, proficiency=proficiency)
                db.session.add(new_user_language)

        db.session.commit()
        flash('Profile updated successfully.', 'success')

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.bio.data = current_user.bio

    return render_template('profile.html', title='Profile', form=form)

# Add other routes and functions here

if __name__ == '__main__':
    app.run(debug=True)
