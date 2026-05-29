from django.contrib import admin

from django.urls import path, include
def home(request):

    return JsonResponse({

        "status": "ok",

        "message": "ESG Backend Running"

    })
urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('ingestion.urls')),
]