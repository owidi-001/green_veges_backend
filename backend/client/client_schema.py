import coreapi
from rest_framework.schemas import AutoSchema


class ClientSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ["put", "post"]:
            extra_fields = [
                coreapi.Field("first_name", required=False, location="form"),
                coreapi.Field("last_name", required=False, location="form"),
                coreapi.Field("email", required=False, location="form"),
                coreapi.Field("phone_number", required=False, location="form"),
            ]
        if method.lower() in ["patch"]:
            extra_fields = []

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields
