import os
import requests

from flask import Flask, render_template, session, request, Response

# Notice that I set a dummy static url path so that the static
# routes do not conflict with the static routes of the two apps.
app = Flask(__name__, static_url_path='/__')
app.config['SECRET_KEY'] = 'mysecretkey1211'
app.config['CAT_APP'] = 'http://localhost:5000'  # domain for cat app
app.config['DOG_APP'] = 'http://localhost:61206'  # domain for dog app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/app/<pet>')
def choose_pet(pet):
    key = '_'.join([pet.upper(), 'APP'])
    session['KEY'] = key
    req = requests.get(app.config[key])
    return req.content
    # return pet

# catch-all path so that static resources get passed on to the
# main app. Note the excluded headers are necessary so that css
# and js files are correctly decoded on arrival.
@app.route('/<path:path>')
def static_files(path):
    key = session.get('KEY')
    # print('im here')
    resp = requests.get(
        url='/'.join([app.config[key], path]),
        headers={key: value for (key, value)
                 in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']

    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers
               ]

    response = Response(resp.content, resp.status_code, headers)
    return response
