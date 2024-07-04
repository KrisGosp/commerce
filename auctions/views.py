from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # Add this line
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Listing, User, Watchlist, Bid, Comment

def check_owner_watching(request, listing_id):
    is_owner = False
    is_watching = False
    if request.user.id == Listing.objects.get(id=listing_id).user.id:
        is_owner = True
    else:
        is_owner = False

# Check if listing is in watchlist of current user
    if Watchlist.objects.filter(listing=listing_id).exists():
        if request.user.id == Watchlist.objects.get(listing=listing_id).user.id:
            is_watching = True
        else:
            is_watching = False

    return is_owner, is_watching

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]

        user = request.user.id
        # Creating and saving new listing
        new_listing = Listing(
            user=User.objects.get(id=user),
            title=title,
            description=description,
            starting_bid=starting_bid,
            current_price=starting_bid,
            image_url=image_url,
            category=category
        )
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html")

def listing(request, listing_id):
    # Check if listing belongs to current user in order to show close button
    is_owner, is_watching = check_owner_watching(request, listing_id)

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(id=listing_id),
        "is_watching": is_watching,
        "is_owner": is_owner
    })

@login_required
def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        user_id = request.user.id
        is_owner = False

        if request.user.id == Listing.objects.get(id=listing_id).user.id:
            is_owner = True
        else:
            is_owner = False

        is_watching = Watchlist.objects.filter(user=user_id, listing=listing_id).exists()
        # Adding listing to watchlist
        if not is_watching:
            watchlist = Watchlist(
                user=User.objects.get(id=user_id),
                listing=Listing.objects.get(id=listing_id)
            )
            watchlist.save()
            return render(request, "auctions/listing.html", {
                "is_watching": True,
                "is_owner": is_owner,
                "listing": Listing.objects.get(id=listing_id),
            })
        else:
            Watchlist.objects.filter(user=user_id, listing=listing_id).delete()
            return render(request, "auctions/listing.html", {
                "is_watching": False,
                "is_owner": is_owner,
                "listing": Listing.objects.get(id=listing_id),
            })

    all_watched = Watchlist.objects.filter(user=request.user.id).values_list('listing_id', flat=True)
    listings = Listing.objects.filter(id__in=all_watched)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def rm_watchlist(request, listing_id):
    all_watched = Watchlist.objects.filter(user=request.user.id).values_list('listing_id', flat=True)
    listings = Listing.objects.filter(id__in=all_watched)

    Watchlist.objects.filter(user=request.user.id, listing=listing_id).delete()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def place_bid(request, listing_id):
    if request.method == "POST":
        bid = request.POST["bid"]
        listing = Listing.objects.get(id=listing_id)
        if float(bid) > listing.current_price:
            # save listing price update and winner
            listing.current_price = float(bid)
            listing.current_winner = request.user
            listing.save()
            # save bid
            user = request.user
            new_bid = Bid(
                user=user,
                listing=listing,
                amount=bid
            )
            new_bid.save()

        is_owner, is_watching = check_owner_watching(request, listing_id)
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(id=listing_id),
            "is_watching": is_watching,
            "is_owner": is_owner
        })

    return render(request, "auctions/index.html")

def close(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.is_open = False
    listing.save()
    return redirect("listing", listing_id=listing_id)

def comment(request, listing_id):
    is_owner, is_watching = check_owner_watching(request, listing_id)

    if request.method == "POST":
        comment = request.POST["content"]
        user = request.user
        new_comment = Comment(
            user=user,
            listing=Listing.objects.get(id=listing_id),
            content=comment
        )
        new_comment.save()
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(id=listing_id),
        "is_watching": is_watching,
        "is_owner": is_owner
    })