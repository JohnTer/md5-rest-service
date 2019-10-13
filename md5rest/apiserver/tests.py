from json import loads
from django.test import TestCase
from .models import Tasks

class ViewTaskCheckTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        email_done = "mail@example.com"
        url_done = "http://site.com/file.txt"
        task_ininst_done = Tasks(email = email_done, url = url_done)
        task_ininst_done.id = '6d348bf9-e572-46b3-b2d2-501ede6e8e01'
        task_ininst_done.md5 = "e10adc3949ba59abbe56e057f20f883e"
        task_ininst_done.set_status_done()


        email_done = "mail@example.com"
        url_done = "http://site.com/file.txt"
        task_ininst_running = Tasks(email = email_done, url = url_done)
        task_ininst_running.id = '6d348bf9-e572-46b3-b2d2-501ede6e8e02'
        task_ininst_running.md5 = ''
        task_ininst_running.status  = 'r'


        email_done = "mail@example.com"
        url_done = "http://site.com/file.txt"
        task_ininst_error = Tasks(email = email_done, url = url_done)
        task_ininst_error.id = '6d348bf9-e572-46b3-b2d2-501ede6e8e03'
        task_ininst_error.md5 = ''
        task_ininst_error.status  = 'e'
        task_ininst_error.set_status_err()

        task_ininst_error.save()
        task_ininst_running.save()
        task_ininst_done.save()

    
    def test_check_done(self):
        response = self.client.get('/check?id={}'.format('6d348bf9-e572-46b3-b2d2-501ede6e8e01'))
        self.assertEqual(response.status_code, 200)
        content = loads(response.content.decode('utf8').replace("'", '"'))
        

        self.assertEqual('e10adc3949ba59abbe56e057f20f883e', content['md5'])
        self.assertEqual('http://site.com/file.txt', content['url'])
        self.assertEqual('done', content['status'])

    def test_check_running(self):
        response = self.client.get('/check?id={}'.format('6d348bf9-e572-46b3-b2d2-501ede6e8e02'))
        self.assertEqual(response.status_code, 200)
        content = loads(response.content.decode('utf8').replace("'", '"'))
        
        self.assertEqual('running', content['status'])

    def test_check_error(self):
        response = self.client.get('/check?id={}'.format('6d348bf9-e572-46b3-b2d2-501ede6e8e03'))
        self.assertEqual(response.status_code, 200)
        content = loads(response.content.decode('utf8').replace("'", '"'))
        
        self.assertEqual('error', content['status'])

    def test_check_not_found(self):
        response = self.client.get('/check?id={}'.format('6d348bf9-e572-46b3-b2d2-501ede6e8e04'))
        self.assertEqual(response.status_code, 404)

    def test_check_no_id(self):
        response = self.client.get('/check')
        self.assertEqual(response.status_code, 422)

    def test_check_wrong_id(self):
        response = self.client.get('/check?id={}'.format('6d348bf9'))
        self.assertEqual(response.status_code, 422)



class ViewTaskSubmitTest(TestCase):
     
    def test_submit_ok(self):
        response = self.client.post('/submit?email={}&url={}'.format('user@example.com', 'http://127.0.0.1:5000/file.txt'))
        self.assertEqual(response.status_code, 201)
        content = loads(response.content.decode('utf8').replace("'", '"'))

        task_inst = Tasks.objects.get(pk=content['id'])
        self.assertEqual(content['id'], str(task_inst.id))

    def test_submit_ok_no_email(self):
        response = self.client.post('/submit?url={}'.format('http://127.0.0.1:5000/file.txt'))
        self.assertEqual(response.status_code, 201)
        content = loads(response.content.decode('utf8').replace("'", '"'))

        task_inst = Tasks.objects.get(pk=content['id'])
        self.assertEqual(content['id'], str(task_inst.id))

    def test_submit_fail_no_url(self):
        response = self.client.post('/submit?email={}'.format('user@example.com'))
        self.assertEqual(response.status_code, 422)

    def test_submit_fail_wrong_url(self):
        response = self.client.post('/submit?url={}'.format('ht/127.0.0.1:5000/file.txt'))
        self.assertEqual(response.status_code, 422)
        

    def test_submit_fail_wrong_email(self):
        response = self.client.post('/submit?email={}&url={}'.format('us.er@ex@ampl#e.com', 'http://127.0.0.1:5000/file.txt'))
        self.assertEqual(response.status_code, 422)

    def test_submit_no_url_param(self):
        response = self.client.post('/submit')
        self.assertEqual(response.status_code, 422)

