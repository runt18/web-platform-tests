import time
import re

def main(request, response):
    key = request.GET['id']
    action = request.GET['action']
    if action == 'put':
        # We want the raw input for 'q'
        q = re.search(r'q=([^&]+)', request.url_parts.query).groups()[0]
        request.server.stash.put(key, q)
        return [("Content-Type", "text/html")], 'Put {0!s}'.format(q)
    else:
        q = request.server.stash.take(key)
        if q is not None:
            return [("Content-Type", "text/html")], q
        return [], ""
