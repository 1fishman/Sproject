# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'student'
        unique_together = (('id', 'password'),)

class Class(models.Model):
    # student = models.ManyToManyField(Student, through='Score')
    sid = models.IntegerField(db_column='Sid')  # Field name made lowercase.
    cname = models.CharField(db_column='Cname', primary_key=True, max_length=255)  # Field name made lowercase.
    cteach = models.CharField(db_column='Cteach', max_length=255, blank=True, null=True)  # Field name made lowercase.
    clast = models.CharField(db_column='Clast', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ctime = models.CharField(db_column='Ctime', max_length=255)  # Field name made lowercase.
    cadr = models.CharField(db_column='Cadr', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cday = models.CharField(db_column='Cday', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'class'
        unique_together = (('cname', 'ctime', 'cday', 'sid'),)



class Score(models.Model):
    # myclass = models.ForeignKey(Class, on_delete=models.CASCADE)
    # student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=255)
    sid = models.IntegerField(db_column='Sid')  # Field name made lowercase.
    cnum = models.CharField(db_column='Cnum', max_length=255)  # Field name made lowercase.
    cname = models.CharField(db_column='Cname', primary_key=True, max_length=255)  # Field name made lowercase.
    csore = models.CharField(db_column='Csore', max_length=255, blank=True, null=True)  # Field name made lowercase.
    credit = models.CharField(max_length=255, blank=True, null=True)
    thour = models.CharField(db_column='Thour', max_length=255, blank=True, null=True)  # Field name made lowercase.
    checkmethod = models.CharField(db_column='checkMethod', max_length=255, blank=True, null=True)  # Field name made lowercase.
    checknature = models.CharField(db_column='checkNature', max_length=255)  # Field name made lowercase.
    checkattr = models.CharField(db_column='checkAttr', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cnature = models.CharField(db_column='cNature', max_length=255, blank=True, null=True)  # Field name made lowercase.
    eclasstype = models.CharField(db_column='eClassType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    smark = models.CharField(db_column='sMark', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'score'
        unique_together = (('cname', 'cnum', 'semester', 'checknature', 'sid'),)
    def countItem(self):
        i=self.csore
        if i == '优秀':
            return float(self.credit)*95
        elif i == '良好':
            return float(self.credit)*85
        elif i == '中等':
            return float(self.credit)*75
        elif i == '及格':
            return float(self.credit)*65
        elif i == '不及格':
            return float(self.credit)*30
        else:
            return float(self.credit)*float(i)