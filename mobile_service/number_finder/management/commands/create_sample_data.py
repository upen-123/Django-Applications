from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
import string
import random
from number_finder.models import Users

user = get_user_model()


class Command(BaseCommand):
    help = "Create Sample Data"

    def handle(self, *args, **options):
        data = []
        self.stdout.write("Task started")
        for i in range(1000):
            name = ''.join(random.choices(string.ascii_lowercase, k=7))
            phone_number = ''.join(random.choices(string.digits, k=10))
            email = ''.join(random.choices(string.ascii_lowercase, k=6)) + "@gmail.com"
            password = name + "123"
            data.append({"name": name, "phone_number": phone_number, "email": email, "password": password})

        user_list = [Users(**kwargs) for kwargs in data]
        user.objects.bulk_create(user_list)

        self.stdout.write("Task ended")
