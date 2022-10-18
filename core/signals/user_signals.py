
def user_created(sender, created=False, instance=None, **kwargs):

    if created and instance is not None and not instance.is_verified:
        instance.send_verification_email()


def user_verified(sender, instance=None, **kwargs):

    if instance.is_verified:
        instance.assign_author_group()
