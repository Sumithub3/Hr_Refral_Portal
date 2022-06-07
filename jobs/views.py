from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import job, post, apply, contact, profile
import csv

# Create your views here.
def home(request):
    return render(request, 'jobs/home.html')

def handleSignup(request):
    if request.method == 'POST':
        print('123')
        fname = request.POST['fname'].capitalize()
        lname = request.POST['lname'].capitalize()
        username = request.POST['username']
        referral_id = request.POST['referral']
        company = request.POST['company'].capitalize()
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myUser = User.objects.create_user(username, email, pass1)
        myUser.first_name = fname
        myUser.last_name = lname
        myUser.save()  

        profile_data = profile(user=myUser, referral_id=referral_id, company=company)   
        profile_data.save()   

        messages.success(request, 'Your account has been created successfully')
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, 'Succesfully Logged In')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials please try again')
            return redirect('home')
    else:
        return HttpResponse('404 - Not Found')       

def handleLogout(request):
    logout(request)
    messages.success(request, 'Succesfully Logged Out')
    return redirect('home')

def postJobs(request):
    if request.method == 'POST':
        job_position = request.POST['position'].capitalize()
        experience_required = request.POST['experience']
        date_posted = request.POST['date']
        job_description = request.POST['description']

        
        data = job.objects.filter(job_position=job_position).values('count')
        if data.exists():
            for info in data:
                count = info['count']

                if count >= 1:
                    count += 1
                    obj = job.objects.get(job_position=job_position)
                    obj.count = count
                    obj.save()

        else:
            job_details = job(job_position=job_position, count=1)
            job_details.save()


        job_post = post(job_position=job_position, experience_required=experience_required,
        date_posted=date_posted, job_description=job_description)
        job_post.save()

        if request.user.is_authenticated:
                user = request.user
                print(user)
                profile_data = profile.objects.get(user=user)
                profile_data.posts.add(job_post)

   
        messages.success(request, 'Your Job has been Posted')  
        return redirect('home')   
    else:
        return render(request, 'jobs/postjob.html')

def jobView(request):
    data = post.objects.all()
    context = {'data': data}
    return render(request, 'jobs/jobview.html', context)

def jobApply(request):
    if request.method == 'POST':
        first_name = request.POST['fname'].capitalize()
        last_name = request.POST['lname'].capitalize()
        email = request.POST['email']
        mobile = request.POST['mobile']
        job_referral = request.POST['hiddenReferral']
        applied_comapny = request.POST['hiddenCompany']
        applied_position = request.POST['hiddenJobPosition']

        job_apply = apply(first_name=first_name, last_name=last_name, email=email, mobile=mobile, job_referral=job_referral,
        applied_company=applied_comapny, applied_position=applied_position)
        job_apply.save()

        messages.success(request, 'Your application has been sent successfully')
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')


def viewApply(request):
    data = apply.objects.all()
    context = {'data': data}
    return render(request, 'jobs/viewapplies.html', context)


def about(request):
    return render(request, 'jobs/about.html')


def contactUs(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('phone', '')
        phone = request.POST.get('email', '')
        desc = request.POST.get('desc', '')

        contact_us = contact(name=name, email=email, phone=phone, desc=desc)
        contact_us.save()
        
        messages.success(request, 'Your Query has been submited')
        return redirect('home')
    else:
        return render(request, 'jobs/contact.html')


def search(request):
    if request.method == 'GET':
        query = request.GET['search'].capitalize()
        print(query)
        if query is not None:
            data = post.objects.filter(job_position__contains=query)
            if data.exists():
                pass
            else:
                data = post.objects.filter(company__contains=query)
            context = {'data': data}
            return render(request, 'jobs/search.html', context)
            
        elif not query:
            messages.error(request, 'Type something to search')
            return redirect('jobView')


def exportCSV(request):
    print('123')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applies.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Company', 'Position Applied', 'Referral Used', 'Email', 'Phone'])

    applies = apply.objects.all().values_list('first_name', 'last_name', 'applied_company',
     'applied_position','job_referral', 'email', 'mobile')
    for applicant in applies:
        writer.writerow(applicant)

    return response


def viewProfile(request):
    if request.user.is_authenticated:
        user = request.user
        data = profile.objects.filter(user=user)
        print(data)
        context = {'data': data}
        return render(request, 'jobs/viewprofile.html', context)
    else:
        return HttpResponse('Not Found')