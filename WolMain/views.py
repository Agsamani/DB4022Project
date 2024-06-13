from django.shortcuts import render, HttpResponse
from django.db import connection

from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request, "base.html")


def psql_test(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM normalUser')
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [
            dict(zip(columns, row))
            for row in rows
        ]
    return JsonResponse(result, safe=False)