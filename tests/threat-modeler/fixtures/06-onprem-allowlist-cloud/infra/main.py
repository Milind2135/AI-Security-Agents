import os

def handler(request):
    if request.headers.get("x-api-key") != os.environ["PARTNER_API_KEY"]:
        return ("forbidden", 403)
    return load_price_list(request.args.get("partner"))
