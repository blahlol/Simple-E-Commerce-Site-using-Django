from django.shortcuts import  render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signupView(request):
    if request.method=='GET':
        form=UserCreationForm()
        return render(request,'registration/signup.html',{'form':form})
    elif request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('store:home')
        else:
            return render(request,'registration/signup.html',{'form':form})

