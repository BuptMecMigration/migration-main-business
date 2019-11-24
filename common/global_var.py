from threading import Lock
from models.user.user_info import UserService
# 定义相关的全局名单对迁移信息进行访问
# 其内部为用户ID，便于查询是否在迁移序列中


# 对应结构:__GLOBAL_USER_SERVICE_MAP,__GLOBAL_MIGRATION_MAP都为
# map,map中key为user_id
# value为保存当前user_id下所有service的map
# value的map以service_id做key,value为UserService对象

class service_map(object):

    __migration_lock = Lock()
    __user_service_lock = Lock()
    __GLOBAL_USER_SERVICE_MAP: map = {}
    __GLOBAL_MIGRATION_MAP: map = {}
    __us_func:function =__default_func
    __mig_func:function =__default_func

    @classmethod
    def __default_func(cls,**args):
        pass

    @classmethod
    def register_us_func(cls,fn:function):
        cls.__us_func =fn
    @classmethod
    def register_migration_func(cls,fn:function):
        cls.__mig_func =fn
    @classmethod
    def deregister_us_func(cls):
        cls.__us_func =cls.__default_func
    @classmethod
    def deregister_mig_func(cls):
        cls.__mig_func =cls.__default_func

    @classmethod
    # 如果 us不在map中,返回false,us为空
    def get_migration_service(cls, user_token: int, service_id:int) -> (bool, UserService):
        cls.__migration_lock.acquire()
        if user_token not in cls.__GLOBAL_MIGRATION_MAP:
            cls.__migration_lock.release()
            return False, None
        else:
            us_map = cls.__GLOBAL_MIGRATION_MAP[user_token]
            if service_id not in us_map:
                cls.__migration_lock.release()
                return False, None
            us=cls.__GLOBAL_MIGRATION_MAP[service_id]
            cls.__migration_lock.release()
            return True, us

    @classmethod
    # 如果 us不在map中,返回false,us为空
    def get_user_service(cls, user_token: int, service_id: int) -> (bool, UserService):
        cls.__user_service_lock.acquire()
        if user_token not in cls.__GLOBAL_USER_SERVICE_MAP:
            cls.__user_service_lock.release()
            return False, None
        else:
            us_map = cls.__GLOBAL_USER_SERVICE_MAP[user_token]
            if service_id not in us_map:
                cls.__user_service_lock.release()
                return False, None
            us= cls.__GLOBAL_USER_SERVICE_MAP[service_id]
            cls.__user_service_lock.release()
            return True, us

    @classmethod
    # 如果 us不在map中,返回false,us为空
    def get_all_migration_service(cls, user_token: int) -> (bool, map(int,UserService)):
        cls.__migration_lock.acquire()
        if user_token not in cls.__GLOBAL_MIGRATION_MAP:
            cls.__migration_lock.release()
            return False, None
        else:
            us_map = cls.__GLOBAL_MIGRATION_MAP[user_token]
            cls.__migration_lock.release()
            return True, us_map

    @classmethod
    # 如果 us不在map中,返回false,us为空
    def get_all_user_service(cls, user_token: int) -> (bool, map(int,UserService)):
        cls.__user_service_lock.acquire()
        if user_token not in cls.__GLOBAL_USER_SERVICE_MAP:
            cls.__user_service_lock.release()
            return False, None
        else:
            us_map = cls.__GLOBAL_USER_SERVICE_MAP[user_token]
            cls.__user_service_lock.release()
            return True, us_map

    @classmethod
    def set_migration_service(cls, us: UserService) -> bool:
        if type(us) is not UserService:
            raise TypeError
        cls.__migration_lock.acquire()
        if us.service_token.user_id in cls.__GLOBAL_MIGRATION_MAP:
            # 当前service_id已经存入,不能再存,返回false
            if us.service_token.service_id in  cls.__GLOBAL_MIGRATION_MAP[us.service_token.user_id]:
                cls.__migration_lock.release()
                return False
            # 新存入一个,返回true    
            cls.__GLOBAL_MIGRATION_MAP[us.service_token.user_id][us.service_token.service_id]=us
            cls.__migration_lock.release()
            # call migration func
            cls.__mig_func(us)
            return True
        else:
            # 新建map,存入对象
            cls.__GLOBAL_MIGRATION_MAP[us.service_token.user_id]={}
            cls.__GLOBAL_MIGRATION_MAP[us.service_token.user_id][us.service_token.service_id]=us
            cls.__migration_lock.release()
            # call migration func
            cls.__mig_func(us)
            return True

    @classmethod
    def set_user_service(cls, us: UserService) -> bool:
        if type(us) is not UserService:
            raise TypeError
        cls.__user_service_lock.acquire()
        if us.service_token.user_id in cls.__GLOBAL_USER_SERVICE_MAP:
            # 当前service_id已经存入,不能再存,返回false
            if us.service_token.service_id in  cls.__GLOBAL_USER_SERVICE_MAP[us.service_token.user_id]:
                cls.__user_service_lock.release()
                return False
            # 新存入一个,返回true
            cls.__GLOBAL_USER_SERVICE_MAP[us.service_token.user_id][us.service_token.service_id] = us
            cls.__user_service_lock.release()
            # call migration func
            cls.__us_func(us)
            return True
        else:
            # 新建map,存入对象
            cls.__GLOBAL_USER_SERVICE_MAP[us.service_token.user_id] = {}
            cls.__GLOBAL_USER_SERVICE_MAP[us.service_token.user_id][us.service_token.service_id] = us
            cls.__user_service_lock.release()
            # call migration func
            cls.__us_func(us)
            return True

    @classmethod
    def remove_migration_service(cls, user_token: int,service_id:int) -> bool:
        cls.__migration_lock.acquire()
        if user_token not in cls.__GLOBAL_MIGRATION_MAP:
            cls.__migration_lock.release()
            return False
        else:
            # 当前service_id已经存入,不能再存,返回false
            if service_id not in cls.__GLOBAL_MIGRATION_MAP[user_token]:
                cls.__migration_lock.release()
                return False
            else:
                del cls.__GLOBAL_MIGRATION_MAP[user_token][service_id]
                if len(cls.__GLOBAL_MIGRATION_MAP[user_token])==0:
                    del cls.__GLOBAL_MIGRATION_MAP[user_token]
                
                cls.__migration_lock.release()
                return True

    @classmethod
    def remove_user_service(cls, user_token: int,service_id:int) -> bool:
        cls.__user_service_lock.acquire()
        if user_token not in cls.__GLOBAL_USER_SERVICE_MAP:
            cls.__user_service_lock.release()
            return False
        else:
            # 当前service_id已经存入,不能再存,返回false
            if service_id not in cls.__GLOBAL_USER_SERVICE_MAP[user_token]:
                cls.__user_service_lock.release()
                return False
            else:
                del cls.__GLOBAL_USER_SERVICE_MAP[user_token][service_id]
                if len(cls.__GLOBAL_USER_SERVICE_MAP[user_token])==0:
                    del cls.__GLOBAL_USER_SERVICE_MAP[user_token]
                
                cls.__user_service_lock.release()
                return True