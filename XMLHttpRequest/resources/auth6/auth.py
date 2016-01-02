def main(request, response):
    if request.auth.username == 'usr' and request.auth.password == 'secret':
        response.headers.set('Content-type', 'text/plain')
        content = ""
    else:
        response.status = 401
        response.headers.set('Status', '401 Authorization required')
        response.headers.set('WWW-Authenticate', 'Basic realm="test"')
        content = 'User name/password wrong or not given: '

    content += "{0!s}\n{1!s}".format(request.auth.username,
                           request.auth.password)
    return content
