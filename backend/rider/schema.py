import coreschema
from rest_framework.schemas import AutoSchema, ManualSchema
import coreapi


class ProductSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.upper() == "POST":
            extra_fields = [
                coreapi.Field("license", required=True, location="form",
                              schema=coreschema.Object(required=True, description="Driver license or rider permit")),
                coreapi.Field("national_id", required=True, location="form",
                              schema=coreschema.Object(required=True, description="National Id")),
                coreapi.Field("dob", required=True, location="form",
                              schema=coreschema.Object(required=True, description="Date of birth")),
                coreapi.Field("brand", required=True, location="form",
                              schema=coreschema.Object(required=True, description="Brand name")),
            ]

        if method.upper() == "PUT":
            extra_fields = [
                coreapi.Field("status", required=True, location="form",
                                schema=coreschema.Object(required=True, description="Status")),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields
