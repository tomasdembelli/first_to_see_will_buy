from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions



class CustomDjangoModelPermission(DjangoModelPermissions):

    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']