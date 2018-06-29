# from settings import POLLS_APP

class Executor(object):
    # EXECUTORS_FILE = POLLS_APP + '/executors.list'
    _executors = {}

    @staticmethod
    def instance(language):
        executor = Executor._executors.get(language)
        if executor is None:
            try:
                executor = __import__('%s' % language, fromlist=[language])
                Executor._executors[language] = executor
            except Exception as e:
                print(e)
                raise Exception('Kod çalıştırılamadı.')
        return executor

    """
    @staticmethod
    def instance(language):
        if Executor._executors is None:
            Executor._executors = Executor._load_executors()
        executor = Executor._executors.get(language.lower())
        if executor is None:
            raise Exception('Cannot locate language executor: %s' % str(language))
        return executor

    @staticmethod
    def _load_executors():
        executors = {}
        f = None
        try:
            f = open(Executor.EXECUTORS_FILE)
            for line in f:
                line = line.strip()
                if len(line) > 0 and not line.startswith('#'):
                    items = [item.strip() for item in line.split(':')]
                    if len(items) == 2:
                        (language, executor) = items
                        try:
                            m = __import__('%s' % executor, fromlist=[executor])
                        except ImportError, e:
                            print e
                            continue
                        executors[language] = m
        except Exception, e:
            print e
            pass
        finally:
            if f: f.close()
        return executors
    """

