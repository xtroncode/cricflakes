#!usr/bin/python

from flask import Flask,jsonify,render_template,request
import urllib2
import xmltodict,json
from cricbuzz import CricbuzzParser

app=Flask(__name__)



@app.route('/_get_scores')
def get_scores():
    #a = request.args.get('a', 0, type=int)
    #b = request.args.get('b', 0, type=int)
    cric = CricbuzzParser()
    match = cric.getXml()
    details = cric.handleMatches(match) #Returns Match details as a Dictionary. Parse it according to requirements.
    o={'details':details}
    return app.response_class(json.dumps(o,
        indent=None if request.is_xhr else 2), mimetype='application/json')

  
@app.route('/')
def index():
    return render_template('index.html')
  
if __name__=="__main__":
  app.run(host='0.0.0.0',port=8080)