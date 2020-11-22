from datetime import datetime
from django.shortcuts import render


def index(request):
    now = datetime.now()
    return render(
        request,
        "newyear/index.html",
        {"is_newyear": "YES" if now.month == 1 and now.day == 1 else "NO"},
    )
