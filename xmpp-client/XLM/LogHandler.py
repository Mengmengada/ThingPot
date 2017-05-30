import logging, logging.handlers


class LogMgr:
    def __init__(self, logpath, markpath):
        self.LOG = logging.getLogger('log')
        loghdlr1 = logging.handlers.RotatingFileHandler(logpath, "a", 0, 1)
        fmt1 = logging.Formatter("%(asctime)s %(threadName)-10s %(message)s", "%Y-%m-%d %H:%M:%S")
        loghdlr1.setFormatter(fmt1)
        self.LOG.addHandler(loghdlr1)
        self.LOG.setLevel(logging.INFO)

        self.MARK = logging.getLogger('mark')
        loghdlr2 = logging.handlers.RotatingFileHandler(markpath, "a", 0, 1)
        fmt2 = logging.Formatter("%(message)s")
        loghdlr2.setFormatter(fmt2)
        self.MARK.addHandler(loghdlr2)
        self.MARK.setLevel(logging.INFO)

    def error(self, msg):
        if self.LOG is not None:
            self.LOG.error(msg)

    def info(self, msg):
        if self.LOG is not None:
            self.LOG.info(msg)

    def debug(self, msg):
        if self.LOG is not None:
            self.LOG.debug(msg)

    def mark(self, msg):
        if self.MARK is not None:
            self.MARK.info(msg)


def main():
    global log_mgr
    log_mgr = LogMgr("mylog", "mymark")
    log_mgr.error('[mylog]This is error log')
    log_mgr.info('[mylog]This is info log')
    log_mgr.debug('[mylog]This is debug log')
    log_mgr.mark('[mymark]This is mark log')


if __name__ == "__main__":
    main()