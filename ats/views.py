from typing_extensions import final
from django.shortcuts import redirect, render
from numpy.lib.function_base import append
from pdf2image import convert_from_path
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from ats.models import skill,Resume
import easyocr
import numpy as np

#########Functions#########
def readfile(file):
    reader = easyocr.Reader(['en'])
    image = convert_from_path(file,poppler_path=r'C:/Program Files/poppler-0.68.0/bin')
    read_image = reader.readtext(np.array(image[0]),min_size=0,slope_ths=0.2,ycenter_ths=0.7,height_ths=0.6,width_ths=0.8,decoder="beamsearch",beamWidth=10)
    str_text = ""
    for i in range(len(read_image)):
        str_text = str_text+read_image[i][1]+"\n"
    return str_text

def search(lst, target):
    low = 0  
    high = len(lst) - 1  
    mid = 0  
    while (low <= high):
        mid = (high + low) // 2
        if( lst[mid] < target):  
            low = mid + 1
        elif (lst[mid] > target):  
            high = mid - 1
        else:  
            return lst[mid]
    return -1  

#########Urls############
def home(request):
    return render(request,'base.html')

@login_required(login_url='/signin/')
def main(request):
    return render(request,'main.html')
def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_password']:
            if request.POST['first_name'] and request.POST['last_name'] and request.POST['email']:
                uname = str(request.POST['email']).split("@")
                uname = uname[0]
                try:
                    user = User.objects.get(email=request.POST['email'])
                    return render(request,'signup.html',{'error':"This username in this email already exists"})
                except User.DoesNotExist:
                    fname = request.POST['first_name']
                    lname = request.POST['last_name']
                    uemail = request.POST['email']
                    password = request.POST['password']
                    user = User.objects.create_user(first_name=fname,last_name=lname,username = uname,email = uemail,password = password)
                    user.save()
                    checkuser = User.objects.get(email=uemail)
                    auth.login(request,checkuser)
                    #User create done
                    return redirect(main)
            else:
                return render(request,'signup.html',{'error':"Empty Field Occurs"})
        else:
            return render(request,'signup.html',{'error':"Password doesn't match."})
    else:
        return render(request,'signup.html')
    return render(request,'signup.html')
def signin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['email'] and request.POST['password']:
                useremail = User.objects.get(email=request.POST.get('email'))
                passw = request.POST.get('password')
                try:
                    user = auth.authenticate(request,username=useremail,password=passw)
                    #print(user)
                    if user is not None:
                        auth.login(request, user)
                        messages.success(request, "You are successfully logged in now")
                        return redirect(main)
                    else:
                        messages.error(request, "Invalid Credentials,Please try again")
                        return redirect("signin")
                except User.DoesNotExist:
                    return render(request, 'signin.html', {'error': "User doesnot exists"})
            else:
                return render(request, 'signin.html', {'error': "Empty field occurs."})
        else:
            return render(request,'signin.html')
    else:
        return redirect(main)

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/signin/')
def dashboard(request):
    print(Resume.objects.filter(user = User.objects.get(username = request.user)).values_list("resume",flat=True))
    resume = Resume.objects.filter(user = User.objects.get(username = request.user)).all()
    resume_list = []
    for i in resume:
        #print(i.resume)
        resume_list.append([i.id,str(i.resume)])
    print(resume_list)
    context ={
        'resume_list':resume_list,
    }
    return render(request,'dashboard.html',context)

@login_required(login_url='/signin/')
def upload(request):
    if request.method == 'POST':
        try:
            myfile = request.FILES['myfile']
            print(myfile)
            check = str(myfile)
            print(User.objects.get(username = request.user))
            print(Resume.objects.filter(user = User.objects.get(username = request.user)).values_list("resume",flat=True))
            print(Resume.objects.filter(user = User.objects.get(username = request.user)).values_list("resume",flat=True).filter(resume = check))
            print(len(Resume.objects.filter(user = User.objects.get(username = request.user)).values_list("resume",flat=True).filter(resume = check)))
            if(len(Resume.objects.filter(user = User.objects.get(username = request.user)).values_list("resume",flat=True).filter(resume = check))==0):
                save_file = Resume(user = User.objects.get(username = request.user),resume = myfile)
                save_file.save()
            else:
                messages.error(request,'Filename is already exists')
                return redirect(main)
            context =  readfile("media/"+str(myfile))
            #print(final_output)
            return render(request,'description.html',{'context':context})
        except:
            return redirect(main)
    else:
        return render(request,'description.html')


@login_required(login_url='/signin/')
def openstat(request,pk1_id):
    #print(pk1_id)
    #print(Resume.objects.filter(user = User.objects.get(username = request.user)).filter(id = pk1_id))
    resume = Resume.objects.filter(user = User.objects.get(username = request.user)).values_list("resume",flat=True).filter(id=pk1_id)
    myfile  = str(resume.first())
    #print(str(resume.first()))
    context =  readfile("media/"+myfile)
    return render(request,'description.html',{'context':context})

@login_required(login_url='/signin/')
def description(request):
    #print(final_output)
    if request.method == 'POST' and request.POST['jd']:
        resume  = request.POST['resume']
        jd = request.POST['jd']
        resume = str(resume).upper()
        resume = resume.replace("C+T","C++")
        jd = str(jd).upper()
        sort_jdarr = [resume,jd]
        final_list = []
        list_set = skill.objects.all()
        
        for i in sort_jdarr:
            ex_data = []
            for j in list_set:
                if((i.find(str(j).upper()) or i.find(str(j.catagory).upper()))>0 and (i.find(str(j).upper()) or i.find(str(j.catagory).upper()))<len(i)):
                    ex_data.append(str(j))
            #print(ex_data)
            ex_data.sort()
            #print(r)
            final_list.append(ex_data)
        #print(request.POST['jd'])
        
        #print(final_list)
        #print(final_list[1])
        check = final_list[0]
        skills = []
        for i in range(len(final_list[1])):
            search_item = final_list[1][i]
            #print(search_item)
            if(search(check,search_item)==-1):
                continue
            skills.append(search(check,search_item))
            #print(search(check,search_item),end="\n")
        print(skills)

        context = {
            "your_resume":final_list[0],
            "JD":final_list[1],
            'matched_skills':skills,
            'numberof_matchedskills':len(skills),
            'total_required_skills':len(final_list[1]),
            'matched_percentage':round((len(skills)/len(final_list[1]))*100,2),
        }
        return render(request,'result.html',context)
    else:
        return render(request,'description.html')

##########Admin###########

def atsadmin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(home)
    return render(request,'admin.html')

@login_required(login_url='/atsadmin/')
def addskills(request):
    return render(request,'skills.html')

@login_required(login_url='/atsadmin/')
def add(request):
    if request.method == "POST":
        Skill = request.POST.get('skill')
        catagory = request.POST.get('catagory')
        print(Skill)
        print(catagory)
        find_skill = skill.objects.filter(skill = Skill)
        print(find_skill)
        total_skill = skill.objects.all()
        print(total_skill)
        if(len(find_skill)==0):
            addskill = skill(skill = Skill,catagory = catagory)
            addskill.save()
        print(len(find_skill))
        return redirect(addskills)
    return render(request,'skills.html')

@login_required(login_url='/atsadmin/')
def alldata(request):
    total_skill  = skill.objects.all()
    print(total_skill)
    alld = []
    for i in total_skill:
        alld.append([i.id,i.skill,i.catagory])
    print(alld)
    context ={
        'total_skills':alld,
    }
    return render(request,'alldata.html',context)

@login_required(login_url='/atsadmin/')
def delete(request,pk_id):
    if request.method == "POST":
        check_username = request.POST.get('checkusername')
        print(request.user)
        if(str(request.user) == str(check_username)):
            delete_skill = skill.objects.get(id = pk_id)
            delete_skill.delete()
            print(delete_skill)
        else:
            return redirect(alldata)
    return redirect(alldata)