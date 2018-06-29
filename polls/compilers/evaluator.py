from web_ilk.settings import POLLS_APP


class Evaluator(object):
    EVALUATORS_FILE = POLLS_APP + '/evaluators.list'
    _evaluators = {}

    @staticmethod
    def instance(language):
        evaluator = Evaluator._evaluators.get(language.name)
        if evaluator is None:
            try:
                m = __import__('%s.%s' % (POLLS_APP, language.evaluator), fromlist=[language.evaluator])
                evaluator_class = getattr(m, 'Evaluator')
                evaluator = evaluator_class()
                Evaluator._evaluators[language.name] = evaluator
            except Exception as e:
                print(e)
                raise Exception('Dil yorumlayıcısı yüklenemedi: %s' % language.name)
        return evaluator

    @staticmethod
    def get_chapter_evaluator(lesson, chapter):
        m = __import__('%s.inputs.lesson%s' % (POLLS_APP, lesson), fromlist=[str('chapter%s' % str(chapter))])
        return getattr(m, 'chapter%s' % str(chapter))

    @staticmethod
    def try_get_chapter_evaluator(lesson, chapter):
        try:
            evaluator = Evaluator.get_chapter_evaluator(lesson, chapter)
            return evaluator
        except Exception as e:
            print(e)
            raise Exception('Cannot locate chapter input/output: (%s, %s)' % (str(lesson), str(chapter)))

    @staticmethod
    def diff(str1, str2):
        str1 = Evaluator.remove_blanks(str1)
        str2 = Evaluator.remove_blanks(str2)
        return str1 == str2

    @staticmethod
    def remove_blanks(string):
        return string.replace(' ', '').replace('\t', '').replace('\n', '')

    @staticmethod
    def instance(lesson, chapter, language):
        if Evaluator._evaluators is None:
            Evaluator._evaluators = Evaluator._load_evaluators()
        evaluator_class = Evaluator._evaluators.get(language.lower())
        if evaluator_class is None:
            raise Exception('Cannot locate language evaluator: %s' % str(language))
        evaluator = evaluator_class(lesson, chapter)
        return evaluator

    @staticmethod
    def _load_evaluators():
        evaluators = {}
        f = None
        try:
            f = open(Evaluator.EVALUATORS_FILE)
            for line in f:
                line = line.strip()
                if len(line) > 0 and not line.startswith('#'):
                    items = [item.strip() for item in line.split(':')]
                    if len(items) == 2:
                        (language, evaluator) = items
                        try:
                            m = __import__('%s.%s' % (POLLS_APP, evaluator), fromlist=['Evaluator'])
                        except ImportError as e:
                            print(e)
                            continue
                        evaluators[language] = getattr(m, 'Evaluator')
        except Exception as e:
            print(e)
            pass
        finally:
            if f: f.close()
        return evaluators

