import secrets
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, current_app
from apps.models import Files_Public, Message, DataDokter, Roles
from apps import db
from apps.files.forms import FilesForm
from flask_login import current_user, login_required
import os
from slugify import slugify
from apps.users.utils import admin_required

files = Blueprint('files', __name__)

def save_file(form_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    file_fn = random_hex + f_ext
    files_path = os.path.join(current_app.root_path, 'static/assets/files/public', file_fn)
        
    form_file.save(files_path)
    return file_fn

@files.route("/admin/berkas-umum", methods=['GET', 'POST'])
@login_required
def new_files():
    form = FilesForm()
    if form.validate_on_submit():
        if form.file.data:
            file_name = save_file(form.file.data)

        file = Files_Public(title=form.title.data, description=form.description.data, filename=file_name, slug = slugify(request.form.get("title")))
        db.session.add(file)
        db.session.commit()
    
    files = Files_Public.query.all()
    return render_template('users/admin/berkas_admin.html', form=form, title='Berkas Publik', files=files)

@files.route("/admin/berkas-umum/<int:file_id>/update", methods=['GET', 'POST'])
@login_required
def file_update(file_id):
    file = Files_Public.query.get_or_404(file_id)

    form = FilesForm()
    if form.validate_on_submit():
        if form.file.data:
            file_name = save_file(form.file.data)
            
        f = Files_Public(title=form.title.data, description=form.description.data, filename=file_name, slug = slugify(request.form.get("title")))
        db.session.add(f)
        db.session.commit()
        flash('Your file has been updated!', 'success')
        return redirect(url_for('files.new_files'))
    files = Files_Public.query.all()

    file = Files_Public.query.get_or_404(file_id)
    form =FilesForm()
    if request.method == 'POST':
        if form.file.data:
            file_name = save_file(form.file.data)
            file.filename = file_name
        file.title = form.title.data
        file.description = form.description.data
        db.session.commit()
        flash('Your File has been updated!', 'success')
        return redirect(url_for('files.new_files'))
    elif request.method == 'GET':
        form.name.data = file.name

    return render_template('users/admin/berkas_admin.html', form=form, title='Berkas Publik', files=files)
   
@files.route("/admin/berkas-umum/<int:file_id>/delete", methods=['POST'])
@login_required
def file_delete(file_id):
    file = Files_Public.query.get_or_404(file_id)
    # if artikel.author != current_user:
    #     abort(403)
    db.session.delete(file)
    db.session.commit()
    flash('Your File has been deleted!', 'deleted')
    return redirect(url_for('files.new_files'))


@files.route("/admin/data-dokter", methods=['GET', 'POST'])
@login_required
def data_dokter():
    # role = Roles.query.filter_by(id=current_user.roles_id).first()
    data = DataDokter.query.all()

    return render_template('users/admin/data_dokter.html', title='Data Dokter', legend='Data Dokter', data=data)

@files.route("/admin/data-verifikasi/<int:id>", methods=['GET', 'POST'])
@login_required
def data_verifikasi(id):
    role = Roles.query.filter_by(id=current_user.roles_id).first()
    data = DataDokter.query.filter_by(user_id=id).first()
    if data.status_data == False:
        data.status_data = True
    elif data.status_data == True:
        data.status_data = False
    db.session.commit()
    flash('Your Data has been updated!', 'success')

    return redirect(url_for('files.data_dokter'))

@files.route("/admin/data-detail/<int:id>", methods=['GET', 'POST'])
@login_required
def data_detail(id):
    # role = Roles.query.filter_by(id=current_user.roles_id).first()
    data = DataDokter.query.filter_by(user_id=id).first()

    return render_template('users/admin/lihat_datadokter.html', title='Verifikasi Data Dokter', legend='Verifikasi Data Dokter', data=data)