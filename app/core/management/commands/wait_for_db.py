# make application sleep in between each database check
import time
# connections=Test if database connection is available
from django.db import connections
# operation error that django throws if the db is not availbale
from django.db.utils import OperationalError
# Class to build on in order to create our custom command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for Database .....')
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database is not available,waiting 1 second')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS(
            'DaTaBasE available 🛌🛌🛌🛌🛌🛌🛌🛌🛌🛌🛌🛌🏃‍♂️🏃‍♂️🏃‍♂️🏃‍♂️'))
