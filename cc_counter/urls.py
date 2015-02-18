from django.conf.urls import patterns, url

from cc_counter import views


urlpatterns = patterns('',
	url(r'^cc/(?P<review_request_id>[0-9]+)/(?P<revision>[0-9]+)/(?P<filediff_id>[0-9]+)/$',
		views.download_ccdata, name='index'),
	url(r'^r/(?P<review_request_id>[0-9]+)/diff/cc/(?P<revision>[0-9]+)/(?P<filediff_id>[0-9]+)/$',
		views.download_ccdata, name='index'),
	url(r'^r/(?P<review_request_id>[0-9]+)/diff/cc/$',
		views.reviewrequest_recent_cc, name='index'),
) 
