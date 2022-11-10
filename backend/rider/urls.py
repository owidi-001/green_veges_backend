from django.urls import path

from rider.views import RiderOrderViews,RiderCreateViews


urlpatterns = [
    path("riders/", RiderCreateViews.as_view(), name="rider"),
    path("riders/orders", RiderOrderViews.as_view(), name="rider_orders"),
]
