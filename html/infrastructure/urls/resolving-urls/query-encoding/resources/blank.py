def main(request, response):
    return [("Content-Type", "text/html; charset={0!s}".format((request.GET['encoding'])))], ""
