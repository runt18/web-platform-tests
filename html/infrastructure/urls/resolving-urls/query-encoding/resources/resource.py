import os
import re

def main(request, response):
    type = request.GET['type']
    encoding = request.GET['encoding']
    # We want the raw input for 'q'
    q = re.search(r'q=([^&]+)', request.url_parts.query).groups()[0]
    if type == 'html':
        return [("Content-Type", "text/html; charset=utf-8")], q
    elif type == 'css':
        return [("Content-Type", "text/css; charset=utf-8")], "#test::before {{ content:'{0!s}' }}".format(q)
    elif type == 'js':
        return [("Content-Type", "text/javascript; charset=utf-8")], "{0!s} = '{1!s}';".format(request.GET['var'], q)
    elif type == 'worker':
        return [("Content-Type", "text/javascript")], "postMessage('{0!s}'); close();".format(q)
    elif type == 'sharedworker':
        return [("Content-Type", "text/javascript")], "onconnect = function(e) {{ e.source.postMessage('{0!s}'); close(); }};".format(q)
    elif type == 'worker_importScripts':
        return ([("Content-Type", "text/javascript; charset={0!s}".format(encoding))], # charset should be ignored for workers
                """try {{
                     var x = 'importScripts failed to run';
                     importScripts('?q=\\u00E5&type=js&var=x&encoding={0!s}');
                     postMessage(x);
                     close();
                   }} catch(ex) {{
                     postMessage(String(ex));
                   }}""".format(encoding))
    elif type == 'worker_worker':
        return ([("Content-Type", "text/javascript; charset={0!s}".format(encoding))], # charset should be ignored for workers
                """try {{
                     var worker = new Worker('?q=\\u00E5&type=worker&encoding={0!s}');
                     worker.onmessage = function(e) {{
                       postMessage(e.data);
                       close();
                     }};
                   }} catch(ex) {{
                     postMessage(String(ex));
                   }}""".format(encoding))
    elif type =='worker_sharedworker':
        return ([("Content-Type", "text/javascript; charset={0!s}".format(encoding))], # charset should be ignored for workers
                """try {{
                   var worker = new SharedWorker('?q=\\u00E5&type=sharedworker&encoding={0!s}');
                     worker.port.onmessage = function(e) {{
                       postMessage(e.data);
                       close();
                     }};
                   }} catch(ex) {{
                     postMessage(String(ex));
                   }}""".format(encoding))
    elif type == 'sharedworker_importScripts':
        return ([("Content-Type", "text/javascript; charset={0!s}".format(request.GET['encoding']))], # charset should be ignored for workers
                """onconnect = function(e) {{
                     var connect_port = e.source;
                     try {{
                       var x = 'importScripts failed to run';
                       importScripts('?q=\\u00E5&type=js&var=x&encoding={0!s}');
                       connect_port.postMessage(x);
                       close();
                     }} catch(ex) {{
                       connect_port.postMessage(String(ex));
                     }}
                   }};""".format(encoding))
    elif type == 'sharedworker_worker':
        return ([("Content-Type", "text/javascript; charset={0!s}".format(encoding))], # charset should be ignored for workers
                """onconnect = function(e) {{
                     var connect_port = e.source;
                     try {{
                       var worker = new Worker('?q=\\u00E5&type=worker&encoding={0!s}');
                       worker.onmessage = function(e) {{
                         connect_port.postMessage(e.data);
                         close();
                       }};
                     }} catch(ex) {{
                       connect_port.postMessage(String(ex));
                     }}
                   }};""".format(encoding))
    elif type == 'sharedworker_sharedworker':
        return ([("Content-Type", "text/javascript; charset={0!s}".format(encoding))], # charset should be ignored for workers
                """onconnect = function(e) {{
                     var connect_port = e.source;
                     try {{
                       onerror = function(msg) {{
                         connect_port.postMessage(msg);
                         close();
                         return false;
                       }};
                       var worker = new SharedWorker('?q=\\u00E5&type=sharedworker&encoding={0!s}');
                       worker.port.onmessage = function(e) {{
                         connect_port.postMessage(e.data);
                         close();
                       }};
                     }} catch(ex) {{
                       connect_port.postMessage(String(ex));
                     }}
                   }};""".format(encoding))
    elif type == 'eventstream':
        return [("Content-Type", "text/event-stream")], "data: {0!s}\n\n".format(q)
    elif type == 'svg':
        return [("Content-Type", "image/svg+xml")], "<svg xmlns='http://www.w3.org/2000/svg'>{0!s}</svg>".format(q)
    elif type == 'xmlstylesheet_css':
        return ([("Content-Type", "application/xhtml+xml; charset={0!s}".format(encoding))],
                (u"""<?xml-stylesheet href="?q=&#x00E5;&amp;type=css&amp;encoding={0!s}"?><html xmlns="http://www.w3.org/1999/xhtml"/>""".format(encoding))
                .encode(encoding))
    elif type == 'png':
        if q == '%E5':
            image = 'green-1x1.png'
        elif q == '%C3%A5':
            image = 'green-2x2.png'
        elif q == '%3F':
            image = 'green-16x16.png'
        else:
            image = 'green-256x256.png'
        rv = open(os.path.join(request.doc_root, "images", image)).read()
        return [("Content-Type", "image/png")], rv
    elif type == 'video':
        ext = request.GET['ext']
        if q == '%E5':
            video = 'A4' # duration: 3
        elif q == '%C3%A5':
            video = 'movie_5' # duration: 5
        elif q == '%3F':
            video = 'green-at-15' # duration: 30
        else:
            video = 'movie_300' # duration: 300
        rv = open(os.path.join(request.doc_root, "media", "{0!s}.{1!s}".format(video, ext))).read()
        if ext == 'ogv':
            ext = 'ogg'
        return [("Content-Type", "video/{0!s}".format(ext))], rv
    elif type == 'webvtt':
        return [("Content-Type", "text/vtt")], "WEBVTT\n\n00:00:00.000 --> 00:00:01.000\n{0!s}".format(q)
