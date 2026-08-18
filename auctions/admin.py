from django.contrib import admin

from .models import (
    Auction,
    Item,
    Bid,
    Announcement,
    Category,
    SubCategory,
)


# =========================================================
# CATEGORY
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'description',
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
# SUBCATEGORY
# =========================================================

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'description',
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
# AUCTION
# =========================================================

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'location',
        'status',
        'start_date',
        'end_date',
        'created_at',
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
# ITEM
# =========================================================

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'auction',
        'category',
        'subcategory',
        'starting_price',
        'condition',
        'is_sold',
        'winner',
        'created_at',
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

    autocomplete_fields = (
        'category',
        'subcategory',
        'winner',
    )


# =========================================================
# BID
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
        'bidder__email',
    )

    ordering = (
        '-amount',
    )


# =========================================================
# ANNOUNCEMENT
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

    ordering = (
        '-created_at',
    )