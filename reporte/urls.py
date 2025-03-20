from django.urls import include, path
import app.api.urls 

urlpatterns = [
    path('v1/', include(app.api.urls)),
]
