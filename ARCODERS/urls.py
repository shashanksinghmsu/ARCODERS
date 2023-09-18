from django import urls
from django.contrib import admin, sitemaps
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from arcoder import views
from arcoder.sitemaps import home_static_sitemaps, program_sitemap, query_sitemap, language_sitemap
from django.contrib.sitemaps.views import sitemap
from ARCODERS.settings import DEBUG


sitemaps = {
    'final_program': program_sitemap,
    'final_query' : query_sitemap,
    'language' : language_sitemap,
    'home' : home_static_sitemaps
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml/', sitemap, {'sitemaps' : sitemaps}),
    path('robots.txt/', include('robots.urls')),
    path('querybook/', include('querybook.urls')),
    path('program/', include('program.urls')),
    path('search/', include('search.urls')),
    path('update/', include('update_profile.urls')),
    path('', include('arcoder.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
