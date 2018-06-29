#import psutil

#p = psutil.Process()

class Limits:
    cpulimit = 1
    realtimelimit = 1000
    memlimit = 50000000
    stacklimit = 10000000
    filesizelimit = 1
    filenolimit = 1
    stdoutlimit = 50000

    '''
    @staticmethod
    def set_limits():
        p.rlimit(psutil.RLIMIT_CPU, (1,1))
        p.rlimit(psutil.RLIMIT_DATA, (Limits.memlimit, Limits.memlimit))
        '''


