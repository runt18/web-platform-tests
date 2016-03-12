from cgi import escape

def main(request, response):
    label = request.GET.first('label')
    return """<!doctype html><meta charset="{0!s}">""".format(escape(label))
