import json
import sys
import os
sys.path.append(os.getcwd() + '//bin/')
from collections import OrderedDict
from flowHandler import TestScn


runObject = None
_DATA = None
_STEPFILE = None
_MSG = '''No JSON file is passed as a parameter while running the script

 ----------------Example--------------------

 Run the below command to run the script from your terminal

 "python start.py <json_file_name>"

 Make sure to place the JSON file in the config folder before running 
 
 You can continue to run the script with a test file this would run the script with 
 "sample.json" JSON file present in config folder
 
 Do you want to continue running the test run (Y) ::'''

if len(sys.argv) < 2:
    isTest = input(_MSG)
    if (isTest.lower() == 'y' ):
        _STEPFILE = os.getcwd() + r'/config/sample.json'
    else:    
        exit(1)
else:
    _STEPFILE = os.getcwd() + r'/config/' + sys.argv[1]

if not os.path.isfile(_STEPFILE):
    print('File "{0}" not found. Make sure the file is in the "config" Directory "{1}"'.format(_STEPFILE, os.getcwd() + "/config"))
    exit(1)
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