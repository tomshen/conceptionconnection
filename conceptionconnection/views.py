from django.shortcuts import render
from django.http import HttpResponse
from re import match
from datetime import date

from conceptionconnection.smbc import ConceptionConnection

def home(request):
    return render(request, 'index.html')

def conception(request):
    if request.method == 'GET':
        params = request.GET
        if 'birthdate' in params:
            if match('^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$',
                        params['birthdate']):
                birthdate = params['birthdate'].split('-')
                if int(birthdate[0]) >= date.today().year - 12:
                    return HttpResponse('You are way too young to know about this.')
            else:
                return HttpResponse('Invalid birthdate provided.')
        else:
            return HttpResponse('No birthdate provided.')
        if 'delta' in params:
            if match('^\d+$', params['delta']):
                delta = params['delta']
            else:
                delta = 5
        else:
            delta = 5
        CC = ConceptionConnection(birthdate, delta)
        if 'type' in params and params['type'] == 'html':
            return HttpResponse(CC.extractEventsHTML())
        else: # JSON by default
            return HttpResponse(CC.extractEvents())
    else:
        return HttpResponse('Request type not supported.')