from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Mail, Box
from .forms import MailForm

# Create your views here.

def home(request): #On the homescreen (inbox)
    return box(request, 'Inbox') #Go to the inbox FOR NOW. MAKE INTRO PAGE LATER.

def box(request, name): #Going inside of a box

    if request.GET.get('q') != None:
        q = request.GET.get('q')
        mail = Mail.objects.filter(
            Q(content__icontains=q) |
            Q(title__icontains=q))
    else:
        mail = Mail.objects.all() #Only grab mail that's inside that specific box

    boxes = Box.objects.all()
    box = Box.objects.get(name=name)

    context = {'boxes': boxes, 'box': box, 'mail': mail}

    return render(request, 'box.html', context)

def mail(request, pk): #Looking at an email
    letter = Mail.objects.get(id=pk) #Grab whatever letter is equal to the pk
    letter.isUnread = False #Marks the letter as read
    letter.save() #Saves it to the database
    context = {'letter': letter}

    return render(request, 'mail.html', context)

def sendMail(request): #Sending an email
    form = MailForm()
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)

    context = {'form': form}

    return render(request, 'mailForm.html', context)

def respond(request, pk): #Responding to an email
    letter = Mail.objects.get(id=pk) #Grab whatever letter is equal to the pk

    if request.method == 'POST':
        newLetter = Mail()
        form = MailForm(request.POST, instance=newLetter)

        if form.is_valid():
            letter.inShadowRealm = True #The old email won't show up anywhere. Keeps the mail in a thread.

            newLetter.save()
            letter.save()
            return redirect('home')
        
        else:
            print(form.errors)

    #Filling in the form
    letter.receiver = letter.sender #Sender becomes the receiver
    letter.sender = None #Will change the sender to the user later. CHANGE LATER.
    letter.currentBox = Box.objects.get(name='Inbox') #Defaults to the inbox
    letter.previousMail = letter #The response points to the old email
    letter.content = '' #Wipe what was in it previously
    letter.isResponse = True #Marks the form as a response

    form = MailForm(instance=letter) #Convert letter to form

    context = {'letter': letter, 'form': form}

    return render(request, 'mailForm.html', context)

def markUnreadOrRead(request, pk):
    letter = Mail.objects.get(id=pk)
    letter.isUnread = not letter.isUnread #Flip the boolean
    letter.save()

    return redirect('home')

def moveMailToBox(request, pk, name):
    letter = Mail.objects.get(id=pk)
    box = Box.objects.get(name=name)

    letter.currentBox = box
    letter.save()

    return redirect('home')


def deleteEmail(request, pk): #Delete an email
    letter = Mail.objects.get(id=pk)
    letter.delete()

    return redirect('home')