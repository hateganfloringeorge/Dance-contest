from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory, BaseInlineFormSet
from .forms import ContestPostModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import logout


from contestapp.models import (
        Contest,
        Team,
        Category,
        Grade,
        Member,
        Round,
    )


# Contest ===================================================================


@login_required(login_url='admin/login/?next=/')
def contest_post_list_view(request):
    qs = Contest.objects.all()
    template_name    = 'contest/list.html'
    context         = {'object_list': qs}
    return render(request, template_name, context)


@login_required(login_url='admin/login/?next=/')
def contest_post_create_view(request):
    form = ContestPostModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("/")
    template_name    = 'contest/form.html'
    context         = {'form': form}
    return render(request, template_name, context)


@login_required(login_url='admin/login/?next=/')
def contest_post_detail_view(request, slug):
    obj = get_object_or_404(Contest, slug=slug)
    template_name    = 'contest/details.html'
    context         = {'object': obj}
    return render(request, template_name, context)


@login_required(login_url='admin/login/?next=/')
def contest_post_update_view(request, slug):
    obj = get_object_or_404(Contest, slug=slug)
    form = ContestPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name    = 'contest/update.html'
    context         = {'form': form, 'object': obj}
    return render(request, template_name, context)


@login_required(login_url='admin/login/?next=/')
def contest_post_delete_view(request, slug):
    obj = get_object_or_404(Contest, slug=slug)
    template_name       = 'contest/delete.html'
    context             = {'object': obj}
    if request.method == "POST":
        obj.delete()
        return redirect("/")
    return render(request, template_name, context)


@login_required(login_url='admin/login/?next=/')
def contest_start_view(request, slug):
    obj = get_object_or_404(Contest, slug=slug)
    template_name   = 'contest/start.html'
    context         = {'object': obj}

    if request.method == "POST":
        # TODO check if data was posted
        obj.isStarted   = True
        obj.canVote     = True
        obj.save()
        for i in range(obj.numberOfRounds):
            rnd         = Round()
            rnd.number  = i + 1
            rnd.contest = obj
            rnd.save()
        addGradeNextRound(slug)
        return redirect(obj.get_absolute_url())

    return render(request, template_name, context)


# Category  =================================================================


@login_required(login_url='admin/login/?next=/')
def category_crud_post_view(request, slug):
    obj                 = get_object_or_404(Contest, slug=slug)
    template_name        = 'category/crud.html'
    CategoryFormset        = inlineformset_factory(Contest, Category, 
                                                    fields=('name', 'percent'), 
                                                    formset=CategoryInlineFormSet, 
                                                    can_delete=True, 
                                                    extra=3, 
                                                    max_num=15,
                                                    # //TODO widget,labels
                                                    widgets={'categoryName': forms.Select(attrs={'disabled':'true'})}
                                                    )
    
    validation_error = []
    if request.method == 'POST':
        formset = CategoryFormset(request.POST, instance=obj)
        if formset.is_valid():
            formset.save()
            return redirect(category_crud_post_view, slug=slug)
        else:
            validation_error = formset._non_form_errors.as_data()
            print(validation_error[0])
    
    formset             = CategoryFormset(instance=obj)
    context             = {'formset': formset, 'validation_error': validation_error}

    return render(request, template_name, context)


@login_required(login_url='admin/login/?next=/')
def category_post_list_view(request, slug):
    qs = Category.objects.filter(contest__slug=slug)
    template_name    = 'category/list.html'
    context         = {'object_list': qs}
    return render(request, template_name, context)


class CategoryInlineFormSet(BaseInlineFormSet):
    def clean(self, *args, **kwargs):
        super(CategoryInlineFormSet, self).clean()
        total = 0
        i = 0
        for form in self.forms:
            if not form.is_valid():
                continue
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                # print("=============================" + str(i))
                print(form.cleaned_data)
                if form.cleaned_data.get('percent') > 100:
                    raise forms.ValidationError("Value(s) over 100")
                else:
                    # form.instance.is_correct = True
                    total += form.cleaned_data['percent']
            # print("=============================" + str(i))
            i += 1
        if total != 100:
            raise forms.ValidationError("Ai luat meditaii de la Viorica?!?!")
        # return self.cleaned_data



# Team ======================================================================


@login_required(login_url='admin/login/?next=/')
def team_list_post_view(request, slug):
    qs = Team.objects.filter(contest__slug=slug)
    template_name    = 'team/list.html'
    context         = {'object_list': qs}
    return render(request, template_name, context)


@login_required(login_url='admin/login/?next=/')
def team_crud_post_view(request, slug):
    obj                 = get_object_or_404(Contest, slug=slug)
    template_name        = 'team/crud.html'
    if (obj.isStarted):
        TeamFormset            = inlineformset_factory(Contest, Team, 
                                                        fields=('teamName', 'numberOnBack', 'isDisqualified', 'isStillCompeting'), 
                                                        can_delete=True, 
                                                        extra=1, 
                                                        max_num=obj.teamCount, 
                                                        # //TODO widget,labels
                                                        )
    else:
        TeamFormset            = inlineformset_factory(Contest, Team, 
                                                        fields=('teamName', 'numberOnBack'), 
                                                        can_delete=True, 
                                                        extra=1, 
                                                        max_num=obj.teamCount, 
                                                        # //TODO widget,labels
                                                        )

    if request.method == 'POST':
        formset = TeamFormset(request.POST, instance=obj)
        if formset.is_valid():
            formset.save()
            return redirect(team_crud_post_view, slug=slug)
    formset         = TeamFormset(instance=obj)
    context         = {'formset': formset, 'object': obj}
    return render(request, template_name, context)


@login_required(login_url='admin/login/?next=/')
def team_post_detail_view(request, slug, pk):
    obj = get_object_or_404(Team, contest__slug=slug, pk=pk)
    template_name    = 'team/details.html'
    context         = {'object': obj}
    return render(request, template_name, context)


@login_required(login_url='admin/login/?next=/')
def team_post_delete_view(request, slug, pk):
    obj = get_object_or_404(Contest, contest__slug=slug, pk=pk)
    template_name    = 'team/delete.html'
    context         = {'object': obj}
    if request.method == "POST":
        obj.delete()
        return redirect("/")
    return render(request, template_name, context)

# Grade =====================================================================

@login_required(login_url='admin/login/?next=/')
def grade_crud_view(request, slug, no, pk):
    obj                 = get_object_or_404(Team, pk=pk)
    template_name       = 'grade/crud.html'
    GradeFormset        = inlineformset_factory(Team, Grade, 
                                                fields=('categoryName', 'grade', 'bonus'), 
                                                can_delete=False, 
                                                extra=0,
                                                labels={
                                                        'categoryName': 'Category',
                                                        'grade': 'Grade',
                                                        'bonus': 'Bonus',
                                                  },
                                                # help_texts={
                                                #         'categoryName': None,
                                                #         'grade': 'Rate it',
                                                #         'bonus': 'Add it',
                                                # },
                                                widgets={'categoryName': forms.Select(attrs={'readonly':'true'}),
                                                         'bonus': forms.NumberInput(attrs={'required':'false'})
                                                        }
                                                )
    
    if request.method == 'POST':
        formset = GradeFormset(request.POST, instance=obj)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.postedBy = request.user
                instance.save()
            return redirect(grade_crud_view, slug=slug, no=no, pk=pk)
        else:
            print('Nu a trecut validarea!')
            print(formset.errors) 
            print(formset._non_form_errors.as_data())
    formset         = GradeFormset(instance=obj)
    context         = {'formset': formset}
    return render(request, template_name, context)


@login_required(login_url='admin/login/?next=/')
def grade_round_list_view(request, slug, no):
    qs = Grade.objects.filter(teamName__contest__slug=slug).filter(roundNumber=no)
    team_qs = Team.objects.filter(contest__slug=slug)
    grades = []
    for team in team_qs:
        grades.append(qs.filter(teamName__pk=team.pk))
    template_name    = 'grade/round_list.html'
    context         = {'object_list': grades, 'round': no}
    return render(request, template_name, context)

# @login_required(login_url='admin/login/?next=/')
# def grade_crud_view(request, slug, pk, c_pk):
#     obj                 = get_object_or_404(Category, pk=c_pk)
#     template_name        = 'grade/crud.html'
#     GradeFormset        = inlineformset_factory(Category, Grade, fields=('grade','comment','bonus'),can_delete=True, max_num=1)
    
#     if request.method == 'POST':
#         formset = GradeFormset(request.POST, instance=obj)
#         if formset.is_valid():
#             instances = formset.save(commit=False)
#             for instance in instances:
#                 instance.postedBy = request.user
#                 instance.save()
#             return redirect(grade_crud_view, slug=slug, pk=pk, c_pk=c_pk)
#     formset         = GradeFormset(instance=obj)
#     context         = {'formset': formset}
#     return render(request, template_name, context)


# Member ====================================================================


@login_required(login_url='admin/login/?next=/')
def member_crud_view(request, slug, pk):
    obj                  = get_object_or_404(Team, pk=pk)
    template_name        = 'member/crud.html'
    MemberFormset        = inlineformset_factory(Team, Member, 
                                                fields=('officialSurname','officialName','stageName','age',), 
                                                can_delete=True, extra=1, max_num=obj.contest.membersPerTeam
                                                # //TODO widget,labels
                                                )
    
    if request.method == 'POST':
        formset = MemberFormset(request.POST, instance=obj)
        if formset.is_valid():
            formset.save()
            return redirect(member_crud_view, slug=slug, pk=pk)

    formset             = MemberFormset(instance=obj)
    context             = {'formset': formset}
    return render(request, template_name, context)


@login_required(login_url='admin/login/?next=/')
def member_list_view(request, slug, pk):
    qs = Member.objects.filter(team__pk=pk)
    template_name    = 'member/list.html'
    context         = {'object_list': qs, 'pk':pk}
    return render(request, template_name, context)


# Round =================================================================================================


@login_required(login_url='admin/login/?next=/')
def round_list_view(request, slug):
    qs = Round.objects.filter(contest__slug=slug)
    template_name    = 'round/list.html'
    context         = {'object_list': qs}
    return render(request, template_name, context)


@login_required(login_url='admin/login/?next=/')
def round_detail_view(request, slug, no):
    qs = Team.objects.filter(contest__slug=slug)
    template_name    = 'round/team_list.html'
    context         = {'object_list': qs, 'round': no}
    return render(request, template_name, context)


# Extra =================================================================================================


def addGradeNextRound(slug):
    contest     = get_object_or_404(Contest, slug=slug)
    contest.currentRound  += 1
    contest.save()

    team_qs     = contest.teams.filter(isDisqualified=False, isStillCompeting=True)
    category_qs = contest.categories.all()
    roundNr     = contest.currentRound
    
    for team in team_qs:
        for categ in category_qs:
            grade               = Grade()
            grade.roundNumber   = roundNr
            grade.teamName      = team
            grade.categoryName  = categ
            grade.save()


@login_required(login_url='admin/login/?next=/')
def elimination_button(request, slug):
    contest     = get_object_or_404(Contest, slug=slug)
    team_qs     = Team.objects.filter(contest__slug=slug).filter(isStillCompeting=True).filter(isDisqualified=False)
    print(team_qs)
    v = {}
    for team in team_qs:
        v[team.pk] = 0
        grade_qs = Grade.objects.filter(teamName__pk=team.pk).filter(teamName__contest__slug=slug).filter(roundNumber=contest.currentRound)
        for grade in grade_qs:
            print(team.teamName + ' ' +  str(grade.grade) + ' ' + grade.categoryName.name + ' %' + str(grade.categoryName.percent))
            v[team.pk] += grade.grade * grade.categoryName.percent
            v[team.pk] += grade.bonus
    
    answer =  []
    answer.append(team_qs.first())
    minim  = v[answer[0].pk]
    print(minim)
    for team in team_qs:
        print(team.teamName + ' ' + str(v[team.pk]))
        if v[team.pk] < minim:
            answer.clear()
            answer.append(team)
            minim = v[team.pk]
        elif v[team.pk] == minim:
            answer.append(team)

    answer = list(set(answer))
    if (len(answer) == 1):
        answer[0].isStillCompeting = False
        answer[0].save()
        print('Elimin pe cineva!!!!!')
    print('Loser' + str(answer))

    addGradeNextRound(slug)

    template_name    = 'contest/details.html'
    context          = {'object': contest, 'answer': answer}
    return redirect(contest.get_absolute_url())


@login_required(login_url='admin/login/?next=/')
def winner_button(request, slug):
    contest     = get_object_or_404(Contest, slug=slug)
    team_qs     = Team.objects.filter(contest__slug=slug).filter(isStillCompeting=True).filter(isDisqualified=False)
    print(team_qs)
    v = {}
    for team in team_qs:
        v[team.pk] = 0
        grade_qs = Grade.objects.filter(teamName__pk=team.pk).filter(teamName__contest__slug=slug).filter(roundNumber=contest.currentRound)
        for grade in grade_qs:
            print(team.teamName + ' ' +  str(grade.grade) + ' ' + grade.categoryName.name + ' %' + str(grade.categoryName.percent))
            v[team.pk] += grade.grade * grade.categoryName.percent
            v[team.pk] += grade.bonus
    
    answer =  []
    answer.append(team_qs.first())
    maxim  = v[answer[0].pk]
    print(maxim)
    for team in team_qs:
        if v[team.pk] > maxim:
            answer.clear()
            answer.append(team)
            maxim = v[team.pk]
        elif v[team.pk] == maxim:
            answer.append(team)

    answer = list(set(answer))
    if (len(answer) == 1):
        winner = answer[0]
    else:
        winner = answer

    print('Winner' + str(answer))
    template_name    = 'rezultat.html'
    context          = {'object': contest, 'winner': winner}
    return render(request, template_name, context)

# @login_required(login_url='admin/login/?next=/')
# def magic_button(request, slug):
#     team_qs    = Team.objects.filter(contest__slug=slug)
#     v = {}
#     for team in team_qs:
#         v[team.pk] = 0
#         grade_qs = Grade.objects.filter(teamName__pk=team.pk).filter(teamName__contest__slug=slug)
#         for gradez in grade_qs:
#             v[team.pk] += gradez.bonus
#             v[team.pk] += gradez.grade
#     maxim = 0
#     answer = team_qs.first()
#     for team in team_qs:
#         if team.isStillCompeting and not team.isDisqualified:
#                  if v[team.pk] > maxim:
#                     answer = team
#                     maxim = v[team.pk]
#     winners = Member.objects.filter(team__pk=answer.pk)
#     template_name   = 'rezultat.html'
#     context         = {'object': answer, 'winners': winners, 'score' : maxim}
#     return render(request, template_name, context)

@login_required(login_url='admin/login/?next=/')
def logout_request(request):
    logout(request)
    return redirect("/")