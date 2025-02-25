import logging

class LoggerConfigurator:
    @staticmethod
    def configure_logger():
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(threadName)s] %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )

        file_handler = logging.FileHandler('tops.log', mode='a')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger


logger = LoggerConfigurator.configure_logger()
