from django.test import TestCase

# Create your tests here.
from accounts.messaging.producer import publish_user_created
publish_user_created({"id": 1, "name": "mimi"})
