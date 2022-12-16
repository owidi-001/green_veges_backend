from cart.models import CartItem
from cart.serializers import CartItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rider.forms import RiderForm
from rider.models import Rider, OrderRider
from rider.serializers import CartItemRiderSerializer, RiderSerializer


class RiderViews(APIView):
    """ Views for rider """
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self,request):
        riders = Rider.objects.all()
        serializer = RiderSerializer(riders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        form = RiderForm(request.POST)
        
        # print(form.is_valid())

        brand=request.data.get("brand")
        dob=request.data.get("dob")
        national_id=request.data.get("national_id")
        license=request.data.get("license")
        
        # print("Pre rider creation")
        rider=Rider.objects.get_or_create(user=request.user,brand=brand,dob=dob,national_id=national_id,license=license)[0]
        # print("Post rider creation")

        if rider:
            rider.save()
            serializer = RiderSerializer(rider)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(form.errors)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST) 


class RiderOrderViews(APIView):
    """ Rider views"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    """ Gets a list of all orders belonging to the rider """

    def get(self, request):
        rider = get_object_or_404(Rider, user=request.user)

        order_for_rider = OrderRider.objects.filter(rider=rider)

        serializer = CartItemRiderSerializer(order_for_rider, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self,request):
        import json

        data=json.loads(request.body.decode('utf-8'))
        
        print(data)

        order=get_object_or_404(CartItem,id=data["order"])

        if order:
            print(order.product.label)

            order.status=data["status"]
            order.save()
            print("order saved")
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)