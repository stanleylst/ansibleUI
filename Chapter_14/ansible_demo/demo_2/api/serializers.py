from rest_framework import serializers
from .models import *

class Demo2Serializer(serializers.ModelSerializer):

    class Meta:
        model = Demo2

class Ansible_HostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ansible_Host

class Ansible_Yml_RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ansible_Yml_Register


