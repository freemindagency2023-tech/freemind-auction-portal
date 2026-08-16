from django.contrib import admin

from .models import (
    Auction,
    Item,
    Bid,
    Announcement,
)


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


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'auction',
        'starting_price',
        'condition',
    )

    list_filter = (
        'auction',
        'condition',
    )

    search_fields = (
        'name',
        'description',
    )


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