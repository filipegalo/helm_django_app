import os
from django.shortcuts import render
from django.db import connection
from app.settings import VERSION


def index(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT app, name, applied
            FROM django_migrations 
            ORDER BY applied DESC
        """
        )
        migrations = cursor.fetchall()

    last_migration = migrations[0] if migrations else None

    pod_ip = os.getenv("MY_POD_IP")
    pod_name = os.getenv("MY_POD_NAME")

    return render(
        request,
        "index.html",
        {
            "last_migration": last_migration,
            "migrations": migrations,
            "version": VERSION,
            "pod_ip": pod_ip,
            "pod_name": pod_name,
        },
    )
