from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("listing/<int:listing_id>/comment/<int:comment_id>", views.deleteComment, name="deleteComment"),
    path("listing/<int:listing_id>/delete", views.deleteListing, name="deleteListing"),
    path("listing/<int:listing_id>/watchlist", views.addWatchlist, name="addWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>/removeWatchlist", views.removeWatchlist, name="removeWatchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.categoryList, name="categoryList"),
    path("addCategory/<int:listing_id>", views.addCategory, name="addCategory"),
    path("removeCategory/<int:listing_id>", views.removeCategory, name="removeCategory"),
    path("listing/<int:listing_id>/endListing", views.endListing, name="endListing")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
