from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    startbid = models.IntegerField()
    imageupload = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, blank=True)
    currentprice = models.IntegerField(blank=True, null=True)
    highestbidder = models.IntegerField(blank=True, null=True)
    userAuction = models.ForeignKey(User, related_name="auctionItems", on_delete=models.CASCADE)
    closed = models.BooleanField()
    def __str__(self):
        return f"{ self.id } { self.title }"

class Bids(models.Model):
    biduser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userbids")
    bidprice = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{ self.id }"

class Comments(models.Model):
    commentuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentsofusers")
    commentauc = models.ForeignKey(AuctionListing, null=True, on_delete=models.CASCADE, related_name="commentsofposts")
    comment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{ self.id } {self.comment} {self.commentauc}"

class Wishlist(models.Model):
    wid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wlsofusers")
    waucid = models.ForeignKey(AuctionListing, null=True, on_delete=models.CASCADE, related_name="wlofposts")

    def __str__(self):
        return f"{self.wid}{self.waucid}"