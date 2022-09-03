from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_new_listing", views.createL, name="createlisting"),
    path("listing/<str:auctionid>", views.listing, name="listing"),
    path("bidding/<int:auctionid2>", views.bid, name="bid"),
    path("closebid/<int:auctionid3>", views.close, name="closebid"),
    path("comment/<int:auctionid4>", views.comment, name="comment"),
    path("category/<str:namecat1>", views.namecat, name="namecat"),
    path("wishlist/<int:auctionid5>", views.wishlist, name="wishlist"),
    path("wishlist", views.wishlist2, name="wishlist2"),
    path("wishlistremove/<int:auctionid5>", views.wishlistr, name="wishlistr")
]

 