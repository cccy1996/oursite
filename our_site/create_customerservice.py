# This file should be run individually
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "our_site.settings") 
import django
django.setup()

import sys
from django.db import DatabaseError
from django.db import transaction as database_transaction
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from account.models import User_Permission
from customerservice.models import *
from customerservice.views import add_permission

def create_customerservice(username, password, email):
    with database_transaction.atomic():
            try:
                user = User.objects.create_user(username, password=password, email=email)
            except DatabaseError as e:
                return False
            add_permission(user, 'service_permission')
            servant = CustomerService()
            servant.user = user
            servant.save()
            return True

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('usage: python {0} <username> <password> <email>'.format(sys.argv[0]))
        exit(0)
    t = create_customerservice(sys.argv[1], sys.argv[2], sys.argv[3])
    if not t:
        print('adding customer service failed')
    else:
        print('done')