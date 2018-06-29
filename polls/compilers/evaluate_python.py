import os
import logging
import multiprocessing
from polls.compilers import evaluator
from polls.pythonsandbox import PythonSandbox

class Evaluator(evaluator.Evaluator):
    def evaluate(self, code, lesson, chapter):
        parent_conn, child_conn = multiprocessing.Pipe()
        p = None
        try:
            p = EvaluatorProcess(lesson, chapter, code, child_conn)
        except Exception as e:
            return [('FAILED', str(e))]
        p.start()
        p.join()
        if p.exitcode == 255:  # sys.exit(-1)
            return [('FAILED', 'Execution error')]
        if os.WIFSIGNALED(p.exitcode):
            parent_conn.close()
            if p.exitcode == -9:
                return [('FAILED', 'Time Limit exceeded')]
            else:
                return [('FAILED', 'Memory limit exceeded')]
        result = parent_conn.recv()
        parent_conn.close()
        return result


class EvaluatorProcess(multiprocessing.Process):
    def __init__(self, lesson, chapter, code, conn):
        multiprocessing.Process.__init__(self)
        try:
            self.evaluator = Evaluator.get_chapter_evaluator(lesson, chapter)
        except Exception as e:
            print(e)
            raise Exception('Cannot locate chapter evaluator: (%s, %s)' % (str(lesson), str(chapter)))
        self.code = code
        self.conn = conn

    def run(self):
        result = EvaluatorProcess.evaluate(self.evaluator, self.code)
        self.conn.send(result)
        self.conn.close()
        return result

    @staticmethod
    def evaluate(evaluator, code):
        evaluation = []
        try:
            sandbox = PythonSandbox(code)
        except Exception as e:
            return [('FAILED', str(e))]
        for testcase in evaluator.testcases():
            environment = {}
            try:
                (status, output) = sandbox.execute(testcase[0], environment, subprocess=False)
                if status == 0:
                    evaluation.extend(evaluator.evaluate(environment, testcase, output))
                else:
                    return [('FAILED', output)]
            except Exception as e:
                evaluation.append(('FAILED', str(e)))
        return evaluation
