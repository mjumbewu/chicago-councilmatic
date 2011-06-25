from fabric.api import local

def clean_compiled():
    local(r'rm -f `find . -name \*.pyc`')
    local(r'rm -f `find . -name \*.pyo`')

def clean_temp():
    local(r'rm -f `find . -name \*~`')

def clean():
    clean_compiled()
    clean_temp()
