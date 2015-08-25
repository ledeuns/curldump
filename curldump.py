from flask import Flask, request, send_file, Response, render_template, make_response
import datetime
import hashlib
import os
import json
import uuid
import magic
import sqlite3
import random
import string

BASE_PATH="/var/www/curldu.mp/files/"
BASE_URL="http://curldu.mp/"
SHORTLEN=10

application = Flask(__name__)
application.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 # Maximum filesize is 1MB

@application.route("/", methods=['GET'])
def curldump():
    r = make_response(render_template("index.md"))
    r.headers["Content-Type"] = "text/plain"
    return r

@application.route("/", methods=['POST'])
def postfile():
    rv = []
    for file in request.files.itervalues():
        h = savefile(file.filename, file.stream)
        rv.append(BASE_URL+h+"\n")

    return Response("".join(rv), mimetype="text/uri-list")

@application.route("/s/<fileid>", methods=['GET'])
def getshort(fileid):
    if (len(fileid) == SHORTLEN) and (fileid.isalnum() == True):
        c = sqlite3.connect("short.db")
        cur = c.cursor()
        cur.execute("SELECT h FROM short WHERE s='%s'" % fileid)
        for row in cur:
            return getfile(row[0])
    return Response("File not found.\n", mimetype="text/plain", status=404)

@application.route("/<fileid>", methods=['GET'])
def getfile(fileid):
    attach = False
    if (request.args.has_key("attach")):
        attach = True
    
    try:
        with open(BASE_PATH+fileid+"/metadata") as mf:    
            metadata = json.load(mf)
            if len(metadata):
                return send_file(BASE_PATH+fileid+"/content", attachment_filename=metadata["filename"], as_attachment=attach, mimetype=metadata["mime"])
    except:
        return Response("File not found.\n", mimetype="text/plain", status=404)

@application.route("/<filename>", methods=['PUT'])
def putfile(filename):
    h = savefile(filename, request.stream)
    return Response(BASE_URL+h+"\n", mimetype="text/uri-list")

@application.route("/", methods=['PUT'])
def putstream():
    filename = str(uuid.uuid4())
    h = savefile(filename, request.stream)
    return Response(BASE_URL+h+"\n", mimetype="text/uri-list")

def savefile(filename, s):
    now = datetime.datetime.now().isoformat()
    h = hashlib.sha1(""+now+filename).hexdigest()
    os.mkdir(os.path.dirname(BASE_PATH+h+"/")) 

    with open(BASE_PATH+h+"/content", "w") as of:
        of.write(s.read())

    mt = magic.from_file(BASE_PATH+h+"/content", mime=True)
    metadata = {"filename": filename, "datetime": now, "mime": mt}
    with open(BASE_PATH+h+"/metadata", "w") as of:
        json.dump(metadata, of, indent=2)

    if (request.headers.get("X-SHORT")):
        return shortened(h)

    return h

def shortened(h):
    s = "".join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(SHORTLEN))
    c = sqlite3.connect("short.db")
    c.execute("INSERT INTO short(s, h, dt) VALUES(?, ?, ?)", (s, h, datetime.datetime.now()))
    c.commit()
    c.close()
    return "s/"+s

if __name__ == "__main__":
    try:
        os.stat(os.path.dirname(BASE_PATH))
    except:
        os.mkdir(os.path.dirname(BASE_PATH))
    application.run(host='::1')
