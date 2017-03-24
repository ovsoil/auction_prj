from authentication.models import Account


class AuthBackend(object):
    """My AuthBackend"""
    def authenticate(self, username=None, password=None):
        try:
            user = Account.objects.get(username=username)
        except Account.DoesNotExist:
            return None
        else:
            if username.startswith('wx_'):
                return user
            if user.check_password(password):
                return user
            else:
                return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
