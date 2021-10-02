import os, flask
from tinydb import TinyDB, Query
from src.challenge_handler import ChallengeHandler

app = flask.Flask(__name__)

@app.route("/request", methods=['POST'])
def request():
    """
    request cookie of a IP and username
    we identify the user by the cookie
    return:
        the generated or selected cookie
    """
    req_json = flask.request.json
    ip = flask.request.remote_addr
    username = req_json.get('username')
    cookie = req_json.get('cookie')
    cha_handler = ChallengeHandler(ip, username, cookie)
    return flask.jsonify(cha_handler.info)

@app.route("/getinfo", methods=['POST'])
def getinfo():
    """
    get info based on cookie
    """
    req_json = flask.request.json
    ip = flask.request.remote_addr
    cookie = req_json.get('cookie')
    cha_no = req_json.get('cha_no')
    cha_handler = ChallengeHandler(ip, None, cookie)
    ret = cha_handler.info
    if cha_no == '1':
        pri_key = cha_handler.handle_q1()
        ret['pri'] = pri_key
    return flask.jsonify(ret)

@app.route("/submit", methods=['POST', 'GET'])
def submit():
    """
    get the user's flag
    """
    flag = flask.request.json
    ip = flask.request.remote_addr
    cha_no = flag.get('challenge_no')
    flag_res = flag.get('flag')
    username = flag.get('username')
    cookie = flag.get('cookie')

    cha_handler = ChallengeHandler(ip, username, cookie)
    print(ip, username, cookie, cha_no, flag)
    print(cha_handler.info)
    if cha_no == "1":
        if cha_handler.verify_flag(flag_res, '1'):
            add_res = cha_handler.add_to_submit(flag_res, cha_no)
            return flask.jsonify({"res": "right"})
        else:
            return flask.jsonify({"res": "wrong"})
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

app.run(host='0.0.0.0', port=9870, debug=True)
