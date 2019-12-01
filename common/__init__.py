from .utils.logger_utils import Logger 


# log = Logger('../../logs/all.log', level='info')
# log.logger.debug('debug')
# log.logger.info('info')
# log.logger.warning('警告')
# log.logger.error('报错')
# log.logger.critical('严重')
log=Logger('../../logs/error.log', level='error').logger.error('error')