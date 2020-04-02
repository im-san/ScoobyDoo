# ScoobyDoo

  Wrapper module around selenium to run UI tests using JSON file.

## Pre requisites
-     Python 3+
-     Google Chrome / Mozilla Firefox
-     webdriver for the corresponding browser
-     Python modules
			selenium
			json2html

# Installation
    Below are the steps for installation of pre-requisites
 -   Python
       Download the installer and follow the instructions from the below link
       https://www.python.org/downloads/
 -   Browser
      Install any of the browser's listed above from the below download links 
        Chrome - [Download Chrome](https://www.google.com/chrome/?brand=CHBD&gclid=CjwKCAjwqZPrBRBnEiwAmNJsNuq7wJZgp3ir39s5Bkq5BdenH8xoo_6Tb75mPoB0B-etcOrPaCCPoRoC1-EQAvD_BwE&gclsrc=aw.ds)
        Firefox - [Download Firefox](https://www.mozilla.org/en-US/firefox/all/#product-desktop-release)
		
- WebDriver
    Download the driver for the installed browser from the below link
	https://www.seleniumhq.org/download/


- Python Modules
Make sure python installation is complete before running this step. You can check this by opening command prompt and running the command "python -v", ehich should show you the installed python version. Post this step, use the below commands to ijnstall the python modules through command prompt or Terminal

		```pip install selenium```

		```pip install json2html```
# Running the application
Open command prompt or terminal in the location where the project files were downloaded, make sure to make changes to the sample.json file in the config folder acrrodingly and run the below command.

	```python start.py <options> <optional parameters>```

    ```    Options::```

    ```        clean <no. of days> ---> can be used to clean all the Log, Screenshot and report files ```
    ```                example : python start.py clean 7 ```

    ```        run <json filename> ---> Use to run a UI automation where the json filename ```
    ```                                 contains JSON for the UI automation```
    ```                                 Make sure to place the JSON file in the config folder before running ```
    ```                example : python start.py run sample.json```

    ```        server ---> starts a REST API server on port 8000```
    
    ```        help ---> Print the help doc.```
    
