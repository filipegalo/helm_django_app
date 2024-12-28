"""
Reference: https://www.ghanei.net/django-migrations-on-kubernetes/
"""
from django.db import connections
from django.conf import settings
from django.core.management.commands.migrate import Command as MigrateCommand


DEFAULT_LOCK_ID = getattr(settings, "MIGRATE_LOCK_ID", 1000)


class Command(MigrateCommand):
    """A Django management command that runs migrations with an advisory lock.
    
    This command extends Django's built-in migrate command to add advisory locking,
    which prevents multiple instances from running migrations simultaneously.
    This is particularly useful in containerized environments like Kubernetes
    where multiple pods may attempt migrations at the same time."""

    help = "Run Django migrations safely, using a lock"

    def add_arguments(self, parser):
        MigrateCommand.add_arguments(self, parser)
        parser.add_argument(
            "--migrate-lock-id",
            default=DEFAULT_LOCK_ID,
            type=int,
            help="The id of the advisory lock to use",
        )

    def handle(self, *args, **options):
        database = options["database"]
        if not options["skip_checks"]:
            self.check(databases=[database])

        # Get the database we're operating from
        connection = connections[database]
        # Hook for backends needing any database preparation
        connection.prepare_database()

        lock_id = options["migrate_lock_id"]
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"SELECT pg_advisory_lock({lock_id})")
                MigrateCommand.handle(self, *args, **options)
            finally:
                cursor.execute(f"SELECT pg_advisory_unlock({lock_id})")
