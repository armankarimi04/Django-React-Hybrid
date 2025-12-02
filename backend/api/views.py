import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from api.models import Employee

# Create your views here.

def index(request):
    return render(request, "api/index.html")


# @method_decorator(login_required, name='dispatch')
class EmployeeView(TemplateView):
    # our hybrid template, shown above
    template_name = 'api/index.html'

    def get_context_data(self, **kwargs):
        # passing the department choices to the template in the context
        return {'department_choices': [{ 'id': c[0], 'name': c[1]} for c in Employee.DEPARTMENT_CHOICES],}
        
        
@require_POST
def login_view(request):
    data = json.loads(request.body)
    print("DATA", data)
    username = data.get('username')
    password = data.get('password')
    print("USERNAME and PASSWORD: ", username, password)
    if username is None or password is None:
        return JsonResponse({"details": "Please provide username and password"})
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"details": "Successfully logged in"})
    else:
        print("USER NOT FOUND")
        return JsonResponse({"details": "Invalid credentials"}, status=400)


def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"details": "You are not logged in"}, status=400)
    logout(request)
    return JsonResponse({"details": "Successfully logged out"})


@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isauthenticated": False})
    return JsonResponse({"isauthenticated": True})


def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isauthenticated": False})
    return JsonResponse({"username": request.user.username})