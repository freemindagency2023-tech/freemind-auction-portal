from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        '',
        views.home,
        name='home'
    ),

    # =====================================================
    # AUCTIONS
    # =====================================================

    path(
        'auctions/',
        views.auction_list,
        name='auction_list'
    ),

    path(
        'auctions/<int:auction_id>/',
        views.auction_detail,
        name='auction_detail'
    ),

    # =====================================================
    # ADMIN / ITEM
    # =====================================================

    path(
        'admin-dashboard/add-item/',
        views.add_item,
        name='add_item'
    ),

    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'dashboard-redirect/',
        views.dashboard_redirect,
        name='dashboard_redirect'
    ),

    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    # =====================================================
    # BIDDING
    # =====================================================

    path(
        'item/<int:item_id>/bid/',
        views.place_bid,
        name='place_bid'
    ),

    path(
        'item/<int:item_id>/close/',
        views.close_bidding,
        name='close_bidding'
    ),

    path(
        'bid/<int:bid_id>/edit/',
        views.edit_bid,
        name='edit_bid'
    ),

    path(
        'bid/<int:bid_id>/delete/',
        views.delete_bid,
        name='delete_bid'
    ),

    # =====================================================
    # LOGIN
    # =====================================================

    path(
        'accounts/login/',
        views.CustomLoginView.as_view(),
        name='login'
    ),

    # =====================================================
    # LOGOUT
    # =====================================================

    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # =====================================================
    # REGISTER
    # =====================================================

    path(
        'accounts/register/',
        views.register,
        name='register'
    ),

    # =====================================================
    # PASSWORD CHANGE
    # =====================================================

    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='auctions/password_change.html',
            success_url='/password-change/done/'
        ),
        name='password_change'
    ),

    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='auctions/password_change_done.html'
        ),
        name='password_change_done'
    ),

    # =====================================================
    # PASSWORD RESET
    # =====================================================

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url='/password-reset/done/'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url='/password-reset-complete/'
        ),
        name='password_reset_confirm'
    ),

    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]