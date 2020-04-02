import json, sys, os, time, shutil
sys.path.append(os.getcwd() + '//bin/')
sys.path.append(os.getcwd() + '//lib/')
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from collections import OrderedDict
from flowHandler import TestScn
from utils import cleanup


runObject = None
port=int(os.environ.get('PORT', 8000))
app = Flask(__name__)
cors = CORS(app)
_DATA = None
_STEPFILE = None
_MSG = '''

--------------------------------------------------------------------------------
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~USAGE DETAILS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
--------------------------------------------------------------------------------


 Run the below command to run the script from your terminal


 "python start.py <options> <optional parameters>"


 Options::

    clean <no. of days> ---> can be used to clean all the Log, Screenshot and report files 
            example : python start.py clean 7
    
    run <json filename> ---> Use to run a UI automation where the json filename 
                             contains JSON for the UI automation
                             Make sure to place the JSON file in the config folder before running 
            example : python start.py run sample.json

    server              -->  Starts an Rest API based web server that accepts requests with JSON filename 
                             The JSON file provided will be executed
                             Reqeust Body sample " {"filename" :"D:\Auto\\testcases\\first.json}
 
    help ---> Print the help doc.
 '''

def _exit(msg = ''):
    print(msg.upper())
    print(_MSG)
    exit(1)

@app.route('/api/testcase/execute',methods=['POST'])
@cross_origin()
def itAllStartsHere():
    __file = request.get_json()
    __file = __file['filename']
    _DATA = json.load(open(__file), object_pairs_hook=OrderedDict)
    for key in _DATA['steps']:
        if type(_DATA['steps'][key]) == str and _DATA['steps'][key].count('.json') == 1:
            _DATA['steps'][key] = json.load(open(os.getcwd() + '\\config\\' + _DATA['steps'][key]), object_pairs_hook=OrderedDict)
    try:
        _runObject = TestScn(_DATA)
        _runObject.runSteps()
        _runObject.postRun()
    except Exception as e:
        print(str(e))
    return jsonify({"status":"Execution Completed"})

cmd = sys.argv[1:]
if len(sys.argv) < 2 or sys.argv[-1].lower() == 'help':
    _exit('HELP DOCUMENTATION :: ')
else:
    runType = cmd[0].lower()
    if runType == 'server':
        app.run(host='0.0.0.0', port=port, debug=True)
    if runType == 'clean':
        if len(cmd) > 1 and cmd[1].isdigit():
            cleanup(int(cmd[1]))
        else:
            _exit('Invalid command ')
    if runType == 'run':
        if not len(cmd) > 1:
            _exit('No JSON file name passed as argument')
        _STEPFILE = os.getcwd() + r'/config/' + cmd[1]
        if not os.path.isfile(_STEPFILE):
            _exit('File "{0}" not found. Make sure the file is in the "config" Directory "{1}"'.format(_STEPFILE, os.getcwd() + "/config"))
        else:
            _DATA = json.load(open(_STEPFILE), object_pairs_hook=OrderedDict)
            for key in _DATA['steps']:
                if type(_DATA['steps'][key]) == str and _DATA['steps'][key].count('.json') == 1:
                    _DATA['steps'][key] = json.load(open(os.getcwd() + r'/config/' + _DATA['steps'][key]), object_pairs_hook=OrderedDict)
        try:
            runObject = TestScn(_DATA)
            runObject.runSteps()
        except Exception as e:
            print(str(e))
        finally:
            runObject.postRun()



