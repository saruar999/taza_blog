from django.apps import AppConfig
import django.dispatch

user_verified = django.dispatch.Signal()


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):

        from django.db.models import signals
        from django.utils.crypto import get_random_string
        from .signals import user_signals, migration_signals

        signals.post_save.connect(
            sender='core.User',
            receiver=user_signals.user_created,
            dispatch_uid=get_random_string(length=10)
        )

        signals.post_save.connect(
            sender='core.Author',
            receiver=user_signals.user_created,
            dispatch_uid=get_random_string(length=10)
        )

        signals.post_migrate.connect(
            receiver=migration_signals.create_user_groups,
            dispatch_uid=get_random_string(length=10)
        )

        signals.post_migrate.connect(
            receiver=migration_signals.create_super_user,
            dispatch_uid=get_random_string(length=10)
        )

        user_verified.connect(receiver=user_signals.user_verified,
                              dispatch_uid=get_random_string(length=10)
                              )
