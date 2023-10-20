from courses.models import Course
from django import forms


class CourseEnrollForm(forms.Form):
    """Used for enrolling students for a course"""

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), widget=forms.HiddenInput
    )
