from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BidForm, RegisterForm, EmailLoginForm
from .models import Auction, Item, Bid, Announcement


# =========================================================
# LOGIN
# =========================================================

class CustomLoginView(LoginView):

    template_name = 'registration/login.html'

    authentication_form = EmailLoginForm

    def form_valid(self, form):

        user = form.get_user()

        login(
            self.request,
            user
        )

        # =================================================
        # ADMIN / STAFF / SUPERUSER
        # =================================================

        if user.is_superuser or user.is_staff:

            return redirect(
                'admin_dashboard'
            )

        # =================================================
        # NORMAL USER
        # =================================================

        return redirect(
            'dashboard'
        )


# =========================================================
# HOME
# =========================================================

def home(request):

    auctions = Auction.objects.all().order_by(
        '-created_at'
    )[:6]

    announcements = Announcement.objects.filter(
        published=True
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'auctions/home.html',
        {
            'auctions': auctions,
            'announcements': announcements,
        }
    )


# =========================================================
# AUCTION LIST
# =========================================================

def auction_list(request):

    auctions = Auction.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'auctions/auction_list.html',
        {
            'auctions': auctions,
        }
    )


# =========================================================
# AUCTION DETAIL
# =========================================================

def auction_detail(request, auction_id):

    auction = get_object_or_404(
        Auction,
        id=auction_id
    )

    items = auction.items.all()

    return render(
        request,
        'auctions/auction_detail.html',
        {
            'auction': auction,
            'items': items,
        }
    )


# =========================================================
# PLACE BID
# =========================================================

@login_required
def place_bid(request, item_id):

    item = get_object_or_404(
        Item,
        id=item_id
    )

    if item.is_sold:

        messages.error(
            request,
            'Mnada wa bidhaa hii umeshafungwa!'
        )

        return redirect(
            'auction_detail',
            auction_id=item.auction.id
        )

    highest_bid = item.bids.first()

    if request.method == 'POST':

        form = BidForm(request.POST)

        if form.is_valid():

            bid_amount = form.cleaned_data['amount']

            minimum_bid = item.starting_price

            if highest_bid:
                minimum_bid = highest_bid.amount

            if bid_amount <= minimum_bid:

                messages.error(
                    request,
                    f'Dau lako lazima liwe kubwa kuliko '
                    f'TZS {minimum_bid:,.2f}'
                )

            else:

                bid = form.save(commit=False)

                bid.item = item

                bid.bidder = request.user

                bid.save()

                messages.success(
                    request,
                    'Dau lako limewekwa kikamilifu!'
                )

                return redirect(
                    'auction_detail',
                    auction_id=item.auction.id
                )

    else:

        form = BidForm()

    return render(
        request,
        'auctions/place_bid.html',
        {
            'item': item,
            'form': form,
            'highest_bid': highest_bid,
        }
    )


# =========================================================
# CLOSE BIDDING
# ADMIN ONLY
# =========================================================

@login_required
@user_passes_test(
    lambda u: u.is_staff or u.is_superuser
)
def close_bidding(request, item_id):

    item = get_object_or_404(
        Item,
        id=item_id
    )

    highest_bid = item.bids.first()

    if highest_bid:

        item.winner = highest_bid.bidder

        item.is_sold = True

        item.save()

        messages.success(
            request,
            f'Mnada umefungwa! Mshindi ni '
            f'{item.winner.first_name or item.winner.username}.'
        )

    else:

        item.is_sold = True

        item.save()

        messages.warning(
            request,
            'Mnada umefungwa bila kuwa na ofa yoyote.'
        )

    return redirect(
        'admin_dashboard'
    )


# =========================================================
# USER DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    # ADMIN ASIINGIE USER DASHBOARD

    if request.user.is_superuser or request.user.is_staff:

        return redirect(
            'admin_dashboard'
        )

    bids = Bid.objects.filter(
        bidder=request.user
    ).select_related(
        'item',
        'item__auction'
    ).order_by(
        '-created_at'
    )

    won_items = Item.objects.filter(
        winner=request.user
    )

    return render(
        request,
        'auctions/dashboard.html',
        {
            'bids': bids,
            'won_items': won_items,
        }
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@login_required
def admin_dashboard(request):

    # NORMAL USER ASIINGIE ADMIN DASHBOARD

    if not (
        request.user.is_staff
        or request.user.is_superuser
    ):

        return redirect(
            'dashboard'
        )

    auctions = Auction.objects.all()

    items = Item.objects.all()

    bids = Bid.objects.all()

    announcements = Announcement.objects.all()

    return render(
        request,
        'auctions/admin_dashboard.html',
        {
            'auctions': auctions,
            'items': items,
            'bids': bids,
            'announcements': announcements,
        }
    )


# =========================================================
# DASHBOARD REDIRECT
# =========================================================

@login_required
def dashboard_redirect(request):

    if (
        request.user.is_superuser
        or request.user.is_staff
    ):

        return redirect(
            'admin_dashboard'
        )

    return redirect(
        'dashboard'
    )


# =========================================================
# EDIT BID
# =========================================================

@login_required
def edit_bid(request, bid_id):

    bid = get_object_or_404(
        Bid,
        id=bid_id,
        bidder=request.user
    )

    item = bid.item

    if item.is_sold:

        messages.error(
            request,
            'Huwezi kubadilisha dau, mnada umekwisha fungwa!'
        )

        return redirect(
            'dashboard'
        )

    highest_bid = item.bids.first()

    if request.method == 'POST':

        form = BidForm(
            request.POST,
            instance=bid
        )

        if form.is_valid():

            bid_amount = form.cleaned_data['amount']

            minimum_bid = item.starting_price

            if highest_bid and highest_bid != bid:

                minimum_bid = highest_bid.amount

            if bid_amount <= minimum_bid:

                messages.error(
                    request,
                    f'Dau lako jipya lazima liwe kubwa kuliko '
                    f'TZS {minimum_bid:,.2f}'
                )

            else:

                form.save()

                messages.success(
                    request,
                    'Dau lako limesasishwa kwa mafanikio!'
                )

                return redirect(
                    'dashboard'
                )

    else:

        form = BidForm(
            instance=bid
        )

    return render(
        request,
        'auctions/edit_bid.html',
        {
            'form': form,
            'bid': bid,
            'item': item,
        }
    )


# =========================================================
# DELETE BID
# =========================================================

@login_required
def delete_bid(request, bid_id):

    bid = get_object_or_404(
        Bid,
        id=bid_id,
        bidder=request.user
    )

    if bid.item.is_sold:

        messages.error(
            request,
            'Huwezi kufuta dau, mnada umekwisha fungwa!'
        )

        return redirect(
            'dashboard'
        )

    if request.method == 'POST':

        bid.delete()

        messages.success(
            request,
            'Dau lako limefutwa kwa mafanikio!'
        )

        return redirect(
            'dashboard'
        )

    return render(
        request,
        'auctions/delete_bid.html',
        {
            'bid': bid,
        }
    )


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.user.is_authenticated:

        if request.user.is_staff or request.user.is_superuser:

            return redirect(
                'admin_dashboard'
            )

        return redirect(
            'dashboard'
        )

    if request.method == 'POST':

        form = RegisterForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                'Akaunti yako imetengenezwa kwa mafanikio! '
                'Sasa unaweza kuingia kwa kutumia email yako.'
            )

            return redirect(
                'login'
            )

    else:

        form = RegisterForm()

    return render(
        request,
        'registration/register.html',
        {
            'form': form,
        }
    )