def main(request, response):
    id = request.GET['id']
    encoding = request.GET['encoding']
    mode = request.GET['mode']
    iframe = ""
    if mode == 'NETWORK':
        iframe = "<iframe src='stash.py?q=%C3%A5&id={0!s}&action=put'></iframe>".format(id)
    doc = """<!doctype html>
<html manifest="manifest.py?id={0!s}&encoding={1!s}&mode={2!s}">
{3!s}
""".format(id, encoding, mode, iframe)
    return [("Content-Type", "text/html; charset={0!s}".format(encoding))], doc.encode(encoding)
