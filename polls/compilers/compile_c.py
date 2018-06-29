from polls.compilers import executeCompiled

COMPILE_CMD = 'gcc -x c %s -o %s -Wall -static'

def execute(code, input = ''):
    return executeCompiled.execute(code, input, COMPILE_CMD, '.c')




