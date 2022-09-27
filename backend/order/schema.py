import coreschema
from rest_framework.schemas import AutoSchema, ManualSchema
import coreapi


class OrderSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.upper() == "POST":
            extra_fields = [
                coreapi.Field("total", required=True, location="form", example="200.99",
                              schema=coreschema.Number(description="Sum of order items value")),
                coreapi.Field("delivery_address", required=True, location="form", example="1",
                              schema=coreschema.Integer(description="Delivery location id")),
            ]

        elif method.upper() == "PUT":
            extra_fields = [
                coreapi.Field("id", required=True, location="form", example="F",
                              schema=coreschema.Integer(description="Order which is to be updated")),
                coreapi.Field("status", required=True, location="form", example="F",
                              schema=coreschema.String(description="Order status eg fulfilled "
                                                                   "cancelled etc")),
            ]

        elif method.upper() == "DELETE":
            extra_fields = [
                coreapi.Field("order", required=True, location="form", example="1",
                              schema=coreschema.Object(required=True,
                                                       description="Order id for the order to be deleted")),
            ]

        elif method.upper() == "PATCH":
            extra_fields = [
                coreapi.Field("status", required=True, location="form", example="F",
                              schema=coreschema.Object(required=True, description="Order status eg fulfilled "
                                                                                  "cancelled etc")),
            ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class OrderItemSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.upper() == "POST":
            extra_fields = [
                coreapi.Field("order", required=True, location="form", example="1",
                              schema=coreschema.Object(required=True, description="Order in which this item belongs")),
                coreapi.Field("product", required=True, location="form", example="1",
                              schema=coreschema.Object(required=True, description="Product id for this order item")),
                coreapi.Field("quantity", required=False, location="form", example="2",
                              schema=coreschema.Object(required=True, description="Enter quantity available")),
            ]

        elif method.upper() == "PUT":
            extra_fields = [
                coreapi.Field("status", required=True, location="form", example="F",
                              schema=coreschema.Object(required=True, description="Order item status eg fulfilled "
                                                                                  "cancelled etc")),
            ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class AddressSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.upper() == "POST":
            extra_fields = [
                coreapi.Field("name", required=True, location="form",
                              schema=coreschema.String(
                                  description="Address name: Eg. Home, Office etc")),
                coreapi.Field("lat", required=True, location="form", example="45.521563",
                              schema=coreschema.Number(description="Location latitude is required")),
                coreapi.Field("long", required=False, location="form", example="-122.677433",
                              schema=coreschema.Number(description="Location longitude is required")),
                coreapi.Field("floor_number", required=False, location="form",
                              schema=coreschema.Number(description="Delivery location floor number")),
                coreapi.Field("door_number", required=False, location="form",
                              schema=coreschema.String(description="Delivery location door/house number"))
            ]

        elif method.upper() in ["PUT", "PATCH"]:
            extra_fields = [
                coreapi.Field("id", required=False, location="form",
                              schema=coreschema.Integer(
                                  description="Id of the address to be updated")),
                coreapi.Field("name", required=False, location="form",
                              schema=coreschema.String(
                                  description="Address name: Eg. Home, Office etc")),
                coreapi.Field("floor_number", required=False, location="form",
                              schema=coreschema.Number(description="Delivery location floor number")),
                coreapi.Field("door_number", required=False, location="form",
                              schema=coreschema.String(
                                  description="Delivery location door/house number"))
            ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class FeedbackSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.upper() == "GET":
            extra_fields = [
                coreapi.Field("order", required=True, location="form",
                              schema=coreschema.Integer(description="Order id for the related feedback"))
            ]

        elif method.upper() == "POST":
            extra_fields = [
                coreapi.Field("order", required=True, location="form",
                              schema=coreschema.Object(required=True, description="Order for the related feedback")),
                coreapi.Field("message", required=True, location="form",
                              example="The product was good/bad, delivery slow/fast etc.",
                              schema=coreschema.Object(required=True, description="Feedback Message/Comment/Review")),
                coreapi.Field("rating", required=False, location="form", example="1-5",
                              schema=coreschema.Object(required=True, description="Rate the servce out of 5 stars")),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields
