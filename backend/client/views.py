# Create your views here.
from product.models import Product
from product.serializer import ProductSerializer

from rest_framework.response import Response
from rest_framework.views import APIView


class ClientPageView(APIView):
    """ Client profile dashboard
        Client views products
        Makes order
        Process payment
     """

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)
