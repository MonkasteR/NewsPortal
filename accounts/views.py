from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .forms import CustomSignupForm


class SignUp(CreateView):
    model = User
    form_class = CustomSignupForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'


@login_required
def test_page(request):
    user_permissions = request.user.get_all_permissions()
    permission_names = list(user_permissions)

    return HttpResponse(f"Ваши текущие разрешения: <br/> {'<br/>'.join(permission_names)}")
