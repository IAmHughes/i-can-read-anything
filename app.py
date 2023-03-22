# app.py

from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import login_user, login_required, current_user
from config import Config
from forms import LoginForm, RegistrationForm, TranslateForm
from extensions import db, login_manager
from models.user import User, load_user
from models.translation import Translation
from googletrans import Translator
import csv
import io

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(email=form.email.data)  # Removed the password keyword argument
            user.set_password(form.password.data)  # Set the password using set_password method
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Login successful.', 'success')
                return redirect(url_for('translate'))
            else:
                flash('Invalid email or password.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/translate', methods=['GET', 'POST'])
    @login_required
    def translate():
        form = TranslateForm()
        if form.validate_on_submit():
            translator = Translator()
            translated = translator.translate(form.text.data, dest=form.target_language.data)
            translation = Translation(text=form.text.data, translation=translated.text, user_id=current_user.id)
            db.session.add(translation)
            db.session.commit()
            flash('Translation saved.', 'success')
            return redirect(url_for('translations'))
        return render_template('translate.html', form=form)

    @app.route('/translations', methods=['GET'])
    @login_required
    def translations():
        saved_translations = current_user.get_saved_translations()
        return render_template('translations.html', translations=saved_translations)

    @app.route('/export_translations', methods=['GET'])
    @login_required
    def export_translations():
        translations = current_user.get_saved_translations()
        csv_data = io.StringIO()
        writer = csv.writer(csv_data)
        writer.writerow(['Text', 'Translation'])
        for t in translations:
            writer.writerow([t.text, t.translation])
        csv_data.seek(0)
        return send_file(
            csv_data,
            mimetype='text/csv',
            as_attachment=True,
            attachment_filename='translations.csv'
        )

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
