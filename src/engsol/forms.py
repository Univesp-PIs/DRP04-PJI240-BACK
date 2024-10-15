from django import forms
from .models import User, Link, Experience, Education, Skill

# Create your forms here
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ['user']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['user']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['user']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = ['user']