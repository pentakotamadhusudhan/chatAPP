from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response

def returnresponse(status_code,data=None,message=None):

    response ={}
    if status_code==200:
        response['status_code'] = status_code
        response['data'] = data
        response['message'] =message
        response['hash'] = False
        return response
    elif status_code==400:
        response['status_code'] = status_code
        response['data'] = data
        response['message'] =message
        response['hash'] = False
        return response
    elif status_code==401:
        response['status_code'] = status_code
        response['data'] = data
        response['message'] =message
        response['hash'] = True
        return response
    else:
       
        response['status_code'] = 500
        response['data'] = None
        response['message'] =message
        response['hash'] = True
        return response