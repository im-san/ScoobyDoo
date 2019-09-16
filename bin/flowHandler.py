import json
import datetime
import sys
import os
sys.path.append(os.getcwd() + '//bin/')
from collections import OrderedDict
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from json2html import json2html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGFILENAME = os.getcwd() + '//log/RunLog_{0}.log'
REPORTFILENAME = os.getcwd() + '//output/REPORT_{0}.html'
CSVFILENAME = os.getcwd() + '//output/REPORT_{0}.csv'
LOGLINE = '{0} :: {1} - {2}'

class TestScn:
    def __init__(self, _data):
        if self.__validateData(_data):
            self.__preSetup()
            self.__log('Completed Pre setup Checks, Starting setup')
            self.data = _data
            self.steps = _data['steps']
            self.__config = _data['config']
            _hdls = 'Browser will be running in headless mode' if self.__config['headless'].lower() == 'true' else 'Browser will run in foreground'
            self.__log(_hdls)
            self.__setup()
            self.__log('Started browser instance')
        else:
            print('Provided JSON file is invalid !')
            exit(1)


    def __setup(self):
        _co = webdriver.ChromeOptions()
        _co.headless = True if self.__config['headless'].lower() == 'true' else False
        self.driver = webdriver.Chrome(executable_path = self.__config['driverpath'], chrome_options = _co)
        self.driver.set_page_load_timeout(self.__config['pageload'])
        self.driver.implicitly_wait(self.__config['implicitwait'])
        self.driver.set_script_timeout(self.__config['scriptTimeout'])
        self.driver.maximize_window()
        self.actions = ActionChains(self.driver)
        self.prevState = []
        self.runDetails = {k.capitalize(): self.data[k] for k in self.data}
        self.runDetails['Started'] = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
        self.runDetails['Config'] = {k.capitalize(): self.runDetails['Config'][k] for k in self.runDetails['Config'].keys() if k.lower() not in ['username', 'password']}
        self.runDetails['Steps'] = {k.capitalize(): 'Not Run' for k in self.runDetails['Steps'].keys()}


    def __validateData(self, data):
        _isValid = True
        if 'name' not in data.keys(): _isValid = False
        if 'config' not in data.keys(): _isValid = False
        if 'steps' not in data.keys(): _isValid = False
        for step in data['steps'].keys():
            for key in data['steps'][step].keys():
                if data['steps'][step][key][0].lower() not in ['wait','click', 'fill', 'login','get','getall','open','clear']:
                    _isValid = False
                    print('"' + data['steps'][step][key][0] + '" is not a valid action !')
        return _isValid


    def __log(self,  message):
        self.logFile.write(LOGLINE.format(datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"), "LOG", message + '\n'))


    def __error(self,  message):
        self.logFile.write(LOGLINE.format(datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"), "ERROR", message + '\n'))


    def __stop(self):
        self.__log('Closing the current instance of chrome')
        self.driver.quit()
        self.__log('Releasing all the resources')
        self.logFile.close()
        exit(1)


    def __preSetup(self):
        self.screensfolder = os.getcwd() + '//screens//SC' + datetime.datetime.now().strftime(r'%Y%m%d%H%M%S')
        self.logFile = open(LOGFILENAME.format(datetime.datetime.now().strftime(r'%Y%m%d_%H%M%S')), 'a')
        self.__log('Starting Pre setup Checks')
        if not os.path.isdir(os.getcwd() + '//log'):
            os.mkdir(os.getcwd() + '//log')
        if not os.path.isdir(os.getcwd() + '//screens'):
            os.mkdir(os.getcwd() + '//screens')
        if not os.path.isdir(os.getcwd() + '//output'):
            os.mkdir(os.getcwd() + '//output')
        os.mkdir(self.screensfolder)


    def __findElement(self, xpath):
        self.__log('Call to locate element with xpath '+ xpath)
        try:
            rtVal = WebDriverWait(self.driver, self.__config['elementWaitTime']).until( \
        EC.presence_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            self.__error('Failed while trying to find the element with xpath ' + xpath + ' waiting for the element')
            self.__error(str(e))
        else:
            _sc_name = self.screensfolder + r'/Screencapture_{0}.png'.format(''.join(c for c in xpath if c.isalnum()))
            self.driver.save_screenshot(_sc_name)
            self.__log('Element Located')
            sleep(2)
            return rtVal
        self.__error('Failed to locate the element with xpath ' + xpath)
        _sc_name = self.screensfolder + r'/Screencapture_{0}_failure.png'.format(''.join(c for c in xpath if c.isalnum()))
        self.driver.save_screenshot(_sc_name)
        return None


    def __findElements(self,xpath):
        try:
            rtVal = WebDriverWait(self.driver, self.__config['elementWaitTime']).until( \
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
        except Exception as e:
            self.__error('Failed while trying to find the element with xpath ' + xpath + ' waiting for the element')
            self.__error(str(e))
        else:
            sc_name = self.screensfolder + r'/Screencapture_{0}.png'.format(''.join(c for c in xpath if c.isalnum()))
            self.driver.save_screenshot(sc_name)
            return rtVal
        self.__error('Failed to locate the element with xpath ' + xpath)
        sc_name = self.screensfolder + r'/Screencapture_{0}_failure.png'.format(''.join(c for c in xpath if c.isalnum()))
        self.driver.save_screenshot(sc_name)
        return None


    def __checkVisibility(self, xpath):
        try:
            WebDriverWait(self.driver, self.__config['elementWaitTime']).until( \
        EC.visibility_of((By.XPATH, xpath)))
        except Exception as e:
                self.__error("Element with xpath '{0}' not Visible !".format(xpath))
                self.__error(str(e))


    def __saveState(self,elem):
        if len(self.prevState) < 5:
            self.prevState.append(elem)
        else:
            for i in reversed(range(1,len(self.prevState))):
                self.prevState[i] = self.prevState[i-1]
            self.prevState[0] = elem

        
    def __click(self, xpath):
        try:
            rtVal = WebDriverWait(self.driver, int(self.__config['elementWaitTime'])).until( \
        EC.element_to_be_clickable((By.XPATH, xpath)))
            rtVal.click()
        except Exception as e:
            self.__error('Element not Clickale')
            self.__error(str(e))
        

    def runSteps(self):
        for case in self.steps.keys():
            for step in self.steps[case].keys():
                inputs = self.steps[case][step]
                _elm = None
                if inputs[1].lower() == 'prev':
                    _elm = self.prevState[inputs[2]]
                if inputs[0].lower() in ['fill', 'get','clear','wait'] and inputs[1].lower() != 'prev':
                    _elm = self.__findElement(inputs[1])
                    if _elm == None:
                        self.runDetails['Steps'][case.capitalize()] = 'Failed'
                        return 1
                if inputs[0].lower() == 'getall':
                    _elm = self.__findElements(inputs[1])
                    if _elm == None:
                        self.runDetails['steps'][case.capitalize()] = 'Failed'
                        return 1
                    else:
                        self.__saveState(_elm)
                try:
                    if inputs[0].lower() == 'click': self.__click(inputs[1])
                    if inputs[0].lower() == 'clear': _elm.clear()
                    if inputs[0].lower() == 'fill': _elm.send_keys(inputs[2])
                    #if inputs[0].lower() == 'login': self.__saml_login(inputs[1])
                    if inputs[0].lower() == 'open': self.driver.get(inputs[1])
                except Exception as e:
                    self.__error('unable to perform "{0}" operation on element with path "{1}"'.format(inputs[0], inputs[1]))
                    self.__error(str(e))
                    self.runDetails['Steps'][case.capitalize()] = 'Failed'
                    return 1
                self.__saveState(_elm)
            self.runDetails['Steps'][case.capitalize()] = 'Passed'
            
            
    def postRun(self):
        self.__log('Complted execution. Preparing reports')
        self.runDetails['Ended'] = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
        with open(REPORTFILENAME.format(datetime.datetime.now().strftime(r'%Y%m%d_%H%M%S')), 'w') as f:
            f.write(json2html.convert(self.runDetails, table_attributes='border="1"'))
        self.__log('completed Reports')
        self.__stop()


if __name__ == "__main__":
    print('This is an Import module. Can not be run directly')