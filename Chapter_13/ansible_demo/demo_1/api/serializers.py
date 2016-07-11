from rest_framework import serializers
from .models import *

class DemoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Demo

