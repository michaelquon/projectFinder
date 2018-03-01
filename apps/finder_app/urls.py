from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index), 
	url(r'^process$', views.process), 
	url(r'^login$', views.login), 
	url(r'^logout$', views.logout),
    url(r'^main$', views.dash),
    url(r'^activity/register$', views.addActivity),
    url(r'^activity/search$', views.searchActivity),
]
