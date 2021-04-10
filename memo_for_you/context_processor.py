from datetime import datetime


def get_time(request):
    """shows actual date everywhere, where context name 'date' would be used"""
    return {'date': datetime.now()}
