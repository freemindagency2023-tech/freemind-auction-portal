from django.db import models
from django.contrib.auth.models import User


class Auction(models.Model):
    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Live', 'Live'),
        ('Closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Upcoming'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Item(models.Model):
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=200)
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
    
    # --- HIVI VYOMBO VIMEONGEZWA KWA AJILI YA KUSHINDA BIDHAA ---
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_items'
    )
    is_sold = models.BooleanField(default=False)
    # -----------------------------------------------------------

    def __str__(self):
        return self.name


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
        ordering = ['-amount']

    def __str__(self):
        return f"{self.bidder.username} - {self.amount}"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title