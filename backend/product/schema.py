import coreschema
from rest_framework.schemas import AutoSchema, ManualSchema
import coreapi


class ProductSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.upper() == "POST":
            extra_fields = [
                coreapi.Field("name", required=True, location="form",
                              schema=coreschema.Object(required=True, description="Product name is required")),
                coreapi.Field("price", required=True, location="form", example="20.99",
                              schema=coreschema.Object(required=True, description="Product price is required")),
                coreapi.Field("stock", required=False, location="form", example="2",
                              schema=coreschema.Object(required=True, description="Enter stock available")),
                coreapi.Field("description", required=True, location="form",
                              schema=coreschema.Object(required=True, description="Product description is required"))
            ]

            if method.upper() == "PUT":
                extra_fields = [
                    coreapi.Field("name", required=True, location="form",
                                  schema=coreschema.Object(required=True, description="Product name is required")),
                    coreapi.Field("price", required=True, location="form", example="20.99",
                                  schema=coreschema.Object(required=True, description="Product price is required")),
                    coreapi.Field("stock", required=False, location="form", example="2",
                                  schema=coreschema.Object(required=True, description="Enter stock available")),
                    coreapi.Field("description", required=True, location="form",
                                  schema=coreschema.Object(required=True,
                                                           description="Product description is required"))
                ]
            manual_fields = super().get_manual_fields(path, method)
            return manual_fields + extra_fields
