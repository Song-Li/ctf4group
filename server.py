import os, flask
from tinydb import TinyDB, Query

app = flask.Flask(__name__)

def insert_to_db(username, cha_no, flag, ip):
    """
    insert a tuple to db
    """
    db = TinyDB('db.json')
    db.insert({'username': username, 'cha_no': cha_no, 'flag': flag, 'IP': ip})

@app.route("/submit", methods=['POST'])
def submit():
    """
    get the user's flag
    """
    flag = flask.request.form
    ip = flask.request.remote_addr
    cha_no = flag.get('challenge_no')
    flag_res = flag.get('flag')
    insert_to_db(flag.get('username'), cha_no, flag_res, ip)
    if cha_no == "1":
        if flag_res.upper() == "7A13CD44A38A4F7A18898FF16D45A682":
            return flask.send_from_directory(os.path.join(app.static_folder, 'challenges'), 'q2.html')
        else:
            return "不太对啊，再试试？"
    if cha_no == "2":
        return flask.send_from_directory(os.path.join(app.static_folder, 'challenges'), 'q3.html')
    if cha_no == "3":
        return flask.send_from_directory(os.path.join(app.static_folder, 'challenges'), 'q4.html')
    if cha_no == "4":
        return flask.send_from_directory(os.path.join(app.static_folder, 'challenges'), 'finish.html')

@app.route('/')
@app.route('/images/<path:imgname>')
@app.route('/js/<path:jsname>')
@app.route('/pub/<path:pub>')
@app.route('/css/<path:cssname>')
@app.route('/vendor/<path:vendor>')
@app.route('/fonts/<path:fonts>')
@app.route('/challenges/<path:cha>')
def index(jsname=None, cssname=None, imgname=None, vendor=None, fonts=None, cha=None, pub=None):
    if jsname:
        return flask.send_from_directory(os.path.join(app.static_folder, 'js'), jsname)
    elif cssname:
        return flask.send_from_directory(os.path.join(app.static_folder, 'css'), cssname)
    elif pub:
        return flask.send_from_directory(os.path.join(app.static_folder, 'pub'), pub)
    elif imgname:
        return flask.send_from_directory(os.path.join(app.static_folder, 'images'), imgname)
    elif vendor:
        return flask.send_from_directory(os.path.join(app.static_folder, 'vendor'), vendor)
    elif fonts:
        return flask.send_from_directory(os.path.join(app.static_folder, 'fonts'), fonts)
    elif cha:
        return flask.send_from_directory(os.path.join(app.static_folder, 'challenges'), cha)
    else:
        return flask.send_from_directory(app.static_folder, 'index.html')

app.run(host='0.0.0.0', port=9870)
