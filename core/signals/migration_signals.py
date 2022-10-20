def add_model_permissions_to_new_group(group_name, model):
    from django.contrib.auth.models import Permission
    from django.contrib.auth.models import Group

    if model == 'all':
        permissions = Permission.objects.exclude(content_type__app_label__in=('contenttypes', 'sessions',))
    else:
        permissions = Permission.objects.filter(content_type__model__in=model)

    group, created = Group.objects.get_or_create(name=group_name)

    for _permission in permissions:
        group.permissions.add(_permission)


def create_user_groups(sender, **kwargs):
    add_model_permissions_to_new_group(group_name='superuser',
                                       model='all')

    add_model_permissions_to_new_group(group_name='author',
                                       model=('posts', 'comments', 'author',
                                              'tags', 'authorfavoriteposts', 'posttags'),)

    add_model_permissions_to_new_group(group_name='moderator',
                                       model=('posts', 'comments', 'author',
                                              'tags', 'posttags'), )

    add_model_permissions_to_new_group(group_name='role_admin',
                                       model=('permission', 'group', 'admins',
                                              'author'),)


def create_super_user(sender, **kwargs):

    from core.models.admins import Admins

    if not Admins.objects.filter(email='admin@admin.com').exists():
        superuser = Admins.objects.create_superuser(email='admin@admin.com', password='123',
                                                    first_name='super', last_name='user',
                                                    gender='M')
        superuser.assign_superuser_group()








