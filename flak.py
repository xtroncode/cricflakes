#!usr/bin/python

from flask import Flask,jsonify,render_template,request
import urllib2
import xmltodict,json
from cricbuzz import CricbuzzParser
from werkzeug.contrib.cache import SimpleCache

app=Flask(__name__)
cache=SimpleCache()


@app.route('/_get_scores')
def get_scores():
    o=cache.get('scores')
    if o is None:
      cric = CricbuzzParser()
      match = cric.getJson()
      details = cric.handleMatches(match) #Returns Match details as a Dictionary. Parse it according to requirements.
      o={'details':details}
      cache.set('scores',o,timeout=15)
    return app.response_class(json.dumps(o,
        indent=None if request.is_xhr else 2), mimetype='application/json')

  
@app.route('/')
def index():
    return render_template('index.html')
  
if __name__=="__main__":
  app.run(host='0.0.0.0',port=8080,debug=False)