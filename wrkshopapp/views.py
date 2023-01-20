from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date,datetime

# Create your views here.


def home(request):
    return render(request,"index.html")



def adminhome(request):
    """ 
        The function to load index page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    return render(request, 'adminhome.html')

def userhome(request):
    """ 
        The function to load user page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    name=request.session["name"]

    return render(request, 'userhome.html',{'name':name})

def techhome(request):
    """ 
        The function to load index page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """

    name=request.session["name"]

    return render(request, 'techhome.html',{'name':name})


def reglog(request):
    """ 
        The function to load index page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    if request.POST:
        # read the username and password given in UI
        email = request.POST['txtEmail']
        pwd = request.POST['txtPassword']
        # checking whether the client is admin

        # checking whether username and email exist in authenticate table
        user = authenticate(username=email, password=pwd)
        if user is None:
            #username or password is incorrect
            messages.info(request, 'Username or password incorrect')
        else:
            #username and password is correct
            user_data = User.objects.get(username=email)
            if user_data.is_superuser == 1:
                # if admin, goto admin interface
                if email == "admin@gmail.com":
                    return redirect("/adminhome")
                else:
                    messages.info(request, 'Something went Wrong')
                    return redirect("/reglog")
                # if user, go to user interface
            else:
                    if user_data.is_staff == 0:
                        r = Registration.objects.get(email=email)
                        request.session["id"] = r.id
                        request.session["name"] = r.name
                        return redirect("/userhome")
                    elif user_data.is_staff == 1:
                        r = Technician.objects.get(email=email)
                        request.session["id"] = r.id
                        request.session["name"] = r.name
                        return redirect("/techhome")
 
                    else:
                        messages.info(request, 'Something went Wrong')
                        return redirect("/reglog")
    return render(request, 'reglog.html')

def registration(request):
    """ 
        The function to load registration page of the project. 
        -------------------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    if request.POST:
        # read the values from UI
        name = request.POST['txtName']
        house = request.POST['txtHouse']
        place = request.POST['txtPlace']
        phone = request.POST['txtPhone']
        email = request.POST['txtEmail']
        pwd = request.POST['txtPassword']
        # check whether any duplicate entries occur
        user = authenticate(username=email, password=pwd)
        if user is None:
            # if no duplicate entries add the data to registration table
            try:
                r = Registration.objects.create(
                    name=name,house=house, place=place, phone=phone, email=email)
                r.save()
            except:
                messages.info(request, 'Sorry some error occured')
            else:
                # add the data to login table also

                try:
                    u = User.objects.create_user(
                        password=pwd, username=email, is_superuser=0, is_active=1, email=email)
                    u.save()
                except:
                    messages.info(request, 'Sorry some error occured')
                else:
                    messages.info(request, 'Registration successfull')
        else:
            # duplicate entries occur and registration is not possible
            messages.info(request, 'User already registered')
    return render(request, 'registration.html')


def adminstaff(request):
    """ 
        The function to add staff. 
        -------------------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    if request.POST:
        # read the values from UI
        name = request.POST['txtName']
        address = request.POST['txtAddress']
        phone = request.POST['txtContact']
        qual = request.POST['txtQualification']
        email = request.POST['txtEmail']
        pwd = request.POST['txtPassword']
        # check whether any duplicate entries occur
        user = authenticate(username=email, password=pwd)
        if user is None:
            # if no duplicate entries add the data to registration table
            
            try:
                r = Technician.objects.create(
                   name=name, address=address, phone=phone, email=email, qualification=qual)
                r.save()
            except:
                print("h1")
                messages.info(request, 'Sorry some error occured')
            else:
                # add the data to login table also
                try:
                    u = User.objects.create_user(
                        password=pwd, username=email, is_superuser=0, is_active=1, is_staff=1, email=email)
                    u.save()
                except:
                    print("h2")
                    messages.info(request, 'Sorry some error occured')
                else:
                    messages.info(request, 'Registration successfull')
        else:
            # duplicate entries occur and registration is not possible
            messages.info(request, 'User already registered')
    # fetch and load all therapist from database
    staff_data = Technician.objects.filter(status=1)
    return render(request, 'adminstaff.html', {"staff": staff_data})


def adminupdatestaff(request):
    """ 
        The function to update staff. 
        -------------------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    sid = request.GET.get('id')
    staff_data = Technician.objects.filter(id=sid)
    if request.POST:
        # read the values from UI
        name = request.POST['txtName']
        address = request.POST['txtAddress']
        phone = request.POST['txtContact']
        qual = request.POST['txtQualification']
        try:
            staff_data.update(
                name=name, address=address, phone=phone, qualification=qual)
        except:
            messages.info(request, 'Sorry some error occured')
        else:
            messages.info(request, 'Updation successfull')
            return redirect("/adminstaff")
    return render(request, 'adminupdatestaff.html', {"staff": staff_data})



def admindeletestaff(request):
    """ 
        The function to delete staff. 
        -------------------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    sid = request.GET.get('id')
    user_data = User.objects.filter(username=sid)
    user_data.update(is_active=False)
    staff_data = Technician.objects.filter(email=sid)
    staff_data.update(status=0)
    return redirect('/adminstaff')

def addfeedback(request):
    """ 
        The function to load user feedback page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    id=request.GET.get('id')
    sch=Schedule.objects.get(id=id)
    if request.POST:
        feed=request.POST['feed']
        f=Feedback.objects.create(sid=sch,feed=feed)
        f.save()
        messages.info(request,"Added feedback Successfully") 
        return redirect("/viewuserrequests")   
    return render(request, 'addfeedback.html')


def viewfeedback(request):
    """ 
        The function to load user feedback page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    feed=Feedback.objects.all().order_by('-id')
    return render(request, 'viewfeedback.html',{'feed':feed})



def addrequest(request):
    """ 
        The function to load user service book page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    rid=request.session["id"]
    uid=Registration.objects.get(id=rid)
    if request.POST:
        vtype=request.POST['vtype']
        vmodel=request.POST['vmodel']
        desc=request.POST['desc']
        b=Request.objects.create(uid=uid,vtype=vtype,vname=vmodel,desc=desc,status="requested")
        b.save()
        messages.info(request,"Request Submitted Successfully")
        return redirect("/viewuserrequests")
    return render(request, 'request.html',{'u':uid})

def viewuserrequests(request):
    """ 
        The function to load user bookings page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    uid=request.session['id']
    book=Request.objects.filter(uid=uid)
    return render(request, 'viewuserrequests.html',{'book':book})


def cancelrequest(request):
    """ 
        The function to cancel user bookings page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    sid=request.GET.get('id')
    Request.objects.filter(id=sid).update(status='cancelled')
    messages.info(request,'Cancelled Successfully')
    return redirect("/viewuserrequests")


def viewbookings(request):
    """ 
        The function to load user bookings page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    book=Request.objects.filter(status='requested')
    return render(request, 'viewbookings.html',{'book':book})


def schedulebooking(request):
    """ 
        The function to load user service book page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    id=request.GET.get("id")
    dt=date.today()
    staff=Technician.objects.all()
    data=Request.objects.get(id=id)
    if request.POST:
        st=request.POST['staff']
        dt=request.POST['dt']
        dt1 = datetime.strptime(dt,'%Y-%m-%d')
        print(dt)
        print(dt1.date())
        if (dt1.date()) < (date.today()):
            messages.info(request,"Invalid Date")
            return redirect("/viewbookings")
        tdata=Technician.objects.get(id=st)
        b=Schedule.objects.create(rid=data,sid=tdata,sdate=dt,status="scheduled")
        b.save()
        Request.objects.filter(id=id).update(status="scheduled")
        messages.info(request,"Scheduled Successfully")
        return redirect("/viewbookings")
    return render(request, 'schedulebooking.html',{'data':data,'staff':staff})



def viewtechschedules(request):
    """ 
        The function to load user bookings page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    tid=request.session["id"]
    book=Schedule.objects.filter(sid=tid).exclude(status='completed')
    return render(request, 'viewtechschedules.html',{'book':book})


def viewtechcompleted(request):
    """ 
        The function to load user bookings page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    tid=request.session["id"]
    book=Schedule.objects.filter(sid=tid,status='completed')
    return render(request, 'viewtechcompleted.html',{'book':book})


def addwrkdetails(request):
    """ 
        The function to load user service book page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    id=request.GET.get("id")
    data=Schedule.objects.get(id=id)
    v=data.sdate
    if request.POST:
        sdt=request.POST['sdt']
        edt=request.POST['edt']
        desc=request.POST['desc']
        amount=request.POST['amt']
        edt1 = datetime.strptime(edt,'%Y-%m-%d')
        print(v)
        print(edt1)
        if (edt1.date())<v:
            messages.info(request,"Date should be greater than Sheduled")
            return redirect("/viewtechschedules") 
        else:
             messages.info(request,"Date Added Successfully")
        Schedule.objects.filter(id=id).update(edate=edt,amount=amount,desc=desc,status="completed")
        Request.objects.filter(id=data.rid.id).update(status="completed")
        messages.info(request,"Work Details Added Successfully")
        return redirect("/viewtechschedules")
    return render(request,'addwrkdetails.html',{'data':data})


def viewwrkdetails(request):
    """ 
        The function to load user bookings page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    id=request.GET.get('id')
    al=Feedback.objects.all().values_list('sid',flat=True)
    Wrk=Schedule.objects.filter(rid=id)
    return render(request, 'viewwrkdetails.html',{'wrk':Wrk,'al':al})


def addpayment(request):
    """ 
        The function to load user pay bill page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 

        Returns: 
            html page
    """
    id=request.GET.get('id')
    sid=Schedule.objects.get(id=id)
    if request.POST:
        yr=request.POST['year']
        if int(yr)<=2022 or int(yr)>2030:
            messages.info(request,"invaid year")
            return redirect("/viewuserrequests")
        Schedule.objects.filter(id=id).update(status='paid')
        messages.info(request,"Paid Successfully")
        return redirect("/viewuserrequests")
    return render(request, 'addpayment.html',{'s':sid})



