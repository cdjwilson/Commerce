from cgi import print_exception
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment, Watchlist
from .forms import ListingForm, BidForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": list(reversed(Listing.objects.all())),
    })


def login_view(request):
    if request.method == "POST":        

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="/login")
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            price = form.cleaned_data['price']
            img = form.cleaned_data.get('img')
            description = form.cleaned_data['description']
            try:
                category = form.cleaned_data['category']
            except:
                category = None
            listing = Listing.objects.create(user = user , title = title, price = price, image = img, description = description, category = category.title())
            listing.save()
        return redirect(index)
    else:
        form = ListingForm()
        return render(request, "auctions/create.html", {
            "form": form
        })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    try:
        if request.user.is_authenticated:
            watchlist = Watchlist.objects.get(user=request.user, listingWatchlist=listing)
        else:
            watchlist = None
    except Watchlist.DoesNotExist:
        watchlist = None
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": BidForm(),
        "comments": Comment.objects.filter(listingComment = listing).all(),
        "watchlist": watchlist
    })

@login_required(login_url="/login")
def bid(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bidPrice = form.cleaned_data['bid']
            listing1 = Listing.objects.get(pk=listing_id)
            if listing1.user != request.user and bidPrice >= listing1.price:
                if listing1.highest_bid == None :
                    bid = Bid.objects.create(user = request.user, listingBid=listing1, bid=bidPrice)
                    listing1.highest_bid = bid
                    bid.save()
                    listing1.save()
                elif listing1.highest_bid.bid < bidPrice:
                    bid = Bid.objects.create(user = request.user, listingBid=listing1, bid=bidPrice)
                    listing1.highest_bid = bid
                    bid.save()
                    listing1.save()
    return redirect(listing, listing_id)

@login_required(login_url="/login")
def comment(request, listing_id):
    if request.method == "POST":
        commentText = request.POST['comment']
        if commentText != "":
            listing1 = Listing.objects.get(pk=listing_id)
            comment = Comment.objects.create(user = request.user, listingComment=listing1, comment = commentText)
            comment.save()
    return redirect(listing, listing_id)

@login_required(login_url="/login")
def deleteComment(request, listing_id, comment_id):
    if request.method == "POST":
        comment = Comment.objects.get(pk=comment_id)
        if comment.user == request.user:
            comment.delete()
    return redirect(listing, listing_id)

@login_required(login_url="/login")
def deleteListing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        if listing.user == request.user:
            listing.delete()
    return redirect(index)

@login_required(login_url="/login")
def addWatchlist(request, listing_id):
    listing1 = Listing.objects.get(pk=listing_id)
    watchlist = Watchlist.objects.create(user = request.user, listingWatchlist = listing1)
    watchlist.save()
    return redirect(listing, listing_id)

@login_required(login_url="/login")
def watchlist(request):
    watchlistListing = Watchlist.objects.filter(user = request.user).all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlistListing
    })

@login_required(login_url="/login")
def removeWatchlist(request, listing_id):
    listing1 = Listing.objects.get(pk=listing_id)
    watchlist = Watchlist.objects.get(user=request.user, listingWatchlist = listing1)
    if watchlist.user == request.user:
        watchlist.delete()
    return redirect(listing, listing_id)

def categories(request):
    categories = Listing.objects.all().values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def categoryList(request, category):
    listings = Listing.objects.filter(category = category)
    return render(request, "auctions/categoryListings.html", {
        "listings": listings
    })

@login_required(login_url="/login")
def addCategory(request, listing_id):
    listing1 = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        category = request.POST['category'].title()
        listing1.category = category
        listing1.save()
        return redirect(listing, listing_id)
    return render(request, "auctions/addCategory.html", {
        "listings": listing1
    })

@login_required(login_url="/login")
def removeCategory(request, listing_id):
    listing1 = Listing.objects.get(pk=listing_id)
    category = listing1.category
    if request.method == "POST":
        listing1.category = None
        listing1.save()
        return redirect(categoryList, category)

@login_required(login_url="/login")
def endListing(request, listing_id):
    listing1 = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        listing1.ended = True
        listing1.save()
        return redirect(listing, listing_id)