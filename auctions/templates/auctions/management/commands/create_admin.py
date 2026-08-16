import os
import django
from django.contrib.auth import get_user_model

# Weka mipangilio ya Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freeemindportal.settings')
django.setup()

User = get_user_model()

# Taarifa za admin uliyozitaka
username = 'freemindagency2023@gmail.com'
email = 'freemindagency2023@gmail.com'
password = 'amreen'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Akaunti ya Admin '{username}' imetengenezwa kwa mafanikio!")
else:
    # Kama tayari ipo, inahakikisha password inajisasisha kuwa hiyo hiyo
    admin_user = User.objects.get(username=username)
    admin_user.set_password(password)
    admin_user.save()
    print(f"Akaunti ya Admin '{username}' imesasishwa kikamilifu!")