import os, errno
from web_ilk.settings import USERFILES_ROOT

def _get_userdir(username):
    userdir = os.path.join(USERFILES_ROOT, username)
    try:
        os.makedirs(userdir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('Cannot save %s\'s file to: %s' % (username, userdir))
            return None
    return userdir

def _get_filename(username, language):
    filename = '%s.%s.src' % (username, str(language))
    return filename

def save(username, language, code):
    userdir = _get_userdir(username)
    if not userdir:
        return
    filename = _get_filename(username, language)
    filepath = os.path.join(userdir, filename)
    try:
        with open(filepath, 'w') as f:
            f.write(code)
    except:
        pass

def load(username, language):
    userdir = _get_userdir(username)
    if not userdir:
        return ''
    filename = _get_filename(username, language)
    filepath = os.path.join(userdir, filename)
    code = ''
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except:
        pass
    return code