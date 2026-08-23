from django.contrib import admin

from .models import (
    Auction,
    Item,
    ItemImage,
    Bid,
    Announcement,
    Category,
    SubCategory,
)


# =========================================================
# CATEGORY ADMIN
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "icon",
        "subcategory_count",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "name",
    )

    def subcategory_count(self, obj):
        return obj.subcategories.count()

    subcategory_count.short_description = "Subcategories"


# =========================================================
# SUBCATEGORY ADMIN
# =========================================================

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "description",
        "category__name",
    )

    ordering = (
        "category__name",
        "name",
    )


# =========================================================
# ITEM IMAGE INLINE
# =========================================================

class ItemImageInline(admin.TabularInline):

    model = ItemImage

    extra = 3

    fields = (
        "image",
        "caption",
    )

    ordering = (
        "created_at",
    )


# =========================================================
# ITEM INLINE
# =========================================================

class ItemInline(admin.StackedInline):

    model = Item

    extra = 1

    fields = (
        "name",
        "category",
        "subcategory",
        "description",
        "starting_price",
        "condition",
        "image",
        "is_sold",
        "winner",
    )

    autocomplete_fields = (
        "category",
        "subcategory",
        "winner",
    )

    show_change_link = True


# =========================================================
# AUCTION ADMIN
# =========================================================

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "location",
        "status",
        "start_date",
        "end_date",
        "created_at",
    )

    list_filter = (
        "status",
        "start_date",
        "end_date",
    )

    search_fields = (
        "title",
        "description",
        "location",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    inlines = (
        ItemInline,
    )


# =========================================================
# ITEM IMAGE ADMIN
# =========================================================

@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):

    list_display = (
        "item",
        "caption",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "item__name",
        "caption",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    autocomplete_fields = (
        "item",
    )


# =========================================================
# ITEM ADMIN
# =========================================================

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "auction",
        "category",
        "subcategory",
        "starting_price",
        "condition",
        "is_sold",
        "winner",
        "created_at",
    )

    list_filter = (
        "category",
        "subcategory",
        "condition",
        "is_sold",
        "auction",
    )

    search_fields = (
        "name",
        "description",
        "auction__title",
        "category__name",
        "subcategory__name",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    autocomplete_fields = (
        "auction",
        "category",
        "subcategory",
        "winner",
    )

    inlines = (
        ItemImageInline,
    )


# =========================================================
# BID ADMIN
# =========================================================

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):

    list_display = (
        "item",
        "bidder",
        "amount",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "item__name",
        "bidder__username",
        "bidder__email",
    )

    ordering = (
        "-amount",
    )

    readonly_fields = (
        "created_at",
    )


# =========================================================
# ANNOUNCEMENT ADMIN
# =========================================================

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "published",
        "created_at",
    )

    list_filter = (
        "published",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )