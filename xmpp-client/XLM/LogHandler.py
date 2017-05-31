import logging, logging.handlers


class LogHandler:
    def __init__(self, logpath, markpath):
        self.LOG = logging.getLogger('log')
        loghdlr1 = logging.handlers.RotatingFileHandler(logpath, "a", 0, 1)
        fmt1 = logging.Formatter("%(asctime)s %(threadName)-10s %(message)s", "%Y-%m-%d %H:%M:%S")
        loghdlr1.setFormatter(fmt1)
        self.LOG.addHandler(loghdlr1)
        self.LOG.setLevel(logging.INFO)

        self.HONEY = logging.getLogger('honey')
        loghdlr2 = logging.handlers.RotatingFileHandler(markpath, "a", 0, 1)
        fmt2 = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
        loghdlr2.setFormatter(fmt2)
        self.HONEY.addHandler(loghdlr2)
        self.HONEY.setLevel(logging.INFO)

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
        if self.HONEY is not None:
            self.HONEY.info(msg)


def main():
    global log_mgr
    log_mgr = LogHandler("mylog", "mymark")
    log_mgr.LOG("This is normal log")
    log_mgr.LOG("This is mark log")



if __name__ == "__main__":
    main()