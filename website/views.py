from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record 

# Home view
def home(request):
    # retrieve the records 
    records = Record.objects.all()

    # check to see if user is logging in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have succesfully logged in!")
            return redirect ("home")
        else:
            messages.success(request, "Error logging in. Please try again...")
            return redirect ("home")
    return render(request, 'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect ("home")

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # look up a single record 
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, 'Oh no! You must login to view the record.')
        return redirect('home')
    

def customer_detail(request, pk):
    customer_record = get_object_or_404(Record, id=pk)
    return render(request, 'customer_detail.html', {'customer_record': customer_record})

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record has been deleted successfully.")
        return redirect('home')
    else:
        messages.success(request, 'Oh no! You must login to delete the record.')
        return redirect('home')
  
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record is added!")
                return redirect('home')  
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "Oh no! You must login to add the record.")
        return redirect('home')  
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = get_object_or_404(Record, id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated!")
            return redirect('home')  
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "Oh no! You must login to update the current record.")
        return redirect('home')
