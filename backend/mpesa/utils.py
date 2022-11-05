# data=b'{"Body":{"stkCallback":{"MerchantRequestID":"12893-73412461-1",' \
#      b'"CheckoutRequestID":"ws_CO_10102022003746936791381653","ResultCode":0,"ResultDesc":"The service request is ' \
#      b'processed successfully.","CallbackMetadata":{"Item":[{"Name":"Amount","Value":1.00},' \
#      b'{"Name":"MpesaReceiptNumber","Value":"QJA9L7X0XZ"},{"Name":"Balance"},{"Name":"TransactionDate",' \
#      b'"Value":20221010003800},{"Name":"PhoneNumber","Value":254791381653}]}}}} '


def format_response(data):
    meta_data = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
    key_value_pair = {}
    for i in meta_data:
        name = i.get("Name")
        value = i.get("Value")

        if name not in key_value_pair.keys():
            key_value_pair[name] = value

    return key_value_pair


def validate_phone(phone):
    if phone.startswith("254"):
        return phone
    if phone.startswith("07") or phone.startswith("01"):
        new_number = phone.replace("0", "254", 1)
        return new_number
    if phone.startswith("+254"):
        new_number = phone[1:]
        return new_number

    return None


def reformat_phone(phone):
    if phone.startswith("254"):
        new_phone = phone.replace("254", "07", 1)
        return new_phone

    return phone
