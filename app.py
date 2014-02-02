from log.logger import LinuxLogger

LinuxLogger.initialize()
logger = LinuxLogger.instance()
logger.log_forever()
