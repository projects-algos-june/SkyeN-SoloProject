from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt
import re

def index(request):
        request.session['loginerror'] = ""
        return render(request, 'index.html')

def logreg(request):
    return render(request, 'logreg.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            try:
                del request.session['success']
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/logreg')
            except:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/logreg')
        else:
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            mail = request.POST['email']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            User.objects.create(first_name=firstname,last_name=lastname,email=mail,password=pw_hash)
            request.session['success'] = True
            return redirect('/logreg')
    else:
        return redirect('/')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            request.session['username'] = logged_user.first_name
            request.session['userlastname'] = logged_user.last_name
            request.session['useremail'] = logged_user.email
            if 'success' in request.session:
                del request.session['success']
            return redirect('/')
        else:
            messages.error(request, "Incorrect password.")
    else:
        messages.error(request, "No account exists for this email. Please register.")
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def edit(request, user_id):
    if request.session['userid'] != user_id:
        return redirect('/')
    else:
        return render(request, 'myaccount.html')

def update(request, user_id):
    if request.method == "POST":
        if request.session['userid'] != user_id:
            return redirect('/')
        else:
            if len(request.POST['first_name']) < 1:
                messages.error(request, "All fields must be filled.")
                return redirect('/myaccount/' + str(user_id))
            if len(request.POST['last_name']) < 1:
                messages.error(request, "All fields must be filled.")
                return redirect('/myaccount/' + str(user_id))
            if len(request.POST['email']) < 1:
                messages.error(request, "All fields must be filled.")
                return redirect('/myaccount/' + str(user_id))
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(request.POST['email']):            
                 messages.error(request, "Invalid email address!")
                 return redirect('/myaccount/' + str(user_id))
            if request.POST['email'] != request.session['useremail']:
                email = User.objects.filter(email=request.POST['email'])
                if email:
                    messages.error(request, "This email is already taken by another user!")
                    return redirect('/myaccount/' + str(user_id))
                else:
                    userupdater = User.objects.get(id=user_id)
                    userupdater.first_name = request.POST['first_name']
                    userupdater.last_name = request.POST['last_name']
                    userupdater.email = request.POST['email']
                    request.session['username'] = request.POST['first_name']
                    request.session['userlastname'] = request.POST['last_name']
                    request.session['useremail'] = request.POST['email']
                    userupdater.save()
                    return redirect('/')
            else:
                userupdater = User.objects.get(id=user_id)
                userupdater.first_name = request.POST['first_name']
                userupdater.last_name = request.POST['last_name']
                userupdater.email = request.POST['email']
                request.session['username'] = request.POST['first_name']
                request.session['userlastname'] = request.POST['last_name']
                request.session['useremail'] = request.POST['email']
                userupdater.save()
                return redirect('/')
    else:            
        return redirect("/")

def order(request):
    if 'userid' not in request.session:
            request.session['loginerror'] = "Please login to place orders."
            return render(request, 'index.html')
    else:
        if request.method == "POST":
            request.session['color'] = request.POST['color']
            return redirect("/checkout")
        else:
            return redirect("/")

def checkout(request):
    return render(request, 'checkout.html')