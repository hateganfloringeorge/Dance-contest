from django import forms

from contestapp.models import Contest
from contestapp.models import Team
from contestapp.models import Grade

CONTEST_CHOICES= [
    (0 , 'Evolutie Sincrona'),
    (1 , 'Evolutie Asincrona'),
    ]


class ContestPostModelForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = (
        'title',
        'teamCount',
        'membersPerTeam',
        'typeOfContest',
        'numberOfRounds',
        )
        widgets = {
            'typeOfContest': forms.Select(choices=CONTEST_CHOICES),
        }

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = Contest.objects.filter(title__iexact=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This contest title has already been used.\nPlease try again.")
        return title

    def clean_teamCount(self, *args, **kwargs):
        teamCount = self.cleaned_data.get('teamCount')
        if teamCount > 15:
            raise forms.ValidationError("Must be a number less than 15.\nPlease try again")
        return teamCount

    def clean_membersPerTeam(self, *args, **kwargs):
        membersPerTeam = self.cleaned_data.get('membersPerTeam')
        if membersPerTeam > 15:
            raise forms.ValidationError("Must be a number less than 15.\nPlease try again")
        return membersPerTeam

class TeamPostModelForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['teamName', 'numberOnBack']

    def clean_teamName(self, *args, **kwargs):
        instance = self.instance
        teamName = self.cleaned_data.get('teamName')
        qs = Team.objects.filter(title__iexact=teamName)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This team name has already been used.\nPlease try again.")
        return teamName