import os
import os.path
import datetime
import logging
import logging.handlers


#오늘날자 :: yyyy-mm-dd
def today()->str:
    return datetime.date.today().isoformat()


class Logger:

    def __call__(self) -> logging:

        logger = logging.getLogger('log')

        if len(logger.handlers) > 0:
            return logger  # Logger already exists

        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] (%(filename)s:%(lineno)d) > %(message)s')

        log_path = 'logs/{}.log'.format(today())
        if not os.path.exists('logs'):
            os.mkdir('logs')

        fileHandler = logging.FileHandler(log_path)
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
        logger.addHandler(streamHandler)

        return logger