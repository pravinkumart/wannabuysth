#coding=utf8
__author__ = 'Alexander.Li'
from celery import Celery


def tob(s, enc='utf8'):
    return s.encode(enc) if isinstance(s, unicode) else bytes(s)
def touni(s, enc='utf8', err='strict'):
    return s.decode(enc, err) if isinstance(s, bytes) else unicode(s)

class Frame(object):
    def __init__(self, tb):
        self.tb = tb
        frame = tb.tb_frame
        self.locals = {}
        self.locals.update(frame.f_locals)

    def print_path(self):
        import traceback
        return touni(traceback.format_tb(self.tb, limit=1)[0])

    def print_local(self):
        return u"\n".join(["%s=%s" % (k, self.dump_value(self.locals[k])) for k in self.locals])

    def dump_value(self, v):
        try:
            return touni(str(v))
        except:
            return u"value can not serilizable"

def print_debug(ex):
    import sys
    exc_type, exc_value, exc_traceback = sys.exc_info()
    frames = []
    tb = exc_traceback
    frames.append(tb.tb_frame)
    detail = u"alex error -Exception:%s\n" % touni(ex.message)
    while tb.tb_next:
        tb = tb.tb_next
        fm = Frame(tb)
        detail += fm.print_path()
        detail += u"\nlocals variables:\n"
        detail += fm.print_local()
        detail += u"\n-------------------------------------------------------\n"
    return detail

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery