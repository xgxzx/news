from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

from allauth.account.forms import SignupForm
from django.core.mail import send_mail, EmailMultiAlternatives


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

#  Добавление в группу при регистрации
# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         print('1')
#         user = super().save(request)
#         print('2')
#         test = Group.objects.get(name="test")
#         user.groups.add(test)
#         print('3')
#         return user


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        subject = 'Добро пожаловать в наш интернет-магазин!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/products">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        # send_mail(
        #     subject='Добро пожаловать!',
        #     message=f'{user.username}, вы успешно зарегистрировались!',
        #     from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
        #     recipient_list=[user.email],
        # )
        return user
