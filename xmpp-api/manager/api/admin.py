from django.contrib import admin
from models import ExecutedTest, Category, ExecutedTestConfiguration, Result, Tests

# Register your models here.

myModels = [ExecutedTest, Category, ExecutedTestConfiguration, Result, Tests]
admin.site.register(myModels)

