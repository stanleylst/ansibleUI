import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.conf.urls import patterns, url, include

from rest_framework import routers
from api.api_demo_2 import *
from views import *
from django.core import urlresolvers

router = routers.SimpleRouter()
router.register(r'demo2_api', Demo2ViewSet)
router.register(r'ansible_host_api', Ansible_HostViewSet)
router.register(r'ansible_yml_register_api', Ansible_Yml_RegisterViewSet)

urlpatterns = [
        url(r'', include(router.urls)),
]


urlpatterns += [
        url(r'^demo_server_deploy/', demo_server_deploy),
        url(r'^demo_server_create/', demo_server_create),
        url(r'^demo_server_add/', demo_server_add),
        url(r'^demo_server_delete/', demo_server_delete),
        url(r'^demo_server_modify/', demo_server_modify),

        url(r'^demo_read_log/', demo_read_log),

        url(r'^demo_upload/', demo_upload),

        url(r'^demo_config_center/', demo_config_center),
        url(r'^demo_operate_interface/', demo_operate_interface),
]
