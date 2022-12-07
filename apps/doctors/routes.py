import os
import secrets
from flask import Blueprint, render_template, request, url_for, current_app, flash, redirect
from apps.models import Roles, DataDokter
from apps.doctors.forms import BerkasForm
from flask_login import current_user, login_required
from apps import db
import datetime

doctors = Blueprint('doctors', __name__)

def save_sip(form_sip):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_sip.filename)
    sip_fn = random_hex + f_ext
    sip_path = os.path.join(current_app.root_path, 'static/assets/files/dokter/sip', sip_fn)
        
    form_sip.save(sip_path)
    return sip_fn 

def save_ijazah(form_ijazah):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_ijazah.filename)
    ijazah_fn = random_hex + f_ext
    ijazah_path = os.path.join(current_app.root_path, 'static/assets/files/dokter/ijazah', ijazah_fn)
        
    form_ijazah.save(ijazah_path)
    return ijazah_fn 

@doctors.route("/tambah-data", methods=['POST', 'GET'])
@login_required
def tambah_data():
    role = Roles.query.filter_by(id=current_user.roles_id).first()

    data = DataDokter.query.filter_by(user_id=current_user.id).first()
    if data:
        return redirect(url_for('doctors.get_data', id=current_user.id))

    form = BerkasForm()

    if form.validate_on_submit():
        if form.file_sip.data:
            sip_file = save_sip(form.file_sip.data)
        if form.file_ijazah.data:
            ijazah_file = save_ijazah(form.file_ijazah.data)

        data = DataDokter(nama_lengkap=form.nama.data, no_hp=form.no_hp.data, owner=current_user, alamat_praktik=form.alamat_praktik.data, tempat_praktik=form.tempat_praktik.data, file_sip=sip_file, file_ijazah=ijazah_file, kota_praktik=form.kota_praktik.data, jam_mulai=form.jam_mulai.data, jam_selesai=form.jam_selesai.data, batas_sip=form.batas_sip.data, hari_praktik=request.form['hidden_days'])
        db.session.add(data)
        db.session.commit()
        flash('Your Data has been added!', 'primary')

        return redirect(url_for('doctors.get_data', id=current_user.id))

    return render_template('users/doctor/berkas.html', title='Data Pribadi', legend='Data Pribadi Dokter', form=form, data=data, roles=current_user.role.title)

@doctors.route("/data/<int:id>", methods=['GET'])
@login_required
def get_data(id):
    data = DataDokter.query.filter_by(user_id=id).first()
    form = BerkasForm()
    if request.method == 'GET':
        form.nama.data = data.nama_lengkap
        form.no_hp.data = data.no_hp
        form.alamat_praktik.data = data.alamat_praktik
        form.tempat_praktik.data = data.tempat_praktik
        form.kota_praktik.data = data.kota_praktik
        form.jam_mulai.data = data.jam_mulai
        form.jam_selesai.data = data.jam_selesai
        form.batas_sip.data = data.batas_sip
        # form['hidden_days'] = data.hari_praktik

    return render_template('users/doctor/berkas_done.html', title='Data Pribadi', legend='Data Pribadi', data=data, roles=current_user.role.title)

@doctors.route("/update-data/<int:id>", methods=['GET', 'POST'])
@login_required
def berkas_update(id):
    role = Roles.query.filter_by(id=current_user.roles_id).first()

    data = DataDokter.query.filter_by(user_id=id).first()

    form = BerkasForm()

    if request.method == 'POST':
        if form.file_sip.data:
            sip_file = save_sip(form.file_sip.data)
            data.file_sip = sip_file
        if form.file_ijazah.data:
            ijazah_file = save_ijazah(form.file_ijazah.data)
            data.file_ijazah = ijazah_file

        data.nama_lengkap = form.nama.data
        data.no_hp = form.no_hp.data
        data.alamat_praktik = form.alamat_praktik.data
        data.kota_praktik = form.kota_praktik.data
        data.tempat_praktik = form.tempat_praktik.data
        data.jam_mulai = form.jam_mulai.data or data.jam_mulai
        data.jam_selesai = form.jam_selesai.data or data.jam_selesai
        data.batas_sip = form.batas_sip.data
        data.hari_praktik = request.form['hidden_days']
        db.session.commit()
        flash('Your Data has been updated!', 'success')

        return redirect(url_for('doctors.get_data', id=current_user.id))

    elif request.method == 'GET':
        form.nama.data = data.nama_lengkap
        form.no_hp.data = data.no_hp
        form.alamat_praktik.data = data.alamat_praktik
        form.tempat_praktik.data = data.tempat_praktik
        form.kota_praktik.data = data.kota_praktik
        form.jam_mulai.data = data.jam_mulai
        form.jam_selesai.data = data.jam_selesai
        form.batas_sip.data = data.batas_sip

    return render_template('users/doctor/berkas.html', title='Data Pribadi', legend='Data Pribadi', form=form, data=data, roles=current_user.role.title)

@doctors.route("/delete-data/<int:id>", methods=['POST', 'GET'])
@login_required
def berkas_delete(id):
    data = DataDokter.query.filter_by(user_id=id).first()
    db.session.delete(data)
    db.session.commit()
    flash('Your Data has been deleted!', 'danger')

    return redirect(url_for('doctors.tambah_data'))

@doctors.route("/data-dokter", methods=['GET', 'POST'])
@login_required
def data_dokter():
    role = Roles.query.filter_by(id=current_user.roles_id).first()
    data = DataDokter.query.all()

    return render_template('users/doctor/data_dokter.html', title='Data Dokter', legend='Data Dokter', data=data, roles=current_user.role.title)

@doctors.route("/data-verifikasi/<int:id>", methods=['GET', 'POST'])
@login_required
def data_verifikasi(id):
    role = Roles.query.filter_by(id=current_user.roles_id).first()
    data = DataDokter.query.filter_by(user_id=id).first()
    data.status_data = True
    db.session.commit()
    flash('Your Data has been deleted!', 'danger')

    return redirect(url_for('doctors.data_dokter'))