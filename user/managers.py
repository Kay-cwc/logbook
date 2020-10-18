from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    '''
    custom user model manager
    email as unique identifier => username
    '''

    def create_user(self, email, password, **extra_fields):
        '''
        create user by email and passwrod
        '''
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        '''
        create superuser
        need extra validation here
        '''
        extra_fields.setdefault('is_admin', True)
        # extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must be true')
        '''
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be true')
        '''
        return self.create_user(email, password, **extra_fields)
