from __future__ import unicode_literals

from djblets.extensions.hooks import TemplateHook, URLHook

from reviewboard.extensions.base import Extension
from reviewboard.urls import review_request_url_names, diffviewer_url_names

from cc_counter.urls import urlpatterns

class CCCounter(Extension):
	"""Links up CC Counter extension into CCCounter's framework
	"""
	metadata = {
		'Name': 'CCCounter'
	}

	has_admin_site = False
	def __init__(self, *args, **kwargs):
		super(CCCounter, self).__init__(*args, **kwargs)
		URLHook(self, urlpatterns)
		TemplateHook(self, "base-after-content", "cc_counter/reviewrequest_cc.html",
				apply_to=diffviewer_url_names)