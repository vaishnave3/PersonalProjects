from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import AuctionListing, Bids, Comments, Wishlist
from .models import User
from datetime import date

def index(request):
    listcat = ["Fashion", "Food", "Cars"]
    return render(request, "auctions/index.html", {
        "listcat" : listcat,
        "auctions" : AuctionListing.objects.all()
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


def createL(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startbid = request.POST["startbid"]
        imgupload = request.POST["imgupload"]
        category = request.POST["category"]
        userAuction = request.user.id
        highestbidder = request.user.id
        currentprice = startbid
        newlisting = AuctionListing(title=title, description=description, 
        startbid=startbid, imageupload=imgupload, 
        category=category, userAuction=request.user, currentprice=currentprice, 
        highestbidder=highestbidder, closed=False)
        newlisting.save()
        return render(request, "auctions/displayNewAuction.html", {
            "title" : title,
            "description" : description,
            "startbid" : startbid,
            "imgupload" : imgupload,
            "category" : category,
            "userAuction" : userAuction,
            "currentprice" : currentprice
        })
    return render(request, "auctions/createL.html")


def listing(request, auctionid):
    f1 = AuctionListing.objects.get(pk=auctionid)
    f2 = False
    message3 = []
    try:
        f3 = Comments.objects.filter(commentauc=auctionid)
        n = f3.count()
        for i in range(n):
            message3.append(f3[i])
    except Comments.DoesNotExist:
        f3 = None
    message2 = ""
    if request.user.id == f1.highestbidder and f1.closed == True :
        message2 = "CONGRATS!!! YOU WON THIS BID."
    if request.user.id == f1.userAuction.id:
        f2 = True
    f1 = AuctionListing.objects.get(pk=auctionid)
    return render(request, "auctions/samp.html", {
        "f1" : f1,
        "f2" : f2,
        "message3" : message3,
        "message2" : message2
    })
    #return HttpResponse(f"{f1.userbids.id}")

def bid(request, auctionid2):
    if request.method == 'POST':
        bidprice = request.POST["bidprice"]
        f1 = AuctionListing.objects.get(pk=auctionid2)
        if f1.currentprice >= int(bidprice):
            message = "Your bid price is less than current price of item. Cannot place bid."
        else:
            message = "Bid Placed."
            b = Bids(biduser=request.user, bidprice=bidprice)
            b.save()
            f1.highestbidder = request.user.id
            f1.currentprice = bidprice
            f1.save()
    return render(request, "auctions/samp.html", {
        "message" : message,
        "high" : f1.highestbidder,
        "f1" : f1
    })

def close(request, auctionid3):
    f3 = AuctionListing.objects.get(pk=auctionid3)
    f3.closed = True
    f3.save()
    message = "Closed Bid Item."
    return render(request, "auctions/samp.html", {
        "message" : message,
        "high" : f3.highestbidder,
        "f1" : f3
    })

def comment(request, auctionid4):
    if request.method == 'POST':
        comment = request.POST["comment"]
        userid = request.user
        commentauc = AuctionListing.objects.get(pk=auctionid4)
        c = Comments(commentuser=userid, comment=comment, commentauc=commentauc)
        c.save()
        return HttpResponseRedirect(reverse(listing, args=(auctionid4,)))
    return HttpResponse("ok")


def namecat(request, namecat1):
    f1 = AuctionListing.objects.filter(category=namecat1)
    return render(request, "auctions/namecat.html", {
        "items" : f1
    })

def wishlist(request, auctionid5):
    if request.method == 'POST':
        f1 = AuctionListing.objects.get(pk=auctionid5)
        wid = request.user
        waucid = AuctionListing.objects.get(pk=auctionid5)
        w = Wishlist(wid=wid, waucid=waucid)
        w.save()
        return render(request, "auctions/samp.html", {
        "message" : "Added to your watchlist.",
        "high" : f1.highestbidder,
        "f1" : f1
    })

def wishlist2(request):
    rid = request.user.id
    w = Wishlist.objects.filter(wid=rid)
    n = w.count()
    message = "Wishlist Empty."
    wl = []
    for i in range(n):
        wl.insert(i, w[i].waucid)
        message = ""
    return render(request, "auctions/wishlist.html", {
        "wl" : wl,
        "message" : message
    })

def wishlistr(request, auctionid5):
    if request.method == 'POST':
        try:
            w = Wishlist.objects.filter(waucid=auctionid5)
            w.delete()
            return HttpResponseRedirect(reverse(index))
        except w.DoesNotExist:
            return HttpResponseRedirect(reverse(index))
    return HttpResponse("removed")