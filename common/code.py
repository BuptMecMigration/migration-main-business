# -*- coding: utf-8 -*-

# 代码枚举普适规定

OK = 0

DB_ERROR = 4001

PARAM_ERROR = 4101

AUTHORIZATION_ERROR = 4201

UNKNOWN_ERROR = 4301

CODE_MSG_MAP = {
    OK: 'ok',
    DB_ERROR: '数据库错误',
    PARAM_ERROR: '请求参数错误',
    AUTHORIZATION_ERROR: '认证授权错误',
    UNKNOWN_ERROR: "未知错误"
}

# 全局migration receiver接收的监听端口
# MIGRATION_SERVICE_LISTEN_IP = '127.0.0.1'
MIGRATION_SERVICE_LISTEN_IP = '0.0.0.0'
MIGRATION_SERVICE_LISTEN_PORT = 9901
# 全局flask服务运行IP和端口
# SERVER_IP = '127.0.0.1'
SERVER_IP = '0.0.0.0'
SERVER_PORT = 5001
# tcp传输重试次数
TRIES_MAXIMUM = 5

# 输出日志的时间
MIGRATION_TIME_RECORD_PATH = "/root/migration_time.txt"

# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
