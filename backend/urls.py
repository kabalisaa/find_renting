from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/rental/', include('renting.urls')),
    path('api/auth/', include('users.urls')),

    # # Optional API:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # # Optional UI:
    path('api/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_title = "Admin panel"
admin.site.site_header = "Kigali House Renting System"
admin.site.index_title = "Management"