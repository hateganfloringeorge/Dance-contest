from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
# ==============================================================================================================================


class Contest(models.Model):
	title					=	models.CharField(max_length=50, unique=True)
	teamCount				=	models.PositiveIntegerField()
	membersPerTeam			=	models.PositiveIntegerField()
	typeOfContest			=	models.PositiveIntegerField(default=0)
	numberOfRounds			=	models.PositiveIntegerField(default=1)
	# TODO	numberOfSeries			=	models.PositiveIntegerField()
	# ========================= Hidden ==========================================
	slug 					=	models.SlugField(unique=True)
	canVote					=	models.BooleanField(default=False)
	isStarted				=	models.BooleanField(default=False)
	currentRound			=	models.PositiveIntegerField(default=0)
	currentSeries			=	models.PositiveIntegerField(default=0)


	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.title)
		super(Contest, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return f"/contest/{self.slug}"

	def get_edit_url(self):
		return f"/contest/{self.slug}/update"

	def get_delete_url(self):
		return f"/contest/{self.slug}/delete"


# ==============================================================================================================================


class Team(models.Model):
	teamName			=	models.CharField(max_length=40)
	numberOnBack		=	models.PositiveIntegerField()
	# TODO numberOfSeries		=	models.PositiveIntegerField()
	# ========================= Hidden ==========================================
	isDisqualified		=	models.BooleanField(default=False)
	isStillCompeting	=	models.BooleanField(default=True)
	contest 			=	models.ForeignKey('Contest', related_name='teams', on_delete=models.CASCADE)


	def get_absolute_url(self):
		return f"/contest/{self.contest.slug}/team/{self.pk}"

	def __str__(self):
		return self.teamName


# ==============================================================================================================================


class Round(models.Model):
	number				=	models.PositiveIntegerField(default=1)
	seriesNumber		= 	models.PositiveIntegerField(default=1)
	contest             =   models.ForeignKey('Contest', related_name='rounds', on_delete=models.CASCADE)
	isStarted			=	models.BooleanField(default=False)
	hasEnded			=	models.BooleanField(default=False)

	def get_absolute_url(self):
		return f"/contest/{self.contest.slug}/round/{self.number}/"

	def get_grades_url(self):
		return f"/contest/{self.contest.slug}/round/{self.number}/grades"

# ==============================================================================================================================


# # class Series(models.Model):
# # 	number				=	models.PositiveIntegerField()
# # 	startSeries			=	
# # 	endSeries			=	


# ==============================================================================================================================


class Category(models.Model):
	name 				=	models.CharField(max_length=30)
	percent				=	models.PositiveIntegerField()
	# ========================= Hidden ==========================================
	contest             =	models.ForeignKey('Contest', related_name='categories', on_delete=models.CASCADE)


	def __str__(self):
		return self.name


# ==============================================================================================================================


class Grade(models.Model):
	grade				=	models.PositiveIntegerField(default=0)
	postedBy			=	models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
	roundNumber			=	models.PositiveIntegerField(default=1)
	bonus				=	models.PositiveIntegerField(default=0)
	comment				=	models.CharField(max_length=30, default='')
	# ========================= Hidden ==========================================
	teamName 			=   models.ForeignKey('Team', related_name='teams', on_delete=models.CASCADE)
	categoryName 		=	models.ForeignKey('Category', related_name='grades', on_delete=models.CASCADE)


# ==============================================================================================================================


class Member(models.Model):
	officialSurname 	=	models.CharField(max_length=25)
	officialName 		=	models.CharField(max_length=25)
	stageName			=	models.CharField(max_length=30)
	age 				=	models.PositiveIntegerField()
	# ========================= Hidden ==========================================
	team 				=	models.ForeignKey('Team', related_name='people', on_delete=models.CASCADE)


# ==============================================================================================================================