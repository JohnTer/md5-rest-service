import time
from uuid import uuid4
from django.db import models

def get_unixtimestamp():
    return int(time.time())


class Tasks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(blank=True, default='')
    url = models.URLField()
    created_at = models.BigIntegerField(default=get_unixtimestamp, blank=True, help_text = "format: Unix timestamp")
    md5 = models.CharField(max_length=16, blank=True)

    TASK_STATUS = (
    ('n', 'not exist'),
    ('r', 'running'),
    ('d', 'done'),
    ('e', 'error'),
    )
    task_status = models.CharField(max_length=1, choices=TASK_STATUS, blank=True, default='r')

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return "{} {} {} {} {}".format(self.id, self.email, self.url, self.task_status, self.created_at)

    
    def get_id_dict(self):
        return {'id': self.id}

    def get_task_status(self):
        if self.task_status == 'd':
            return {'md5': self.md5, 'status': self.get_task_status_display(), 'url': self.url} 
        else:
            return {'status': self.get_task_status_display()}


    def set_status_done(self):
        self.task_status = 'd'

    def set_status_err(self):
        self.task_status = 'e'


    @classmethod
    def get_running_literal(cls):
        return cls.TASK_STATUS[1][0]

    
        