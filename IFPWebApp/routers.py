# routers.py
class HomeAffairsRouter:
    """
    Routes database operations for homeaffairs models
    """
    ha_models = {
        'citizen', 'address', 'document', 'birthcertificate',
        'deathcertificate', 'passport', 'photo', 'marriage',
        'marriageparticipant'
    }

    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.ha_models:
            return 'homeaffairs'
        return None

    def db_for_write(self, model, **hints):
        # Prevent writes to homeaffairs models
        if model._meta.model_name in self.ha_models:
            return None  # Or raise error for write attempts
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations between HA models
        if {obj1._meta.model_name, obj2._meta.model_name} <= self.ha_models:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'homeaffairs':
            return False  # Never migrate homeaffairs database
        elif db == 'default':
            # Only allow IFPWebApp models that aren't HA models
            return model_name not in self.ha_models
        return None