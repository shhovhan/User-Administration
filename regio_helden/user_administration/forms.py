from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from user_administration.models import AdminUser, CustomUser


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'iban')

    @login_required
    def custom_user_list(request, template_name='home.html'):
        custom_users = CustomUser.objects.all()
        data = {}
        data['users'] = custom_users
        return render(request, template_name, data)

    @login_required
    def custom_user_create(request, template_name='custom_user_form.html'):
        form = CustomUserForm(request.POST or None)
        if form.is_valid():
            print('ISVALID')
            form.save()
            return redirect('custom_user_list')
        return render(request, template_name, {'form': form})

    @login_required
    def custom_user_update(request, pk, template_name='custom_user_form.html'):
        custom_user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserForm(request.POST or None, instance=custom_user)
        if form.is_valid():
            form.save()
            return redirect('custom_user_list')
        return render(request, template_name, {'form': form})

    @login_required
    def custom_user_delete(request, pk,
                           template_name='custom_user_delete.html'):
        custom_user = get_object_or_404(CustomUser, pk=pk)
        if request.method == 'POST':
            custom_user.delete()
            return redirect('custom_user_list')
        return render(request, template_name, {'user': custom_user})
