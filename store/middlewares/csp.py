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

        response["Content-Security-Policy"] = "script-src {}; style-src {};".format(script_src, style_src)

        return response
