from datetime import datetime


def get_time(request):
    return {'date': datetime.now()}
