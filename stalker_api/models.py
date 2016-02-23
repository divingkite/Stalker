from django.db import models

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    '''
    info of the people user interested in.
    '''
    name             = models.CharField(max_length=50,verbose_name="Full Name of the Person Whose handle names are stored")
    codechef_handle  = models.CharField(null=True,blank=True,max_length=20,verbose_name="Codechef handle name")
    codeforces_handle= models.CharField(null=True,blank=True,max_length=20,verbose_name="Codeforces handle name")
    owner            = models.ForeignKey( User ) 

class Contest(models.Model):
    contestId = models.IntegerField(null=True)           # used only for codeforces
    name      = models.CharField(max_length=30)          
    site      = models.CharField(max_length=20) 
    questions = models.ManyToManyField(Person, through='Question')
    
    def __str__(self):
        return self.name

class Question(models.Model):
    name    = models.CharField(max_length=20)
    link    = models.CharField(max_length=50,verbose_name="link of the question")  #used only for codechef.
    site    = models.CharField(max_length=20)
    index   = models.CharField(max_length=2)                                       #used only for codeforces.
    person  = models.ForeignKey(Person)
    contest = models.ForeignKey(Contest)

    def __str__(self):
        return self.name

class PracticeProb(models.Model):
    name   = models.CharField(max_length=20)
    index  = models.CharField(max_length=2)
    link   = models.CharField(max_length=50,verbose_name="link of the question")
    site   = models.CharField(max_length=20)
    person = models.ForeignKey(Person)
    
    def __str__(self):
        return self.name
