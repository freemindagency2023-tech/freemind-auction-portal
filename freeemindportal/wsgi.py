import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freeemindportal.settings')

application = get_wsgi_application()

# Hii itatengeneza admin yenyewe app ikianza kuwaka mtandaoni
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    username = 'freemindagency2023@gmail.com'
    password = 'amreen'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=username, password=password)
    else:
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
except Exception as e:
    pass