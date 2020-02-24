import logging
from django.http import Http404
from rest_framework.views import exception_handler, set_rollback
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.response import Response


logger = logging.getLogger(__name__)


def get_full_name(obj):
    """
    Helper function to get fully qualified class name of an object
    """
    # o.__module__ + "." + o.__class__.__qualname__ is an example in
    # this context of H.L. Mencken's "neat, plausible, and wrong."
    # Python makes no guarantees as to whether the __module__ special
    # attribute is defined, so we take a more circumspect approach.
    # Alas, the module name is explicitly excluded from __qualname__
    # in Python 3.

    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__  # Avoid reporting __builtin__
    else:
        return module + '.' + obj.__class__.__name__


def custom_exception_handler(exc, context):
    """
    There are basically 2 type of exceptions when using Django Rest Framework:
    - APIException and derivatives
    - Generic exceptions: from django and system
    """
    errors = []
    headers = {}

    if isinstance(exc, APIException):
        
        # --- copy from exception_handler ---
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait
        # --- end copy ---

        if isinstance(exc, ValidationError):
            """
            exc.detail format:
            {
                <field_name> : [ List of ErrorDetail ]
            }
            """
            for field in exc.detail:
                for validation_error in exc.detail[field]:
                    errors.append({
                        "code": f"{field}_{validation_error.code}",
                        "message": str(validation_error)
                    })
        else:   # Maybe one of 2 types: list or dict
            if isinstance(exc.detail, list):
                logger.exception(exc)   # TODO: log for further expandsion
            elif isinstance(exc.detail, dict):
                logger.exception(exc)   # TODO: log for further expandsion
            else:
                errors.append({
                    "code": exc.detail.code,
                    "message": exc.detail.detail,
                })
        
        set_rollback()
    else:
        # Not APIException, ie: django.http.response.Http404
        # Then there will be no code but optionally include message
        errors.append({
            "code": get_full_name(exc),
            "message": str(exc) or get_full_name(exc)   # In case str(exc) return empty string
        })

    return Response({
            "errors": errors
        },
        status=exc.status_code if hasattr(exc, 'status_code') else 500,
        headers=headers
    )