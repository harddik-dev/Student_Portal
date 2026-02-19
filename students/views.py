from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Grade
from .forms import ProfileUpdateForm, PasswordChangeCustomForm

@login_required
def dashboard(request):
    student = Student.objects.get(user=request.user)
    semester = request.GET.get('semester')

    grades = None
    if semester:
        grades = Grade.objects.filter(student=student, semester=semester)

    return render(request, 'dashboard.html', {
        'student': student,
        'grades': grades,
        'selected_semester': semester
    })


@login_required
def profile_view(request):
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=student, user=request.user)
        password_form = PasswordChangeCustomForm(request.POST, user=request.user)

        if 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')

        if 'change_password' in request.POST and password_form.is_valid():
            request.user.set_password(password_form.cleaned_data['new_password'])
            request.user.save()
            messages.success(request, "Password changed successfully.")
            return redirect('login')

    else:
        profile_form = ProfileUpdateForm(instance=student, user=request.user)
        password_form = PasswordChangeCustomForm(user=request.user)

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'student': student
    })
