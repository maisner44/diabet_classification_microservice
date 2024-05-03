class AdminRoleMixin:
    def get_admin_role(self, request):
        user = request.user
        is_admin = user.groups.filter(name='Administators').exists()
        return is_admin