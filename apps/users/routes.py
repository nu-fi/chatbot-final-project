from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from apps.models import User, Roles, Article, News, DataDokter, User
from apps.users.utils import save_picture, send_reset_email
from apps.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from apps import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)

@users.route("/admin")
@login_required
def admin():
    role = Roles.query.filter_by(id=current_user.roles_id).first()
    num_article = Article.query.all()
    num_datadok = DataDokter.query.all()
    num_news = News.query.all()
    num_dok = User.query.filter_by(roles_id=2).all()
    return render_template('users/admin/admin_dash.html', current_user=current_user, roles=current_user.role.title, num_article=len(num_article), num_datadok=len(num_datadok), num_news=len(num_news), num_dok=len(num_dok), title='Dashboard Admin')

@users.route("/dokter")
@login_required
def dokter():
    role = Roles.query.filter_by(id=current_user.roles_id).first()
    return render_template('users/doctor/dokter_dash.html', current_user=current_user, roles=current_user.role.title, title='Dashboard Dokter')

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.admin'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in ', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.roles_id == 1:
            return redirect(next_page) if next_page else redirect(url_for('users.admin'))
        else:
            return redirect(next_page) if next_page else redirect(url_for('users.dokter'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if current_user.roles_id == 1:
                return redirect(next_page) if next_page else redirect(url_for('users.admin'))
            else:
                return redirect(next_page) if next_page else redirect(url_for('users.dokter'))

        else:
            flash('Login Unsuccessful. Please check email and password again', 'deleted')

    return render_template('users/login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/akun", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='assets/img/profile_pics/' + current_user.image_file)
    return render_template('users/account.html', title='Akun', image_file=image_file, form=form)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent  with instruction to reset your password', 'info')
        return redirect(url_for('users.login'))

    return render_template('users/reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is invalid or expired token', 'deleted')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html', title='Reset Password', form=form)