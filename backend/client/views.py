# Create your views here.
from product.models import Product
from product.serializer import ProductSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView


class ProductListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
        Product list of available products
    """

    def get(self, request):
        """
        List of all available products
        """
        query = Product.objects.all()

        return Response(
            ProductSerializer(query, many=True).data, status=status.HTTP_200_OK
        )

# cart operations