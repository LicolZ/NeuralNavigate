# NeuralNavigate/myproject/user/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, error_messages={
        'unique': "A user is already registered with this e-mail address",
    })
    name = models.CharField(max_length=255, blank=True, null=True)  # Name field
    about = models.TextField(blank=True, null=True)  # About Me field
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# user's saved definitions 
class SavedDefinition(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    definition = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # for tracking when the definition was saved

    class Meta:
        unique_together = ('user', 'topic', 'definition')  # to ensure the same definition isn't saved twice for the same topic and user

