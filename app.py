from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from googletrans import Translator
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import user, translation
db.create_all()

from models.user import User, load_user
from models.translation import Translation
from forms import LoginForm, RegistrationForm

translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('translations'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/translations', methods=['GET', 'POST'])
@login_required
def translations():
    if request.method == 'POST':
        text = request.form.get('text')
        translated_text = translator.translate(text, src='auto', dest='en').text
        new_translation = Translation(text=text, translation=translated_text, user_id=current_user.id)
        db.session.add(new_translation)
        db.session.commit()
        flash('Translation saved!')
    translations = current_user.translations.all()
    return render_template('translations.html', translations=translations)

@app.route('/export_translations')
@login_required
def export_translations():
    translations = current_user.translations.all()
    filename = f"{current_user.username}_translations.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for t in translations:
            f.write(f"{t.text}\n{t.translation}\n\n")
    return send_file(filename, as_attachment=True)

@app.route('/translate', methods=['POST'])
@login_required
def translate():
    text = request.json['text']
    translated_text = translator.translate(text, src='auto', dest='en').text
    return jsonify(translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
