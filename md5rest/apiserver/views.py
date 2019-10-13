from threading import Thread
from queue import Queue

from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from .forms import CreateTaskForm, GetTaskForm
from .models import Tasks
from .services import HashMailService




@method_decorator(csrf_exempt, name='dispatch')
class TaskCreateEnv(View):
    def __init__(self, *args, **kwargs):
        super(TaskCreateEnv, self).__init__(*args, **kwargs)

        self.signal_queue = Queue()
        hashserv = HashMailService(self.signal_queue)
        thr = Thread(target=hashserv.run, daemon=True)
        thr.start()


    @csrf_exempt
    def post(self, request, *args, **kwargs):
        form = CreateTaskForm(request.GET)
        if form.is_valid():
            task_inst = Tasks(**form.cleaned_data)
            task_inst.save()
            
            self.signal_queue.put(True)
            return JsonResponse(task_inst.get_id_dict(), status = 201)
        else:
            return JsonResponse(CreateTaskForm.get_invalid_data_dict(), status=422)


class TaskCheckView(View):

    def get(self, request, *args, **kwargs):
        form = GetTaskForm(request.GET)

        if form.is_valid():
            task_inst = get_object_or_404(Tasks, pk=form.cleaned_data["id"])
            return JsonResponse(task_inst.get_task_status(), status=200)
        else:
            return JsonResponse(CreateTaskForm.get_invalid_data_dict(), status=422)



