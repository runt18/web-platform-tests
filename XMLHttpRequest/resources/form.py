def main(request, response):
    return "id:{0!s};value:{1!s};".format(request.POST.first("id"), request.POST.first("value"))
