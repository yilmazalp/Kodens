import logging
from polls import common
from polls.compilers.evaluator import Evaluator
from polls.messages import Messages
from polls.models import practice_question

logger = logging.getLogger(__name__)

class CodeEvaluator(object):
    def __init__(self, lesson, chapter, code):
        if lesson is None or chapter is None or code is None:
            raise Exception(Messages.MISSING_INPUT)
        common.check_code(code)
        self.code = code
        try:
            lesson = int(lesson)
        except Exception:
            raise Exception('Lesson number invalid: %s. Should be an integer' % str(lesson))
        self.lesson = lesson
        try:
            chapter = int(chapter)
        except Exception:
            raise Exception('Chapter number invalid: %s. Should be an integer' % str(chapter))
        self.chapter = chapter
        lessonobjs = practice_question.objects.filter(number=lesson)
        if len(lessonobjs) == 0:
            raise Exception('Lesson not exists: %d' % lesson)
        self.language = lessonobjs[0].language

    def evaluate(self):
        evaluator = Evaluator.instance(self.language)
        evaluation = evaluator.evaluate(self.code, self.lesson, self.chapter)
        self.all_passed = True
        for e in evaluation:
            if e[0] == 'FAILED':
                self.all_passed = False
                break
        return evaluation