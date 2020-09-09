from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books$', views.books),
    url(r'^books/(?P<book_id>\d+)$', views.show),
    url(r'^books/(?P<book_id>\d+)/delete$', views.delete),
    url(r'^books/(?P<book_id>\d+)/unfavorite$', views.unfavorite),
    url(r'^books/(?P<book_id>\d+)/favorite$', views.favorite)
]

