from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.db.models import Max
from django.utils import timezone

from .models import User, Listing, Comment, Bid, WatchList


class CreateListingForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    starting_bid = forms.IntegerField()
    img = forms.CharField(required=False)
    category = forms.CharField(required=False)

class NewCommentForm(forms.Form):
    text = forms.CharField()

class NewBidForm(forms.Form):
    amount = forms.IntegerField()

def index(request):
    # bids = Bid.objects.filter(listing=int(listing_id)).order_by("-bid_price").values()
    return render(request, "index.html", {
        "title": "Active Listings",
        "listings": Listing.objects.filter(closed=False).order_by("-publication_date")
    })

def about(request):
    return render(request, "about.html")

def listing(request, listing_id):
    listing = Listing.objects.filter(id=int(listing_id)).first()
    bids = Bid.objects.filter(listing=int(listing_id)).order_by("-bid_price").values()
    comments = Comment.objects.filter(listing=int(listing_id)).order_by("comment_date")

    return render(request, "listing.html", {
        "listing": listing,
        "current_price": bids[0]["bid_price"] if bids.count() > 0 else listing.starting_bid,
        "current_bid_user": bids[0]["user_id"] if bids.count() > 0 else listing.user_id,
        "bids": bids,
        "comments": comments,
        "in_watchlist": WatchList.objects.filter(listing_id=int(listing_id)).all().count() > 0,
    })

def add_bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.filter(id=int(listing_id)).first()
        bids = Bid.objects.filter(listing=int(listing_id)).order_by("-bid_price").values()
        # print("-------", bids[0])
        form = NewBidForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            new_bid = Bid(
                user=request.user,
                listing=listing,
                bid_price=form.cleaned_data["amount"]
            )

            current_price = bids[0]["bid_price"] if bids.count() > 0 else listing.starting_bid

            # current_bid = listing.bids.all().order_by("amount").first()
            # if not current_bid:
                # current_bid = Bid(bid_price=listing.starting_bid, listing=listing, user=request.user)
            print(new_bid)
            if not new_bid.bid_price > current_price:
                return HttpResponse("Error: Your Bid is less than or equal to Current Bid")
            new_bid.save()
        return HttpResponseRedirect(f"/listings/{listing_id}")
    else:
        return HttpResponseRedirect(f"/listings/{listing_id}")

def add_comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.filter(id=int(listing_id)).first()
        form = NewCommentForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            new_comment = Comment(
                user=request.user,
                listing=listing,
                comment=form.cleaned_data["text"])
            # new_comment.user = request.user
            # new_comment.listing = Listing.objects.filter(id=int(listing_id)).first()
            print(new_comment)

            new_comment.save()
        return HttpResponseRedirect(f"/listings/{listing_id}")
    else:
        return HttpResponseRedirect(f"/listings/{listing_id}")

@login_required(login_url='/login')
def watchlist(request):
    watchlists = request.user.watchlist.all()
    for watchlist in watchlists:
        print(watchlist.listing)
    return render(request, "watchlist.html", {
        "watchlists": request.user.watchlist.all()
    })

@login_required(login_url='/login')
def add_watchlist(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    print("skjdfsl", WatchList.objects.filter(listing_id=listing_id).all().count())
    if WatchList.objects.filter(listing_id=listing_id).all().count() > 0:
        WatchList.objects.filter(listing_id=listing_id).delete()
        return HttpResponseRedirect(f"/listings/{listing_id}")
        
    watchlist = WatchList(
        listing= listing,
        user= request.user
    )
    print(watchlist)
    watchlist.save()
    return HttpResponseRedirect(f"/listings/{listing_id}")



@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            
            listing = Listing(
                user=request.user,
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                starting_bid=form.cleaned_data["starting_bid"],
                img=form.cleaned_data["img"],
                category=form.cleaned_data["category"] 
            )
            print(listing)
            
            listing.save()

    
    return render(request, "create.html")


@login_required(login_url='/login')
def close_listing(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    listing.closed = True
    listing.save()
    return HttpResponseRedirect(f"/listings/{listing_id}")

def categories(request):
    return render(request, "categories.html")

def category_listing(request, category):

    return render(request, "index.html", {
        "title": "Listings in " + category,
        "listings": Listing.objects.filter(category=category, closed=False)
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        number = request.POST["number"]
        password = request.POST["password"]
        user = authenticate(request, number=number, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid phone number and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    print(request)
    if request.method == "POST":
        username = request.POST["username"]
        number = request.POST['number']
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username,
                email=email,
                password=password,
                number=number
                )
            user.save()
            print("user created")
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
