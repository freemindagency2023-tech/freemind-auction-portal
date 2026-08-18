from django.contrib import admin

from .models import (
    Category,
    SubCategory,
    Auction,
    Item,
    Bid,
    Announcement,
)


# =========================================================
# CATEGORY ADMIN
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'icon',
    )

    search_fields = (
        'name',
        'description',
    )

    ordering = (
        'name',
    )


# =========================================================
# SUBCATEGORY ADMIN
# =========================================================

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
    )

    list_filter = (
        'category',
    )

    search_fields = (
        'name',
        'category__name',
        'description',
    )

    ordering = (
        'category',
        'name',
    )


# =========================================================
# AUCTION ADMIN
# =========================================================

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'location',
        'status',
        'start_date',
        'end_date',
    )

    list_filter = (
        'status',
        'start_date',
        'end_date',
    )

    search_fields = (
        'title',
        'description',
        'location',
    )

    ordering = (
        '-created_at',
    )


# =========================================================
# ITEM ADMIN
# =========================================================

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'subcategory',
        'auction',
        'starting_price',
        'condition',
        'is_sold',
        'winner',
    )

    list_filter = (
        'category',
        'subcategory',
        'condition',
        'is_sold',
        'auction',
    )

    search_fields = (
        'name',
        'description',
        'category__name',
        'subcategory__name',
        'auction__title',
    )

    ordering = (
        '-created_at',
    )


# =========================================================
# BID ADMIN
# =========================================================

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):

    list_display = (
        'item',
        'bidder',
        'amount',
        'created_at',
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'item__name',
        'bidder__username',
    )

    readonly_fields = (
        'created_at',
    )

    ordering = (
        '-amount',
    )


# =========================================================
# ANNOUNCEMENT ADMIN
# =========================================================

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'published',
        'created_at',
    )

    list_filter = (
        'published',
        'created_at',
    )

    search_fields = (
        'title',
        'content',
    )

    readonly_fields = (
        'created_at',
    )

    ordering = (
        '-created_at',
    )