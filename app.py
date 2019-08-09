import os
import urllib

from flask import (Flask, render_template, session,
                   redirect, request, send_from_directory)


app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'mysecretkey1211'
app.config['CAT_APP'] = os.path.join(app.static_folder, 'cat', 'build')
app.config['DOG_APP'] = os.path.join(app.static_folder, 'dog', 'build')


@app.route('/<filename>')
@app.route('/')
def index(filename=' '):
    if any([ext in filename for ext in ['json', 'jpeg']]):
        key = session.get('KEY')
        try:
            return send_from_directory(app.config[key], filename, as_attachment=False)
        except:
            return '', 404
    return render_template('index.html')


@app.route('/app/<pet>')
def choose_pet(pet):
    key = '_'.join([pet.upper(), 'APP'])
    session['KEY'] = key
    return send_from_directory(app.config[key], 'index.html', as_attachment=False)
    # return pet


@app.route('/static/<path:filename>')
def static_files(filename):
    selected_key = session.get('KEY')
    # print('im here')
    filename_parts = filename.split('/')
    stem = filename_parts[-1]
    app_static_dir = os.path.join(
        app.config[selected_key], 'static', *filename_parts[:-1])
    # print(app_static_dir)
    return send_from_directory(app_static_dir, stem, as_attachment=False)
