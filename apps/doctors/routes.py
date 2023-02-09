from flask import Blueprint, render_template, request, url_for, current_app, flash, redirect
from apps.models import Roles, DataDokter, TempatPraktik
from apps.doctors.forms import BerkasForm, TempatPraktikForm
from flask_login import current_user, login_required
from apps import db
import datetime

doctors = Blueprint('doctors', __name__)

@doctors.route("/tambah-data", methods=['POST', 'GET'])
@login_required
def tambah_data():
    role = Roles.query.filter_by(id=current_user.roles_id).first()
    cekdata = DataDokter.query.filter_by(user_id=current_user.id).first()
    if cekdata:
        data_valid=cekdata.status_data
    else:
        data_valid=False

    data = DataDokter.query.filter_by(user_id=current_user.id).first()
    if data:
        return redirect(url_for('doctors.get_data', id=current_user.id))

    form = BerkasForm()

    if form.validate_on_submit():
        data = DataDokter(nama_lengkap=form.nama.data, no_hp=form.no_hp.data, owner=current_user, batas_sip=form.batas_sip.data)
        db.session.add(data)
        db.session.commit()
        flash('Your Data has been added!', 'primary')

        return redirect(url_for('doctors.get_data', id=current_user.id))

    return render_template('users/doctor/berkas.html', title='Data Pribadi', legend='Data Pribadi Dokter', form=form, data=data, roles=current_user.role.title, data_valid = data_valid)


@doctors.route("/data/<int:id>", methods=['GET'])
@login_required
def get_data(id):
    data = DataDokter.query.filter_by(user_id=id).first()
    cekdata = DataDokter.query.filter_by(user_id=current_user.id).first()
    tempat_praktik = TempatPraktik.query.filter_by(user_id=current_user.id).all()

    form = BerkasForm()
    if request.method == 'GET':
        form.nama.data = data.nama_lengkap
        form.no_hp.data = data.no_hp
        form.batas_sip.data = data.batas_sip
        # form['hidden_days'] = data.hari_praktik

    return render_template('users/doctor/berkas_done.html', title='Data Pribadi', legend='Data Pribadi', data=data, roles=current_user.role.title, data_valid = cekdata.status_data, tempat_praktik=tempat_praktik)

@doctors.route("/update-data/<int:id>", methods=['GET', 'POST'])
@login_required
def berkas_update(id):
    role = Roles.query.filter_by(id=current_user.roles_id).first()
    cekdata = DataDokter.query.filter_by(user_id=current_user.id).first()

    data = DataDokter.query.filter_by(user_id=id).first()

    form = BerkasForm()
    form_tp = TempatPraktikForm()

    if request.method == 'POST':
        data.nama_lengkap = form.nama.data
        data.no_hp = form.no_hp.data
        data.batas_sip = form.batas_sip.data
        # data.alamat_praktik = tp_form.alamat_praktik.data
        # data.kota_praktik = tp_form.kota_praktik.data
        # data.tempat_praktik = tp_form.tempat_praktik.data
        # data.jam_mulai = tp_form.jam_mulai.data or data.jam_mulai
        # data.jam_selesai = tp_form.jam_selesai.data or data.jam_selesai
        
        # data.hari_praktik = request.form['hidden_days']
        db.session.commit()
        flash('Your Data has been updated!', 'success')

        return redirect(url_for('doctors.get_data', id=current_user.id))

    elif request.method == 'GET':
        form.nama.data = data.nama_lengkap
        form.no_hp.data = data.no_hp
        form.batas_sip.data = data.batas_sip

    return render_template('users/doctor/berkas.html', title='Data Pribadi', legend='Data Pribadi', form=form, data=data, roles=current_user.role.title, data_valid = cekdata.status_data, form_tp=form_tp)

@doctors.route("/delete-data/<int:id>", methods=['POST', 'GET'])
@login_required
def berkas_delete(id):
    data = DataDokter.query.filter_by(user_id=id).first()
    tp = TempatPraktik.query.filter_by(user_id=id).all()

    if tp != None:
        for t in tp:
            db.session.delete(t)
        db.session.commit()
    db.session.delete(data)
    db.session.commit()
    flash('Your Data has been deleted!', 'danger')

    return redirect(url_for('doctors.tambah_data'))


@doctors.route("/data-dokter", methods=['GET', 'POST'])
@login_required
def data_dokter():
    role = Roles.query.filter_by(id=current_user.roles_id).first()
    cekdata = DataDokter.query.filter_by(user_id=current_user.id).first()
    data = DataDokter.query.all()
    data_tp = TempatPraktik.query.all()

    return render_template('users/doctor/data_dokter.html', title='Data Dokter', legend='Data Dokter', data=data, roles=current_user.role.title, data_valid = cekdata.status_data, data_tp=data_tp)

@doctors.route("/tambah-tempat-praktik", methods=['POST', 'GET'])
@login_required
def tambah_tempatpraktik():
    role = Roles.query.filter_by(id=current_user.roles_id).first()
    cekdata = DataDokter.query.filter_by(user_id=current_user.id).first()
    if cekdata:
        data_valid=cekdata.status_data
    else:
        data_valid=False

    form = TempatPraktikForm()
    
    if form.validate_on_submit():
        tempat_praktik = form.tempat_praktik.data
        alamat_praktik = form.alamat_praktik.data
        kota_praktik = form.kota_praktik.data
        hari_praktik = request.form['hidden_days']
        jam_mulai = form.jam_mulai.data
        jam_selesai = form.jam_selesai.data
        tempat = TempatPraktik(tempat_praktik=tempat_praktik, alamat_praktik=alamat_praktik, kota_praktik=kota_praktik, hari_praktik=hari_praktik, jam_mulai=jam_mulai, jam_selesai=jam_selesai, user_id=current_user.id)
        db.session.add(tempat)
        db.session.commit()

        flash('Your Data has been added!', 'success')

        return redirect(url_for('doctors.get_data', id=current_user.id))

    return render_template('users/doctor/tempat_praktik.html', title='Tempat Praktik Dokter', legend='Tempat Praktik Dokter', form=form, roles=current_user.role.title, data_valid = data_valid)

@doctors.route("/update-tempat-praktik/<int:id>", methods=['GET', 'POST'])
@login_required
def update_tp(id):
    role = Roles.query.filter_by(id=current_user.roles_id).first()
    cekdata = DataDokter.query.filter_by(user_id=current_user.id).first()

    data = TempatPraktik.query.filter_by(id=id).first()

    # form = BerkasForm()
    form = TempatPraktikForm()

    if request.method == 'POST':
        data.alamat_praktik = form.alamat_praktik.data
        data.kota_praktik = form.kota_praktik.data
        data.tempat_praktik = form.tempat_praktik.data
        data.jam_mulai = form.jam_mulai.data or data.jam_mulai
        data.jam_selesai = form.jam_selesai.data or data.jam_selesai
        data.hari_praktik = request.form['hidden_days']
        db.session.commit()
        flash('Your Data has been updated!', 'success')

        return redirect(url_for('doctors.get_data', id=current_user.id))

    elif request.method == 'GET':
        form.alamat_praktik.data = data.alamat_praktik
        form.kota_praktik.data = data.kota_praktik 
        form.tempat_praktik.data = data.tempat_praktik
        form.jam_mulai.data = data.jam_mulai
        form.jam_selesai.data = data.jam_selesai
        # request.form['hidden_days'] = data.hari_praktik
        

    return render_template('users/doctor/update_tempat_praktik.html', title='Ubah Tempat Praktik', legend='Data Pribadi', form=form, data=data, roles=current_user.role.title, data_valid = cekdata.status_data)


@doctors.route("/delete-tempatpraktik/<int:id>", methods=['POST', 'GET'])
@login_required
def tp_delete(id):
    tp = TempatPraktik.query.filter_by(id=id).first()
    db.session.delete(tp)
    db.session.commit()
    flash('Your Data has been deleted!', 'danger')

    return redirect(url_for('doctors.tambah_data'))