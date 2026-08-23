from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "auctions"


urlpatterns = [

    # =====================================================
    # AUTHENTICATION (Password Reset)
    # =====================================================

    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
        name="password_reset",
    ),

    # =====================================================
    # HOME / AUCTIONS
    # =====================================================

    path(
        "",
        views.auction_list,
        name="home",
    ),

    path(
        "auctions/",
        views.auction_list,
        name="auction_list",
    ),

    path(
        "auctions/<int:auction_id>/",
        views.auction_detail,
        name="auction_detail",
    ),


    # =====================================================
    # USER DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "dashboard/redirect/",
        views.dashboard_redirect,
        name="dashboard_redirect",
    ),


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard",
    ),

    path(
        "add-item/",
        views.add_item,
        name="add_item",
    ),

    path(
        "item/<int:item_id>/close/",
        views.close_bidding,
        name="close_bidding",
    ),


    # =====================================================
    # ITEM DETAIL
    # =====================================================

    path(
        "item/<int:item_id>/",
        views.item_detail,
        name="item_detail",
    ),


    # =====================================================
    # PLACE BID
    # =====================================================

    path(
        "item/<int:item_id>/bid/",
        views.place_bid,
        name="place_bid",
    ),


    # =====================================================
    # EDIT / DELETE BID
    # =====================================================

    path(
        "bid/<int:bid_id>/edit/",
        views.edit_bid,
        name="edit_bid",
    ),

    path(
        "bid/<int:bid_id>/delete/",
        views.delete_bid,
        name="delete_bid",
    ),


    # =====================================================
    # CATEGORY
    # =====================================================

    path(
        "category/<int:category_id>/",
        views.category_detail,
        name="category_detail",
    ),


    # =====================================================
    # SUBCATEGORY
    # =====================================================

    path(
        "subcategory/<int:subcategory_id>/",
        views.subcategory_detail,
        name="subcategory_detail",
    ),


    # =====================================================
    # ANNOUNCEMENTS
    # =====================================================

    path(
        "announcements/",
        views.announcements,
        name="announcements",
    ),

    path(
        "announcements/<int:announcement_id>/",
        views.announcement_detail,
        name="announcement_detail",
    ),
]