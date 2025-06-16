class HomeAffairsRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'homeaffairs':
            return 'homeaffairs'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'homeaffairs':
            return 'homeaffairs'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == 'homeaffairs' or
            obj2._meta.app_label == 'homeaffairs'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'homeaffairs':
            return db == 'homeaffairs'
        return None
