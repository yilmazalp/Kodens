import random
import string

max_input_size = 1000
max_output_size = 5000
max_code_size = 20000

LanguageMap = {
    'c': 'clike',
    'c++': 'clike',
    'java': 'clike',
    'c#': 'clike',
    'python': 'python',
    'javascript': 'javascript',
    'scheme': 'scheme',
    'haskell': 'haskell',
    'php': 'php',
    'html': 'html',
};

def language_codemirror(language):
    result = LanguageMap.get(language.lower())
    if result is None:
        return language
    else:
        return result

chars = string.ascii_letters + string.digits

def randomstring():
    return "".join(random.choice(chars) for x in range(random.randint(8, 16)))

def check_input(input):
    if len(input) > max_input_size:
        raise Exception("Girdi boyutu limiti aşıldı.")

def check_code(code):
    if len(code) > max_code_size:
        raise Exception("Kod limiti aşıldı.")

def crop_output(output):
    if len(output) > max_output_size:
        return output[:max_output_size]
    return output


