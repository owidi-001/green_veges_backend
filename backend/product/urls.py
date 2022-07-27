from django.urls import path


from .views import ProductView

urlpatterns=[
    path('products/',ProductView,name="product"),
]