import io
import multiprocessing
from datetime import datetime

from django.core.management import BaseCommand
from main.models import *
from AdvaRisk.settings import DATA_FILE_PATH


class Command(BaseCommand):

    @staticmethod
    def create_reviews(items):
        col_names = {
            0: "product",
            1: "user",
            2: "name",
            3: "helpfulness",
            4: "score",
            5: "timestamp",
            6: "summary",
            7: "text"
        }
        for item in items:
            lines = item.split("\n")
            obj = {}
            try:
                for i, line in enumerate(lines):
                    split_line = line.split(":")
                    value = ''.join(split_line[1:]).strip()
                    if i == 4:
                        obj[col_names[i]] = float(value)
                    elif i == 5:
                        obj[col_names[i]] = datetime.utcfromtimestamp(float(value))
                    else:
                        obj[col_names[i]] = value
                Review.objects.create(**obj)
            except Exception as e:
                print(e)

    def handle(self, *args, **options):
        print("Starting data migration...")
        file_path = DATA_FILE_PATH
        with io.open(file_path, "r", encoding="ISO-8859-1") as file:
            data = file.read()
        items = data.split("\n\n")
        print("Items to be migrated =", str(len(items)))
        inputs = [items[i*150000:i*150000+150000] for i in range(4)]
        pool = multiprocessing.Pool(processes=4)
        pool.map(Command.create_reviews, inputs)

