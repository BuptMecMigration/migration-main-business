from .logger_utils import Logger
import os 


# log = Logger('../../logs/all.log', level='info')
# log.logger.debug('debug')
# log.logger.info('info')
# log.logger.warning('警告')
# log.logger.error('报错')
# log.logger.critical('严重')

loggerPath=os.path.curdir+"/logs"
if not os.path.exists(loggerPath):
    os.mkdir(loggerPath)
log=Logger(loggerPath+"/info.log", level='info')
log_error=Logger(loggerPath+"/error.log", level='error')