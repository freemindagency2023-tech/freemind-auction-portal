from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # =====================================================
    # DJANGO ADMIN
    # =====================================================

    path(
        'admin/',
        admin.site.urls
    ),


    # =====================================================
    # AUCTIONS APP
    # =====================================================

    path(
        '',
        include('auctions.urls')
    ),

]


# =========================================================
# STATIC & MEDIA FILES (LOCAL DEVELOPMENT)
# =========================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )