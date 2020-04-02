import time, sys, os, shutil

def cleanup(days):
    print('Deleting Log and screen files older than {0} days !'.format(str(days)))
    _delta = time.time() - (days * 86400)
    for file in os.listdir(os.getcwd() + '//log/'):
        file = os.path.join(os.getcwd() + '//log/', file)
        if os.stat(file).st_mtime < _delta:
            os.remove(file)
    for file in os.listdir(os.getcwd() + '//output/'):
        file = os.path.join(os.getcwd() + '//output/', file)
        if os.stat(file).st_mtime < _delta:
            os.remove(file)
    for file in os.listdir(os.getcwd() + '//screens/'):
        file = os.path.join(os.getcwd() + '//screens/', file)
        if os.stat(file).st_mtime < _delta:
            shutil.rmtree(file)


