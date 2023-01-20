from django.db import models

# Create your models here.


class Registration(models.Model):
    name=models.CharField(max_length=100)
    house=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.EmailField()
    status=models.IntegerField(default=1)


class Technician(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.EmailField()
    qualification=models.CharField(max_length=100)
    status=models.IntegerField(default=1)



class Request(models.Model):
    uid=models.ForeignKey(Registration,on_delete=models.CASCADE)
    date=models.DateField(null=True,auto_now=True)
    vtype=models.CharField(max_length=100,null=True,blank=True)
    vname=models.CharField(max_length=100,null=True,blank=True)
    desc=models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=100,null=True,blank=True)



class Schedule(models.Model):
    rid=models.ForeignKey(Request,on_delete=models.CASCADE)
    sid=models.ForeignKey(Technician,on_delete=models.CASCADE)
    sdate=models.DateField(null=True)
    edate=models.DateField(null=True)
    amount=models.CharField(null=True,max_length=100)
    desc=models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=100,null=True,blank=True)


class Feedback(models.Model):
    sid=models.ForeignKey(Schedule,on_delete=models.CASCADE,default="")
    feed=models.CharField(max_length=100,null=True,blank=True)