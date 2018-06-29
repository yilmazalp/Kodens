import os
import tempfile
from io import StringIO
import subprocess

from polls.compilers.wrapper import InteractiveJailExecutor

def execute(code, input, compile_cmd, suffix, chroot = True):
    try:
        exe = compileCode(code, compile_cmd, suffix)
        exeCommand = InteractiveJailExecutor(chroot)
        return exeCommand.execute(exe, input)
    except Exception as e:
        return -1, str(e)


def compileCode(code, compile_cmd, suffix):
    codeFileName = None
    codeFile = None
    try:
        fileNo, codeFileName = tempfile.mkstemp(suffix=suffix, dir='C:/Users/User/Desktop')
        codeFile = open(codeFileName, 'w')
        codeFile.write(code)
        codeFile.flush()
        fileNo, exeFile = tempfile.mkstemp()
        removeFile(exeFile)
        cmd = compile_cmd % (codeFileName, exeFile)

        (status, output) = subprocess.getstatusoutput(cmd)
        output = output.replace(codeFileName, 'code%s' % suffix)
        if status == 0:
            return exeFile
        else:
            raise Exception(output)
    finally:
        if codeFileName:
            removeFile(codeFileName)
        if codeFile:
            try:
                codeFile.close()
            except:
                pass


def removeFile(filename):
    try:
        os.remove(filename)
    except:
        pass
