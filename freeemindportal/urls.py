from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from auctions import views


urlpatterns = [

    # =====================================================
    # DJANGO ADMIN
    # =====================================================

    path(
        "admin/",
        admin.site.urls
    ),


    # =====================================================
    # AUCTIONS APP
    # =====================================================

    path(
        "",
        include("auctions.urls")
    ),


    # =====================================================
    # LOGIN
    # =====================================================

    path(
        "accounts/login/",
        views.CustomLoginView.as_view(),
        name="login",
    ),


    # =====================================================
    # LOGOUT
    # =====================================================

    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(
            next_page="login"
        ),
        name="logout",
    ),


    # =====================================================
    # REGISTER
    # =====================================================

    path(
        "accounts/register/",
        views.register,
        name="register",
    ),
]


# =========================================================
# MEDIA / STATIC - DEVELOPMENT
# =========================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )