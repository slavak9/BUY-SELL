from django.test import TestCase

# Create your tests here.
import datetime

f = datetime.datetime.strptime('0001 11 5','%Y %m %d')

d = datetime.datetime.now()
b = datetime.datetime(d.year-150,d.month,d.day)
print(datetime.timedelta(weeks=12))

