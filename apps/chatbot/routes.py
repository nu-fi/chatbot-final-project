from flask import Blueprint, render_template, url_for, flash, redirect, request
from apps.models import Message
from apps import db
from flask_login import current_user, login_required
import json
import pandas as pd
import subprocess

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

@chatbot.route("/admin/dataset")
@login_required
def dataset():
    data_file = open('apps/intents.json').read()
    intents = json.loads(data_file)
    df = pd.read_json(json.dumps(intents))
    
    return render_template('users/admin/chatbot/dataset.html', title='Dataset', data=df)

@chatbot.route("/admin/dataset-training")
@login_required
def training():
    subprocess.call("py apps/train.py", shell=True)
    
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

        return redirect(url_for('chatbot.dataset'))
    return render_template('users/admin/chatbot/tambah_dataset.html', title='Tambah Dataset')

@chatbot.route("/admin/history")
@login_required
def history():
    return render_template('users/admin/chatbot/history.html', title='History Chatbot')

@chatbot.route("/admin/chatbot")
@login_required
def unans_chat():
    messages = Message.query.all()
    return render_template('users/admin/chatbot/unanswered.html', messages=messages, title='Unanswered Chatbot')

@chatbot.route("/admin/unans-delete/<int:id>", methods=['POST'])
@login_required
def quest_delete(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    
    return redirect(url_for('chatbot.unans_chat'))