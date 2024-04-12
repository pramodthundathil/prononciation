from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.shortcuts import render
import speech_recognition as sr
import pyttsx3
from difflib import SequenceMatcher
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .forms import UserAddForm, AddPrononciationForm
from django.contrib.auth.models import User,Group
from textblob import TextBlob

from .models import AudioPrononciation, Comments
from django.contrib.auth.decorators import login_required
from .decorators import admin_only

from django.http import JsonResponse
from django.views.decorators.http import require_POST


@admin_only
def Index(request):
    return render(request,"index.html")


def Detect(request):

    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    user_word = ""
    threshold = 0.8

    if request.method == 'POST':
        correct_word = request.POST["word"]
        recognizer = sr.Recognizer()
        pronon = "Correct prononciation is {}".format(correct_word)


        with sr.Microphone() as source:
            print("Please say the word.")
            audio = recognizer.listen(source)
             

        try:
            word = recognizer.recognize_google(audio)
            user_word = word
            similarity_score = similarity(correct_word, user_word)

            if similarity_score >= threshold:
                engine = pyttsx3.init()
                engine.say("Correct prononciation congrats")
                engine.runAndWait()
                val = "Correct Pronunciation!"
            else:
                engine = pyttsx3.init()
                engine.say(pronon)
                engine.runAndWait()
                val = "Wrong Pronunciation. Try again."
            return render(request, 'detectpronon.html', {'word':"you said {}".format(user_word), "val":val, "similarity_score":"Accuracy score: {}".format(similarity_score)})
        except sr.UnknownValueError:
            message = "Speech Recognition could not understand the audio."
            engine = pyttsx3.init()
            engine.say(pronon)
            engine.runAndWait()
            val = "Wrong Pronunciation. Try again."
        except sr.RequestError as e:
            engine = pyttsx3.init()
            engine.say(pronon)
            engine.runAndWait()
            val = "Wrong Pronunciation. Try again."
            message = f"Could not request results from Google Speech Recognition service; {e}"

        return render(request, 'detectpronon.html', {'message': message,"val":val})

    return render(request, 'detectpronon.html')


def GetPronon(request):

    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    user_word = ""
    threshold = 0.8

    if request.method == 'POST':
        correct_word = request.POST["word"]
        recognizer = sr.Recognizer()
        pronon = correct_word 
        engine = pyttsx3.init()
        engine.say(pronon)
        engine.runAndWait()

        return render(request, 'getpronon.html', {"val":"Your Word Is {}".format(pronon)})

    return render(request, 'getpronon.html')

def CheckPrononciation(request):
    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    user_word = ""
    threshold = 0.8

    if request.method == 'POST':
        correct_word = request.POST["word"]
        recognizer = sr.Recognizer()
        pronon = "Correct prononciation is {}".format(correct_word)


        with sr.Microphone() as source:
            print("Please say the word.")
            audio = recognizer.listen(source)
             

        try:
            word = recognizer.recognize_google(audio)
            user_word = word
            similarity_score = similarity(correct_word, user_word)

            if similarity_score >= threshold:
                engine = pyttsx3.init()
                engine.say("Correct prononciation congrats")
                engine.runAndWait()
                val = "Correct Pronunciation!"
            else:
                engine = pyttsx3.init()
                engine.say(pronon)
                engine.runAndWait()
                val = "Wrong Pronunciation. Try again."
            return render(request, 'checkpronunciation.html', {'word':"you said {}".format(user_word), "val":val, })
        except sr.UnknownValueError:
            message = "Speech Recognition could not understand the audio."
            engine = pyttsx3.init()
            engine.say(pronon)
            engine.runAndWait()
            val = "Wrong Pronunciation. Try again."
        except sr.RequestError as e:
            engine = pyttsx3.init()
            engine.say(pronon)
            engine.runAndWait()
            val = "Wrong Pronunciation. Try again."
            message = f"Could not request results from Google Speech Recognition service; {e}"

        return render(request, 'checkpronunciation.html', {'message': message,"val":val})

    return render(request, 'checkpronunciation.html')





def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            login(request, user1)
            return redirect('Index')
        
        else:
            messages.info(request,'Username or Password Incorrect')
            return redirect('SignIn')
    return render(request,"login.html")

def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get("email")
            if User.objects.filter(username = username).exists():
                messages.info(request,"Username Exists")
                return redirect('SignUp')
            if User.objects.filter(email = email).exists():
                messages.info(request,"Email Exists")
                return redirect('SignUp')
            else:
                new_user = form.save()
                new_user.save()
                
                # group = Group.objects.get(name='user')
                # new_user.groups.add(group) 
                
                messages.success(request,"User Created")
                return redirect('SignIn')
            
    return render(request,"register.html",{"form":form})



def SignOut(request):
    logout(request)
    return redirect('Index')


@login_required(login_url="SignIn")
def AddPrononciation(request):
    form = AddPrononciationForm()
    audio = AudioPrononciation.objects.filter(user = request.user)
    if request.method == "POST":
        form = AddPrononciationForm(request.POST,request.FILES)
        if form.is_valid():
            aus = form.save()
            aus.user = request.user
            aus.save()
            messages.success(request,"Data Saved")
            return redirect('AddPrononciation')
        else:
            messages.success(request,"something wrong")
            return redirect('AddPrononciation')


    context = {
        "form":form,
        "audio":audio
    }
    return render(request,"addprononciation.html",context)


@login_required(login_url="SignIn")
def AllPrononciations(request):
    audio = AudioPrononciation.objects.all()
    

    for val in audio:
        comments = []
        user_comment = Comments.objects.filter(Audio = val)
        for com in user_comment:
            comments.append(com.comment)
            # Perform sentiment analysis for each comment
        sentiment_scores = []
        for comment in comments:
            blob = TextBlob(comment)
            sentiment_score = blob.sentiment.polarity
            sentiment_scores.append((comment, sentiment_score))

        # Sort comments based on sentiment scores
        sorted_comments = sorted(sentiment_scores, key=lambda x: x[1], reverse=True)
        total = 0
        # Print sorted comments with sentiment scores
        for comment, score in sorted_comments:
            print(f"Sentiment Score: {score:.2f} - Comment: {comment}")
            total = total + score
        val.sentimental_score = total
        val.save()


    

    comment = Comments.objects.all()
    audio1 = AudioPrononciation.objects.all().order_by("-sentimental_score")


    context = {
        "audio":audio1,
        "comment":comment
    }
    return render(request,"prononciation.html",context)




@login_required(login_url="SignIn")
def Addcomment(request,pk):
    audio = AudioPrononciation.objects.get(id = pk)
    if request.method == "POST":
        comm = request.POST["comment"]
        comment = Comments.objects.create(Audio = audio,user = request.user, comment = comm )
        comment.save()
        return redirect("AllPrononciations")
    return redirect("AllPrononciations")


def Search(request):
    if request.method == "POST":
        search = request.POST['search']
        audio = AudioPrononciation.objects.filter(word__contains = search ).order_by("-sentimental_score")
        comment = Comments.objects.all()

        context  = {
            "audio":audio,
            "comment":comment

        }
        return render(request,"prononciation.html",context)


def AdminIndex(request):
    comment = Comments.objects.all()
    audio1 = AudioPrononciation.objects.all().order_by("-sentimental_score")

    context = {
        "audio":audio1,
        "comment":comment
    }
    return render(request,"adminindex.html",context)

def DeletePronunciation(request,pk):
    AudioPrononciation.objects.get(id = pk).delete()
    messages.info(request,"Pronunciation deleted successfully....")
    return redirect("AdminIndex")

from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="SignIn")
def like_audio(request, pk):

    audio = AudioPrononciation.objects.get(id=pk)
    if request.user in audio.likes.all():
        audio.likes.remove(request.user)
        audio.save()
        return redirect("AllPrononciations")

    else:
        audio.likes.add(request.user)
        audio.save()
        return redirect("AllPrononciations")
    return redirect("AllPrononciations")






