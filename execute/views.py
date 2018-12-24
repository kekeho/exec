from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
import os
import re

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUFFER_ROOT = os.path.join(APP_ROOT, 'execute/buffers')


def script_validator(script: str):
    # FUCK YOU HACKING CODE
    black_list = ['subprocess', 'sys', 'os', 'exec']
    errors = [module for module in black_list if re.findall('[^\'\";.]'+module, script)]
    if len(errors) != 0:
        raise TypeError('Can\'t exec!')

    return script


class MethodNotAllowed(HttpResponse):
    status_code = 505


class Script():
    def __init__(self, script: str):
        script = script_validator(script)

        request_uuid = uuid.uuid4()
        self.buffer_filename = BUFFER_ROOT + '/' + str(request_uuid) + '.buf'
        header = f"""__all__ = ['sys']
import sys
buffer = open('{self.buffer_filename}', 'w')
sys.stdout = buffer
"""
        footer = f"""
buffer.close()
"""
        self.script = header + script + footer
        self.result = None

    def execute(self):
        exec(self.script)
        with open(self.buffer_filename) as buffer:
            self.result = buffer.read()
        os.remove(self.buffer_filename)


def execute_front(request):
    # raise 505
    if request.method != 'GET':
        return MethodNotAllowed('<h1>505 METHOD NOT ALLOWED</h1>')

    return render(request, 'execute_front.html')


@csrf_exempt
def execute_string(request):
    # raise 505
    if request.method != 'POST':
        return MethodNotAllowed('<h1>505 METHOD NOT ALLOWED</h1>')

    script = Script(request.POST['script'])
    script.execute()

    return HttpResponse(script.result)
