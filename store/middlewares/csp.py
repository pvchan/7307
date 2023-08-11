
import base64
import os
from django.utils.crypto import get_random_string


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Generate nonce
        nonce = get_random_string(32)
        request.nonce = nonce

        response = self.get_response(request)

        # Add nonce to CSP header in the response
        script_src = "'self' 'nonce-{}' https://code.jquery.com https://cdnjs.cloudflare.com https://maxcdn.bootstrapcdn.com https://checkout.stripe.com".format(nonce)
        style_src = "'self' 'nonce-{}' https://maxcdn.bootstrapcdn.com https://use.fontawesome.com https://checkout.stripe.com".format(nonce)

        # Default CSP directives
        default_src = "'self'"
        img_src = " ".join([
            "'self'",
            "https://www.freepnglogos.com",
            "https://stripe.com/",
            "https://q.stripe.com/"
        ])
        
        # Frame and font sources
        frame_src = "'self' https://checkout.stripe.com"
        font_src = "'self' https://use.fontawesome.com"

        # Report URI
        report_uri = "/csp-report/"

        # Construct the CSP header
        csp_header_value = "default-src {}; script-src {}; style-src {}; img-src {}; frame-src {}; font-src {}; report-uri {};".format(
            default_src, script_src, style_src, img_src, frame_src, font_src, report_uri)

        response["Content-Security-Policy"] = csp_header_value

        return response
