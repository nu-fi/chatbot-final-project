from flask import Blueprint, render_template, url_for, redirect, request, send_from_directory, current_app, flash
from apps.models import Message
from apps import db
from flask_login import login_required
import json, os
import pandas as pd
from io import StringIO

chatbot = Blueprint('chatbot', __name__)

def write_json(new_data, filename='apps/intents.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["intents"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def get_dataset_by_tag(tag):
    with open('apps/intents.json') as json_file:
        data = json.load(json_file)
        for dataset in data['intents']:
            if dataset['tag'] == tag:
                return dataset
    return None

def ubah_dataset(tag, new_patterns, new_responses):
    with open('apps/intents.json', 'r') as json_file:
        data = json.load(json_file)
        for dataset in data['intents']:
            if dataset['tag'] == tag:
                dataset['patterns'] = new_patterns
                dataset['responses'] = new_responses
                break
    
    with open('apps/intents.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def delete_tag(tag):
    with open('apps/intents.json', 'r') as file:
        data = json.load(file)
    
    # Find the index of the tag to be deleted
    index = None
    for i in range(len(data['intents'])):
        if data['intents'][i]['tag'] == tag:
            index = i
            break

    # Delete the tag if found
    if index is not None:
        data['intents'].pop(index)
        
        # Write the updated data to the file
        with open('apps/intents.json', 'w') as file:
            json.dump(data, file, indent=4)
            
@chatbot.route("/admin/dataset")
@login_required
def dataset():
    data_file = open('apps/intents.json').read()
    intents = json.loads(data_file)
    intents = json.dumps(intents)
    df = pd.read_json(StringIO(intents))
    
    return render_template('users/admin/chatbot/dataset.html', title='Manajemen Dataset', data=df)

@chatbot.route("/admin/download-dataset")
def dataset_download():
    filename = "intents.json"
    path = os.path.join(current_app.root_path)
    return send_from_directory(path, filename, as_attachment=True)

@chatbot.route('/admin/upload-dataset', methods=['POST'])
def upload_dataset():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = "data.pth"
            file.save(os.path.join(current_app.root_path, filename))
            flash('New model uploaded successfully!!', 'primary')
            return redirect(url_for('chatbot.dataset'))
        else:
            flash('No file selected.', 'error')
    return redirect(url_for('chatbot.dataset'))

@chatbot.route("/admin/tambah-dataset", methods=['GET', 'POST'])
@login_required
def add_dataset():
    if request.method == 'POST':

        tag = request.form['tag']
        patterns = request.form['patterns']
        responses = request.form['responses']

        patterns = patterns.split('\n')
        responses = responses.split('\n')
        y = {
            "tag": tag,
            "patterns": patterns,
            "responses": responses
        }

        write_json(y)
        flash("Dataset berhasil ditambah", 'primary')
        return redirect(url_for('chatbot.dataset'))
    return render_template('users/admin/chatbot/tambah_dataset.html', title='Tambah Dataset')

@chatbot.route("/admin/edit-dataset/<string:tag>", methods=['GET', 'POST', 'PUT'])
@login_required
def edit_dataset(tag):
    dataset = get_dataset_by_tag(tag)

    if request.method == 'POST' or request.method == 'PUT':

        patterns = request.form['patterns']
        responses = request.form['responses']

        patterns = patterns.split('\n')
        responses = responses.split('\n')
        dataset['patterns'] = patterns
        dataset['responses'] = responses

        ubah_dataset(dataset['tag'], patterns, responses)
        flash("Dataset berhasil diubah", 'success')

        return redirect(url_for('chatbot.dataset'))

    return render_template('users/admin/chatbot/edit_dataset.html', title='Ubah Dataset', dataset=dataset)

@chatbot.route("/admin/delete-dataset/<string:tag>", methods=['GET', 'POST', 'DELETE'])
@login_required
def delete_dataset(tag):
    delete_tag(tag)
    flash("Dataset berhasil dihapus", 'danger')
    return redirect(url_for('chatbot.dataset'))

@chatbot.route("/admin/history")
@login_required
def history():
    messages = Message.query.filter_by(status_data=True).all()
    return render_template('users/admin/chatbot/history.html', messages=messages, title='History Chatbot')

@chatbot.route("/admin/unanswered")
@login_required
def unans_chat():
    messages = Message.query.filter_by(status_data=False).all()
    return render_template('users/admin/chatbot/unanswered.html', messages=messages, title='Unanswered Chatbot')

@chatbot.route("/admin/unans-delete/<int:id>", methods=['POST'])
@login_required
def unans_delete(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash("Data percakapan tidak terjawab berhasil dihapus", 'danger')
    
    return redirect(url_for('chatbot.unans_chat'))

@chatbot.route("/admin/history-delete/<int:id>", methods=['POST'])
@login_required
def history_delete(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash("Data percakapan berhasil dihapus", 'danger')
    
    return redirect(url_for('chatbot.history'))