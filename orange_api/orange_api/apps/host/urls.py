
from django.urls import path,re_path


from rest_framework import routers
from host.views import HostApiView,HostCategoryApiView,ExeclHostView

# router = routers.DefaultRouter()
# router.register('', HostApiView, basename='host')


urlpatterns = [
    path('',HostApiView.as_view({'get': 'list', 'post': 'create'})),
    re_path('(?P<pk>\d+)', HostApiView.as_view({'get':'retrieve', 'put':'update','delete': 'destroy'})),
    re_path(r'^category/$', HostCategoryApiView.as_view()),
    re_path('excel_host', ExeclHostView.as_view())
]

# urlpatterns += router.urls