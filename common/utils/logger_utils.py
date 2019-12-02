import logging
from logging import handlers

# logging.basicConfig(level=logging.INFO,
#                     # filename='runtime.log',  # 写入的文件路径
#                     # filemode='a',  # 表示读写模式是追加写入的方式
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)


class Logger(object):
    # 日志关系映射map
    level_map = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level = 'info', when = 'D', backCount = 3,
                 format = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(format)  # 设置日志格式
        self.logger.setLevel(self.level_map.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        # 设置屏幕上显示的格式
        sh.setFormatter(format_str)
        # 往文件里写入
        # 指定间隔时间自动生成文件的处理器
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')
        # 实例化 TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒、M 分、H 小时、D 天、W 每星期（interval==0 时代表星期一）midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式，以及输出到相应目录的具体string
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)



