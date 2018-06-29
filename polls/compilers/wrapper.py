import os
import shutil
import tempfile
import subprocess

from web_ilk.settings import BASE_DIR
from polls.limits import Limits

class Process(object):
    WRAPPER = 'wrapper'
    CHROOT = 'chroot'

    def __init__(self, chroot = True):
        self.cpulimit = Limits.cpulimit
        self.realtimelimit = Limits.realtimelimit
        self.memlimit = Limits.memlimit
        self.stacklimit = Limits.stacklimit
        self.filesizelimit = Limits.filesizelimit
        self.filenolimit = Limits.filenolimit
        self.stdoutlimit = Limits.stdoutlimit

        if chroot:
            self.wrapper = os.path.join(BASE_DIR, Process.CHROOT)
        else:
            self.wrapper = os.path.join(BASE_DIR, Process.WRAPPER)


    def getwrapper(self, path, exe):
        cmd = '%s -c %d -t %d -m %d -s %d -f %d -n %d -o %d -p %s %s' % \
              (self.wrapper, self.cpulimit, self.realtimelimit, self.memlimit,
                self.stacklimit, self.filesizelimit, self.filenolimit, self.stdoutlimit,
                path, exe)
        return cmd

    def execute(self, path, exe, stdin = None, stdout = None):
        cmd = self.getwrapper(path, exe)
        self.process = subprocess.Popen(cmd, shell=True, stdin=stdin, stdout=stdout, stderr=stdout)
        return self.wait()

    def wait(self):
        if self.process:
            returnValue = self.process.wait()
            return returnValue
        return -1

class JailExecutor(Process):
    def __init__(self, chroot = True):
        Process.__init__(self, chroot)

    def execute(self, exepath, stdin = None, stdout = None):
        tmpdir = None
        try:
            exename = os.path.basename(exepath)
            tmpdir = tempfile.mkdtemp()
            shutil.move(exepath, tmpdir)
            returnValue= super(JailExecutor, self).execute(tmpdir, exename, stdin, stdout)
            return returnValue
        except Exception as e:
            return -1, str(e)
        finally:
            if tmpdir:
                shutil.rmtree(tmpdir, ignore_errors=True)

class InteractiveProcess(Process):
    def __init__(self, chroot=True):
        Process.__init__(self, chroot)

    def execute(self, path, exe, input):
        cmd = self.getwrapper(path, exe)
        self.process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if self.process:
            self.process.stdin.write(input)
            output = self.process.communicate()[0]
            status = self.wait()
            return (status, output)
        else:
            return (-1, 'System Error: Cannot create child process')

class InteractiveJailExecutor(InteractiveProcess):
    def __init__(self, chroot=True):
        InteractiveProcess.__init__(self, chroot)

    def execute(self, exepath, input):
        # get a temporary jail directory and run the exe in it
        tmpdir = None
        try:
            exename = os.path.basename(exepath)
            tmpdir = tempfile.mkdtemp()
            shutil.move(exepath, tmpdir)
            result = super(InteractiveJailExecutor, self).execute(tmpdir, exename, input)
            return result
        except Exception as e:
            return -1, str(e)
        finally:
            if tmpdir: shutil.rmtree(tmpdir, ignore_errors=True)
