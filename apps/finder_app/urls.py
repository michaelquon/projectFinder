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
	url(r'^clearSearch$', views.clearSearch),
	url(r'^join_activity/(?P<number>\d+)$', views.joinActivity),
	url(r'^leave_activity/(?P<number>\d+)$', views.leaveActivity),
	url(r'^delete_activity/(?P<number>\d+)$', views.deleteActivity),
	url(r'^leave_review/(?P<number>\d+)$', views.leaveReview),
	url(r'^view_review/(?P<number>\d+)$', views.viewReview),
	url(r'^close_review$', views.exitReview),
	url(r'^write_message/(?P<number>\d+)$', views.messagesid),
    url(r'^processMessage$', views.processMessage),
    url(r'^closeMessages$', views.closeMessages),
]
