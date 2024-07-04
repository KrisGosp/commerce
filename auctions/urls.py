from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("rm_watchlist/<int:listing_id>", views.rm_watchlist, name="rm_watchlist"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
]
