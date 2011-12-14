from functools import wraps
import os, json
from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort, send_from_directory, request, Response

from flaskext.openid import OpenID

app = Flask(__name__)

oid = OpenID(app)

@app.before_request
def before_request():
    if 'openid' in session:
        pass

def check_auth():
    if 'DOMAIN' in os.environ:
        if 'openid' in session:
            return True
        return False
    else:
        return True

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not check_auth():
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if 'DOMAIN' in os.environ:
        return oid.try_login("https://www.google.com/accounts/o8/site-xrds?hd=%s" % os.environ['DOMAIN'])
    else:
        return oid.try_login("https://www.google.com/accounts/id")
        

@oid.after_login
def create_or_login(resp):
    session['openid'] = resp.identity_url
    return redirect(oid.get_next_url())

@app.route('/logout')
def logout():
    session.pop('openid', None)
    return redirect(oid.get_next_url())

@app.route('/')
@requires_auth
def index():
    return render_template("index.html")
    
@app.route('/<path:filename>')
@requires_auth
def stuff(filename):
    """This does some special handling for restful paths. It allows you 
    to visit directly HTML pages, or visit the filenames as a path and
    successfully view them. Any route that does not contain .html or is
    not a directory is served as a file.
    """
    if filename.endswith("/"):
        return render_template(filename + "index.html")        
    if filename.find(".") == -1:
        return render_template(filename + ".html")
    elif filename.find(".html") != -1:
        return render_template(filename)
    return send_from_directory('templates', filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
