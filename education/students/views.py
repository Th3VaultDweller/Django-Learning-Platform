from typing import Any

from courses.models import Course
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from .forms import CourseEnrollForm

# Create your views here.


class StudentRegistrationView(CreateView):
    """Used for registering students for a course"""

    # CreateView предоставляет функциональность создания модельных объектов
    # путь к шаблону, применяемому для прорисовки этого представления
    template_name = "students/student/registration.html"
    # форма для создания объектов, которая должна быть ModelForm
    form_class = UserCreationForm
    # адрес перенаправления пользователя после успешной передачи формы
    success_url = reverse_lazy("student_course_list")

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd["username"], password=cd["password1"])
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """Works with the enrolled students"""

    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data["course"]
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("student_course_detail", args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    """Used for viewing the list of courses that have students in them"""

    model = Course
    template_name = "students/course/list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = "students/course/detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # получить объект Course
        course = self.get_object()
        if "module_id" in self.kwargs:
            # взять текущий модуль
            context["module"] = course.module.get(id=self.kwargs["module_id"])
        else:
            # взять первый модуль
            context["module"] = course.modules.all()[0]
        return context
