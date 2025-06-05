# utils.py

from rest_framework.response import Response
from rest_framework import status
import traceback

def try_except_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("Exception caught in try_except_wrapper:")
            traceback.print_exc()
            return Response({
                'error': 'An internal server error occurred.',
                'exception': e.__class__.__name__
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper  


def flatten_errors(errors, prefix=''):
    flat = {}
    if isinstance(errors, dict):
        for k, v in errors.items():
            key = f"{prefix}{k}" if not prefix else f"{prefix}.{k}"
            flat.update(flatten_errors(v, key))
    elif isinstance(errors, list):
        messages = [str(e) for e in errors if not isinstance(e, (dict, list))]
        if messages:
            flat[prefix] = '; '.join(messages)
        for e in errors:
            if isinstance(e, (dict, list)):
                flat.update(flatten_errors(e, prefix))
    else:
        flat[prefix] = str(errors)
    return flat
