def main(request, response):
    id = request.GET['id']
    mode = request.GET['mode']
    fallback_url = ""
    if mode == "FALLBACK":
        fallback_url = "fallback-namespace/"
    manifest = u"""CACHE MANIFEST

{0!s}:
{1!s} stash.py?q=\u00E5&id={2!s}&action=put
""".format(mode, fallback_url, id)
    return [("Content-Type", "text/cache-manifest; charset={0!s}".format(request.GET['encoding']))], manifest.encode('utf-8') # charset should be ignored for cache manifests
