from django.urls import path

from rider.views import RiderOrderViews,RiderViews


urlpatterns = [
    path("riders/", RiderViews.as_view(), name="rider"),
    path("riders/orders", RiderOrderViews.as_view(), name="rider_orders"),
]
