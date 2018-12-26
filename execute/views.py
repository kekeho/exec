from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
import os
import docker

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_ROOT = os.path.join(APP_ROOT, 'execute/scripts')
DOCKER_FILE_ROOT = os.path.join(APP_ROOT, 'execute/')


class MethodNotAllowed(HttpResponse):
    status_code = 405


class Script():
    def __init__(self, script: str):
        self.uuid = uuid.uuid4()
        self.script = script
        self.result = None

    def execute(self):
        with open(f'{SCRIPTS_ROOT}/{self.uuid}.py', 'w') as script:
            script.write(self.script)

        client = docker.from_env()
        client.images.build(path=DOCKER_FILE_ROOT, tag='exec-python:3.7', rm=True)
        try:
            self.result = client.containers.run('exec-python:3.7', str(self.uuid))
        except docker.errors.ContainerError as e:
            self.result = str(e)
        finally:
            os.remove(f'{SCRIPTS_ROOT}/{self.uuid}.py')


def execute_front(request):
    # raise 505
    if request.method != 'GET':
        return MethodNotAllowed('<h1>405 METHOD NOT ALLOWED</h1>')

    return render(request, 'execute_front.html')


@csrf_exempt
def execute_string(request):
    # raise 505
    if request.method != 'POST':
        return MethodNotAllowed('<h1>405 METHOD NOT ALLOWED</h1>')

    script = Script(request.POST['script'])
    script.execute()

    return HttpResponse(script.result)
