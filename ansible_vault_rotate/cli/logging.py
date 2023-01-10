import logging


class FormattingConsoleLogHandler(logging.StreamHandler):
    colors = {
        logging.DEBUG: '\033[37m',
        logging.INFO: '\033[34m',
        logging.WARNING: '\033[33m',
        logging.ERROR: '\033[31m',
        logging.CRITICAL: '\033[101m',
    }
    reset = '\033[0m'
    my_formatter = logging.Formatter('\033[37m[%(filename)10s:%(lineno)s]\033[0m \033[37m---\033[0m %(message)s')

    def format(self, record):
        color = self.colors[record.levelno]
        log = self.my_formatter.format(record)
        reset = self.reset
        return color + "%7s " % record.levelname + reset + log
