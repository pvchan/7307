# Secure Programming Assignment 2 

1. Clone this repository into a folder on your computer
2. run virtualenv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. python manage.py makemigrations
6. python manage.py migrate
7. Type python manage.py runserver to start a localhost server for the app.




python manage.py shell
from store.models.user import Role
roles = Role.objects.all()
print(roles)
Role.objects.create(name='Admin', description='Administrator Role Description')
Role.objects.create(name='Staff', description='Staff Role Description')
