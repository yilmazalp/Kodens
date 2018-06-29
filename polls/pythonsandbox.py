import os
import sys
import types
import psutil
from polls.limits import Limits
from psutil import Process
import io
from io import StringIO
from polls import policy
import builtins
import multiprocessing



class PythonSandbox(object):
    def __init__(self, code):
        # check if the code can be compiled (throws an exception)
        compile(code, '<string>', 'exec')
        self.code = code

    def execute(self, input, environment, subprocess=True):
        if subprocess:
            return self.execute_in_subprocess(input, environment)
        else:
            return self.execute_here(input, environment)

    def execute_here(self, input, environment):
        p = PythonSandboxProcess()
        p.set_code(self.code, input, environment, None)
        result = p.run()
        return result

    def execute_in_subprocess(self, input, environment):
        parent_conn, child_conn = multiprocessing.Pipe()
        p = PythonSandboxProcess()
        p.set_code(self.code, input, environment, child_conn)
        p.start()
        p.join()
        if p.exitcode == 255:  # sys.exit(-1)
            return (-1, 'Yorumlama hatası')
        if os.WIFSIGNALED(p.exitcode):
            parent_conn.close()
            if p.exitcode == -9:
                return (-1, 'Kod zaman aşımına uğradı')
            else:
                return (-1, 'Limit aşıldı')
        data = parent_conn.recv()
        parent_conn.close()
        result = data.get('result', (-1, 'Yorumlama hatası'))
        return result


class PythonSandboxProcess(multiprocessing.Process):
    ALLOWED_MODULES = []
    FORBIDDEN_BUILTINS = []
    __BUILTINS__ = {}
    __IMPORT__ = None

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.compile = True
        self.input = ''
        self.environment = {}
        self.conn = None

    def set_code(self, code, input, environment, conn):
        self.compile = True
        self.code = code
        self.input = input
        self.environment = environment
        self.conn = conn

    def set_function(self, function, args):
        self.compile = False
        self.function = function
        self.input = ''
        self.args = args
        self.conn = None

    def run(self):
        Limits.set_limits()
        stdio = None
        result = None
        try:
            if self.compile:
                self.code = compile(self.code, '<string>', 'exec')
            PythonSandboxProcess.load_policy()
            PythonSandboxProcess.restrict_import()
            PythonSandboxProcess.restrict_builtins()
            stdio = PythonSandboxProcess.replace_stdio(self.input)
            if self.compile:
                exec(self.code in self.environment)
                result = (0, stdio[1].getvalue())
            else:
                result = (0, self.function(*self.args))
        except MemoryError as e:
            result = (-1, e.message if e.message else 'Bellek limiti aşıldı')
        except Exception as e:
            result = (-1, str(e))
        finally:
            PythonSandboxProcess.restore_builtins()
            PythonSandboxProcess.restore_import()
            PythonSandboxProcess.restore_stdio(stdio)
            self._send_result(result)
            return result

    def _send_result(self, result):
        if not self.conn:
            return
        try:
            self.conn.send({'result': result})
            self.conn.close()
        except Exception as e:
            sys.exit(-1)

    @staticmethod
    def __my_import__(modulename, globs=globals(), locs=locals(), fromlist=[], level=-1):
        if modulename in PythonSandboxProcess.ALLOWED_MODULES:
            return PythonSandboxProcess.__IMPORT__(modulename, globs, locs, fromlist, level)
        raise ImportError('%s modülü bulunamadı.' % modulename)

    @staticmethod
    def load_policy():
        allowed = policy.POLICY.get('allowed')
        if allowed:
            PythonSandboxProcess.ALLOWED_MODULES = allowed.get('modules', [])
        forbidden = policy.POLICY.get('forbidden')
        if forbidden:
            PythonSandboxProcess.FORBIDDEN_BUILTINS = forbidden.get('builtins', [])

    @staticmethod
    def restrict_builtins():
        for builtin in PythonSandboxProcess.FORBIDDEN_BUILTINS:
            PythonSandboxProcess.__BUILTINS__[builtin] = getattr(builtins, builtin)
            setattr(builtins, builtin, None)

    @staticmethod
    def restore_builtins():
        for name, func in PythonSandboxProcess.__BUILTINS__.iteritems():
            setattr(builtins, name, func)

    @staticmethod
    def restrict_import():
        PythonSandboxProcess.__IMPORT__ = builtins.__import__
        builtins.__import__ = PythonSandboxProcess.__my_import__

    @staticmethod
    def restore_import():
        builtins.__import__ = PythonSandboxProcess.__IMPORT__

    @staticmethod
    def replace_stdio(input):
        #stdin = StringIO.StringIO(input)
        #stdout = StringIO.StringIO()
        stdin = io.StringIO(input)
        stdout = io.StringIO()
        sys.stdin = stdin
        sys.stdout = stdout
        sys.stderr = stdout
        return stdin, stdout
        #return (stdin, stdout)

    @staticmethod
    def restore_stdio(stdio):
        if stdio:
            stdio[0].close()
            stdio[1].close()
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__






