from fabric.api import local

def clean_compiled():
    """Removed the compiled Python files"""
    local(r'rm -f `find . -name \*.pyc`')
    local(r'rm -f `find . -name \*.pyo`')

def clean_temp():
    """Clean up the temporary files"""
    local(r'rm -f `find . -name \*~`')

def clean():
    clean_compiled()
    clean_temp()
