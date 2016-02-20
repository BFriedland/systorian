from django.conf.urls import patterns, url, include
from rest_framework import routers
from api import EntryViewSet, CurrentEntryView, SingleDayEntryView  # , SinceDateEntryView #ArbitrarilyFilteredEntryView,

router = routers.DefaultRouter()
router.register(r'entry', EntryViewSet)


urlpatterns = patterns(
    '',
    url(r'^$', CurrentEntryView.as_view()), # remember this must be at the end or everything else skips it

    # urls for Django Rest Framework API
    url(r'^api/v1/current/$', CurrentEntryView.as_view()),
    # url(r'^api/v1/contains/(?P<desired_data>.+)', ArbitrarilyFilteredEntryView.as_view()),
    # url(r'^api/v1/since/(?P<time>.+)', SinceDateEntryView.as_view()),
    url(r'^api/v1/on/(?P<year>.+)/(?P<month>.+)/(?P<day>.+)/$', SingleDayEntryView.as_view()),
    url(r'^api/v1/', include(router.urls)),
)
