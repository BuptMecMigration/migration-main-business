from common.global_var import GLOBAL_MIGRATION_LIST


class Migration(object):

    @classmethod
    def migration_list_check(cls, user_id: int) -> bool:

        # 检查该id是否在本地迁移列表里
        for id in GLOBAL_MIGRATION_LIST:
            # 如果在：則返回遷移信息
            if user_id == id:
                return True
        # 如果不在：则将该用户添加到本地迁移名单
        return False


    @classmethod
    def migration_list_add(cls, user_id: int):

        # 將該id添加到對應的list里, 以便下一步檢查
        GLOBAL_MIGRATION_LIST.append(user_id)

