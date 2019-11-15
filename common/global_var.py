from threading import Lock
from models.user.user_info import UserService
# 定义相关的全局名单对迁移信息进行访问
# 其内部为用户ID，便于查询是否在迁移序列中
class global_var(object):
    
    __migration_lock=Lock()
    __user_service_lock=Lock()
    __GLOBAL_USER_SERVICE_LIST :map={}
    __GLOBAL_MIGRATION_LIST :map={}

    @classmethod 
    # 如果 us不在map中,返回false,us为空
    def get_migration_service(cls,user_token:int)->(bool,UserService):
        cls.__migration_lock.acquire()
        if user_token not in cls.__GLOBAL_MIGRATION_LIST:
            cls.__migration_lock.release()
            return False,""
        else:
            cls.__migration_lock.release()
            return True,cls.__GLOBAL_MIGRATION_LIST[user_token]

    @classmethod 
    # 如果 us不在map中,返回false,us为空
    def get_user_service(cls,user_token:int)->(bool,UserService):
        cls.__user_service_lock.acquire()
        if user_token not in cls.__GLOBAL_USER_SERVICE_LIST:
            cls.__user_service_lock.release()
            return False,""
        else:
            cls.__user_service_lock.release()
            return True,cls.__GLOBAL_USER_SERVICE_LIST[user_token]
