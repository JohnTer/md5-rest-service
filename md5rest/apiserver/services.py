import hashlib
import requests
import logging
from django.core.mail import send_mail
import md5rest.settings as glsett
from .models import Tasks

class HashMailService():
    def __init__(self, queue):
        self.signal_queue = queue

    def _get_task(self):   
        try:
            task_inst = Tasks.objects.filter(task_status=Tasks.get_running_literal()).first()
        except:
            task_inst = None
        return task_inst

    def _hashproc(self, url):
        hsh = hashlib.md5()

        r = requests.get(url, stream=True)
        r.raise_for_status()
        for line in r.iter_lines():
            hsh.update(line)

        return hsh.hexdigest()


    def _worker(self):
        while True:
            task_inst = self._get_task()
            if task_inst is None:
                return 

            try:
                md5_res = self._hashproc(task_inst.url)
                task_inst.md5 = md5_res
                task_inst.set_status_done()
            except:
                task_inst.set_status_err()

            if glsett.MAIL_SETTINGS and task_inst.email != '' and task_inst.task_status == 'd':
                    self.send_email(task_inst.email, task_inst.url, task_inst.md5)

            task_inst.save()

    def run(self):
        while True:
            _ = self.signal_queue.get()
            self._worker()

    
    def send_email(self, email_to, task_url, task_md5):
        subject = 'md5 hash'
        message = "url: {}, md5: {}".format(task_url, task_md5)
        email_from = glsett.EMAIL_HOST_USER
        recipient_list = [email_to,]
        try:
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
        except:
            logger = logging.getLogger(__name__)
            logger.error("Send mail error")

