import logging
from polls import common
from polls.models import practice_question
from polls.models import practice_question_input
from polls.compilers.executor import Executor
from polls.messages import Messages
import multiprocessing
import sys
from io import StringIO
import contextlib
#from polls.pythonsandbox import PythonSandbox
from polls.compilers import compile_c

logger = logging.getLogger(__name__)
from polls.compilers import executeCompiled

COMPILE_CMD = 'gcc -x c %s -o %s -Wall -static'


class CodeExecutor(object):
    def __init__(self, language, code, input):
        if language is None or code is None:
            raise Exception(Messages.MISSING_INPUT)
        common.check_code(code)
        common.check_input(input)

        self.code = code
        self.input = input
        self.language = language


        #try:
        #    language = int(language)
        #except Exception:
        #    raise Exception('%s dil kodu geçersiz. Dil kodunun tamsayı olması gerekir' % str(language))
        #languageobj = practice_question.objects.filter(question_language_field=language)

    '''
    def execute(self):
        executor = Executor.instance(self.language)
        (status, output) = executor.execute(self.code, self.input)
        return status, common.crop_output(output)
    '''

    def pythonExecute(self, python_code, input, output):
        self.python_code = python_code
        codeFile = open('static/temp_files/temp.py', 'r+')
        codeFile.truncate()
        codeFile.write(python_code)


        self.input = input
        inputFile = open('static/data_files/input.txt', 'w+')
        inputFile.truncate()

        for line in input:
            if line!="\n":
                inputFile.write(line)

        inputFile.write('\n')

        self.output = output
        outputFile = open('static/data_files/answer.txt', 'w+')
        outputFile.truncate()

        for line in output:
            if line != "\n":
                outputFile.write(line)

        outputFile.write('\n')


    def cExecute(self, c_code, input, output):
        self.c_code = c_code
        codeFile = open('static/temp_files/temp.c', 'r+')
        codeFile.truncate()
        codeFile.write(c_code)

        self.input = input
        inputFile = open('static/data_files/input.txt', 'w+')
        inputFile.truncate()

        for line in input:
            if line != "\n":
                inputFile.write(line)

        inputFile.write('\n')

        self.output = output
        outputFile = open('static/data_files/answer.txt', 'w+')
        outputFile.truncate()

        for line in output:
            if line != "\n":
                outputFile.write(line)

        outputFile.write('\n')


    def JavaExecute(self, java_code, input, output):
        self.java_code = java_code
        codeFile = open('static/temp_files/JavaTest/Temp.java', 'r+')
        codeFile.truncate()
        codeFile.write(java_code)

        self.input = input
        inputFile = open('static/data_files/input.txt', 'w+')
        inputFile.truncate()

        for line in input:
            if line != "\n":
                inputFile.write(line)

        inputFile.write('\n')

        self.output = output
        outputFile = open('static/data_files/answer.txt', 'w+')
        outputFile.truncate()

        for line in output:
            if line != "\n":
                outputFile.write(line)

        outputFile.write('\n')

    def c_sharpExecute(self, c_sharp_code, input):
        self.c_sharp_code = c_sharp_code
        codeFile = open('C:/Users/User/Desktop/temp.cs', 'r+')
        codeFile.truncate()
        codeFile.write(c_sharp_code)

        self.input = input
        inputFile = open('C:/Users/User/Desktop/input.txt', 'w+')
        inputFile.truncate()

        for line in input:
            if line != "\n":
                inputFile.write(line)

        inputFile.write('\n')


    def phpExecute(self, php_code, input, output):
        self.php_code = php_code
        codeFile = open('static/temp_files/temp.php', 'r+')
        codeFile.truncate()
        codeFile.write(php_code)

        self.input = input
        inputFile = open('static/data_files/input.txt', 'w+')
        inputFile.truncate()

        for line in input:
            if line != "\n":
                inputFile.write(line)

        inputFile.write('\n')














