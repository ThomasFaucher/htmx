
from django.core.management.base import BaseCommand
from myapp.task.models import Task

class Command(BaseCommand):
    help = 'Create a new task'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str, help='Task title')
        parser.add_argument('description', type=str, help='Task description')
        parser.add_argument('--done', action='store_true', help='Mark task as done')
        parser.add_argument('--user', type=int, help='User ID')

    def handle(self, *args, **options):
        title = options['title']
        description = options['description']
        done = options['done']
        user_id = options['user']

        task = Task.objects.create(title=title, description=description, done=done, user_id=user_id)
        self.stdout.write(f'Successfully created task with ID {task.id}')
