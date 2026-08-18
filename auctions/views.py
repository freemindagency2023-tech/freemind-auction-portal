from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BidForm, RegisterForm, EmailLoginForm
from .models import (
    Auction,
    Item,
    Bid,
    Announcement,
    Category,
    SubCategory,
)


# =========================================================
# LOGIN
# =========================================================

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = EmailLoginForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        if user.is_superuser or user.is_staff:
            return redirect('admin_dashboard')

        return redirect('dashboard')


# =========================================================
# HOME
# =========================================================

def home(request):
    auctions = Auction.objects.all().order_by('-created_at')[:6]

    announcements = Announcement.objects.filter(
        published=True
    ).order_by('-created_at')

    categories = Category.objects.prefetch_related(
        'subcategories'
    ).order_by('name')

    return render(
        request,
        'auctions/home.html',
        {
            'auctions': auctions,
            'announcements': announcements,
            'categories': categories,
        }
    )


# =========================================================
# CATEGORY BASED AUCTIONS
# =========================================================

def auction_list(request):

    categories = Category.objects.prefetch_related(
        'subcategories'
    ).order_by('name')

    selected_category = request.GET.get('category')
    selected_subcategory = request.GET.get('subcategory')

    selected_category_obj = None
    selected_subcategory_obj = None

    items = Item.objects.select_related(
        'auction',
        'category',
        'subcategory'
    ).prefetch_related(
        'bids'
    ).order_by('-created_at')

    # -----------------------------------------------------
    # CATEGORY FILTER
    # -----------------------------------------------------

    if selected_category:

        try:
            selected_category_id = int(selected_category)

            selected_category_obj = get_object_or_404(
                Category,
                id=selected_category_id
            )

            items = items.filter(
                category=selected_category_obj
            )

        except (ValueError, TypeError):
            selected_category = None

    # -----------------------------------------------------
    # SUBCATEGORY FILTER
    # -----------------------------------------------------

    if selected_subcategory:

        try:
            selected_subcategory_id = int(
                selected_subcategory
            )

            selected_subcategory_obj = get_object_or_404(
                SubCategory,
                id=selected_subcategory_id
            )

            items = items.filter(
                subcategory=selected_subcategory_obj
            )

            if not selected_category:
                selected_category_obj = (
                    selected_subcategory_obj.category
                )

                selected_category = str(
                    selected_category_obj.id
                )

        except (ValueError, TypeError):
            selected_subcategory = None

    # -----------------------------------------------------
    # SUBCATEGORIES
    # -----------------------------------------------------

    if selected_category_obj:

        subcategories = SubCategory.objects.filter(
            category=selected_category_obj
        ).order_by('name')

    else:

        subcategories = SubCategory.objects.none()

    return render(
        request,
        'auctions/auction_list.html',
        {
            'categories': categories,
            'subcategories': subcategories,
            'items': items,

            'selected_category': selected_category,
            'selected_subcategory': selected_subcategory,

            'selected_category_obj': selected_category_obj,
            'selected_subcategory_obj': selected_subcategory_obj,
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

    items = auction.items.select_related(
        'category',
        'subcategory'
    ).prefetch_related(
        'bids'
    )

    categories = Category.objects.all().order_by('name')

    return render(
        request,
        'auctions/auction_detail.html',
        {
            'auction': auction,
            'items': items,
            'categories': categories,
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

        winner_name = (
            item.winner.first_name
            or item.winner.username
        )

        messages.success(
            request,
            f'Mnada umefungwa! Mshindi ni {winner_name}.'
        )

    else:

        item.is_sold = True
        item.save()

        messages.warning(
            request,
            'Mnada umefungwa bila kuwa na ofa yoyote.'
        )

    return redirect('admin_dashboard')


# =========================================================
# USER DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin_dashboard')

    bids = Bid.objects.filter(
        bidder=request.user
    ).select_related(
        'item',
        'item__auction',
        'item__category',
        'item__subcategory',
    ).order_by('-created_at')

    won_items = Item.objects.filter(
        winner=request.user
    ).select_related(
        'auction',
        'category',
        'subcategory',
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

    if not (
        request.user.is_staff
        or request.user.is_superuser
    ):
        return redirect('dashboard')

    auctions = Auction.objects.all().order_by('-created_at')

    items = Item.objects.select_related(
        'auction',
        'category',
        'subcategory',
        'winner',
    ).all().order_by('-created_at')

    bids = Bid.objects.select_related(
        'item',
        'bidder',
    ).all().order_by('-created_at')

    announcements = Announcement.objects.all().order_by(
        '-created_at'
    )

    categories = Category.objects.prefetch_related(
        'subcategories'
    ).all().order_by('name')

    subcategories = SubCategory.objects.select_related(
        'category'
    ).all().order_by(
        'category__name',
        'name'
    )

    return render(
        request,
        'auctions/admin_dashboard.html',
        {
            'auctions': auctions,
            'items': items,
            'bids': bids,
            'announcements': announcements,
            'categories': categories,
            'subcategories': subcategories,
        }
    )


# =========================================================
# DASHBOARD REDIRECT
# =========================================================

@login_required
def dashboard_redirect(request):

    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin_dashboard')

    return redirect('dashboard')


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

        return redirect('dashboard')

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

                return redirect('dashboard')

    else:

        form = BidForm(instance=bid)

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

        return redirect('dashboard')

    if request.method == 'POST':

        bid.delete()

        messages.success(
            request,
            'Dau lako limefutwa kwa mafanikio!'
        )

        return redirect('dashboard')

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

        if (
            request.user.is_staff
            or request.user.is_superuser
        ):
            return redirect('admin_dashboard')

        return redirect('dashboard')

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Akaunti yako imetengenezwa kwa mafanikio! '
                'Sasa unaweza kuingia kwa kutumia email yako.'
            )

            return redirect('login')

    else:

        form = RegisterForm()

    return render(
        request,
        'registration/register.html',
        {
            'form': form,
        }
    )