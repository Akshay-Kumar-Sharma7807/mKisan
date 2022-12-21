from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("listings/create", views.create_listing, name="create"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("listings", views.listings, name='listings'),
    path("comment/add/<int:listing_id>", views.add_comment, name="add_comment"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("bid/add/<int:listing_id>", views.add_bid, name="add-bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_listing, name="category_listing"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("close/<int:listing_id>", views.close_listing, name="close_listing"),
    path("__reload__/", include("django_browser_reload.urls")),
]
