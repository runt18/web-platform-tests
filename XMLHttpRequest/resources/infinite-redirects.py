def main(request, response):
    location = "{0!s}://{1!s}:{2!s}/{3!s}".format(request.url_parts.scheme,
                                  request.url_parts.netloc,
                                  request.url_parts.port,
                                  request.url_parts.path)
    page = "alternate";
    type = 302;
    mix = 0;
    if request.GET.first("page", None) == "alternate":
        page = "default"

    if request.GET.first("type", None) == "301":
        type = 301

    if request.GET.first("mix", None) == "1":
        mix = 1
        type = 302 if type == 301 else 301

    new_location = "{0!s}?page={1!s}&type={2!s}&mix={3!s}".format(location, page, type, mix)
    headers = [("Cache-Control", "no-cache"),
               ("Pragma", "no-cache"),
               ("Location", new_location)]
    return 301, headers, "Hello guest. You have been redirected to " + new_location

