class UserRoleMixin:
    def get_user_roles(self, request):
        user = request.user
        is_patient = user.groups.filter(name='Patients').exists()
        is_doctor = user.groups.filter(name='Doctors').exists()
        return is_patient, is_doctor