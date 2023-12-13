from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated


class IsInAccountsGroup(IsAuthenticated):
    def has_permission(self, request, view):
        # Check if the user is in the "accounts" group
        user = request.user
        try:
            accounts_group = Group.objects.get(name='accounts')
            return accounts_group in user.groups.all()
        except:
            return False
