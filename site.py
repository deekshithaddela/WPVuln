import sys, os
from flask import (
    Flask,
    Markup,
    render_template,
    render_template_string,
    request,
    send_file )
from flask_frozen import Freezer
from werkzeug import secure_filename
from shelljob import proc
#from flask.ext.autoindex import AutoIndex

DEBUG = True

app = Flask(__name__)
freezer = Freezer(app)
app.config.from_object(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/links/')
def links():
    return render_template('links.html')

@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/url/")
def url():
    return render_template('url.html')

@app.route("/urlsfile/")
def urlsfile():
    return render_template('urlsfile.html')

@app.route('/vulnfiles/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      #import wpvuln

      import os
      i=""
      file = open(f.filename, "r")
      for line in file:
          dir=line[line.find('://www.')+7:line.find('.',line.find('://www.')+7)]
          path = os.getcwd()+"/"+dir
          for filename in os.listdir(path):
              i=i+filename+"\n"

      return i

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/404.html")
def static_404():
  return render_template('404.html')


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=True)
