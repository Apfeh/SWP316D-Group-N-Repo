class HomeAffairsRouter:
    """
    A router to control all database operations on models in the
    home affairs application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read home affairs models go to homeaffairs DB.
        """
        if model._meta.app_label == 'IFPWebApp':
            return 'homeaffairs'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write home affairs models go to homeaffairs DB.
        """
        if model._meta.app_label == 'IFPWebApp':
            return 'homeaffairs'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both models are in the homeaffairs database.
        """
        if obj1._meta.app_label == 'IFPWebApp' and obj2._meta.app_label == 'IFPWebApp':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure home affairs models only appear in the 'homeaffairs' database.
        """
        if app_label == 'IFPWebApp':
            return db == 'homeaffairs'
        return None