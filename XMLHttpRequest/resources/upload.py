def main(request, response):
    content = []

    for key, values in sorted(item for item in request.POST.items() if not hasattr(item[1][0], "filename")):
         content.append("{0!s}={1!s},".format(key, values[0]))
    content.append("\n")

    for key, values in sorted(item for item in request.POST.items() if hasattr(item[1][0], "filename")):
        value = values[0]
        content.append("{0!s}={1!s}:{2!s}:{3!s},".format(key,
                                         value.filename,
                                         value.headers["Content-Type"],
                                         len(value.file.read())))

    return "".join(content)
