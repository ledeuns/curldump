from flask import Flask, request, send_file, Response
import datetime
import hashlib
import os
import json
import uuid
import magic

BASE_PATH="/var/www/curldu.mp/files/"
BASE_URL="http://curldu.mp/"

application = Flask(__name__)
application.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 # Maximum filesize is 1MB

@application.route("/", methods=['GET'])
def curldump():
    return Response("curl -T myfile curldu.mp", mimetype="text/plain")

@application.route("/", methods=['POST'])
def postfile():
    rv = []
    for file in request.files.itervalues():
        h = savefile(file.filename, file.stream)
        rv.append(BASE_URL+h+"\n")

    return Response("".join(rv), mimetype="text/uri-list")

@application.route("/<fileid>", methods=['GET'])
def getfile(fileid):
    try:
        with open(BASE_PATH+fileid+"/metadata") as mf:    
            metadata = json.load(mf)
            if len(metadata):
                return send_file(BASE_PATH+fileid+"/content", attachment_filename=metadata["filename"], as_attachment=True, mimetype=metadata["mime"])
    except:
        return Response(fileid+" not found.\n", mimetype="text/uri-list")

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

    return h


if __name__ == "__main__":
    try:
        os.stat(os.path.dirname(BASE_PATH))
    except:
        os.mkdir(os.path.dirname(BASE_PATH))
    application.run(host='::1')
