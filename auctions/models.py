from django.db import models
from django.contrib.auth.models import User


# =========================================================
# CATEGORY
# =========================================================

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: 🚗, 🏠, 💻, 🏭"
    )

    class Meta:

        verbose_name_plural = "Categories"

        ordering = [
            'name'
        ]

    def __str__(self):

        return self.name


# =========================================================
# SUBCATEGORY
# =========================================================

class SubCategory(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    class Meta:

        verbose_name_plural = "Subcategories"

        ordering = [
            'name'
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'category',
                    'name'
                ],
                name='unique_subcategory_per_category'
            )
        ]

    def __str__(self):

        return f"{self.category.name} - {self.name}"


# =========================================================
# AUCTION
# =========================================================

class Auction(models.Model):

    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Live', 'Live'),
        ('Closed', 'Closed'),
    ]

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    location = models.CharField(
        max_length=200
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Upcoming'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title


# =========================================================
# ITEM
# =========================================================

class Item(models.Model):

    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name='items'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items'
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items'
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField()

    starting_price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='auction_items/',
        blank=True,
        null=True
    )

    condition = models.CharField(
        max_length=100,
        blank=True
    )

    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_items'
    )

    is_sold = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =========================================================
# BID
# =========================================================

class Bid(models.Model):

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='bids'
    )

    bidder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bids'
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            '-amount'
        ]

    def __str__(self):

        return f"{self.bidder.username} - {self.amount}"


# =========================================================
# ANNOUNCEMENT
# =========================================================

class Announcement(models.Model):

    title = models.CharField(
        max_length=200
    )

    content = models.TextField()

    published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title