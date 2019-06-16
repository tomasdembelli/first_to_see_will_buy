from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from .forms import *
from .decorators import *
from django.urls import reverse
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
import urllib
import json
from django.conf import settings
from django.contrib import messages
from rest_framework import viewsets
from .serializers import AdSerializer




# Create your views here.
#USERS = list(User.objects.all()[:].values_list('user_name', flat=True))
#USER_LIST = list(filter(lambda x: x.user_name, USERS))

def index(request):
    #return HttpResponse('Hello, world. You are at the sahibinden index.')
    return HttpResponseRedirect(reverse('ad_messages:ad_list'))

'''
def ad_list(request):
    ad_list = Ad.objects.order_by('-pub_date')[:]
    response = '<br>'.join([a.ad_title for a in ad_list])
    return HttpResponse(response)
'''

def ad_list(request):
    now = timezone.now()
    old = 120    #Ads older than 'old' won't be shown -- this is not working now.
    #ads_list = Ad.objects.filter(pub_date__lte=now).filter(pub_date__gte=(now - datetime.timedelta(days=old))).order_by('-pub_date')[:]    #filters the one published within last 30 days.    
    #ads_list = Ad.objects.order_by('-pub_date')[:]    
    ads_list = Ad.objects.all()   
    #ads_list = Ad.objects.order_by('-pub_date')[:]     
    template = loader.get_template('ad_messages/ad_list.html')
    context = {'ads_list': ads_list,}
    return HttpResponse(template.render(context, request))


@login_required
def my_ads(request):
    ads_list=Ad.objects.filter(owner=request.user).order_by('-pub_date')[:]
    context = {'ads_list': ads_list,}
    return render(request, 'ad_messages/my_ads.html', context)


@login_required
def my_favourites(request):
    ads_list = request.user.favouritead_set.all()[:]
    context = {'ads_list': ads_list,}
    return render(request, 'ad_messages/my_favourites.html', context)


def detail_(request, ad_id):
    """Shows the details of an ad."""
    #ad_id = ad_id_title.split('_', 1)[0]
    '''
    try:
        ad = Ad.objects.get(id=ad_id)
    except Ad.DoesNotExist:
        raise Http404('Ad does not exist.') 
    '''
    ad = get_object_or_404(Ad, id=ad_id)    # shortcut, better for loose coupling design principle
    #message_list = Message.objects.filter(ad__id=ad_id).order_by('-sent_time')[:]
    message_list = ad.message_set.order_by('-sent_time')[:]     # !!! how to reach foreignkeyed items !!!
    #template = loader.get_template('ad_messages/ad_detail.html')
    context = {'ad': ad, 'message_list': message_list,}
    return render(request, 'ad_messages/ad_detail.html', context)
    #return HttpResponse(template.render(context, request))


@login_required
#@user_is_ad_owner
def ad_detail(request, ad_id):
    """Shows the details of an ad with message form."""

    #num_visits = request.session.get('visit_count', 0)    work on this later !!
    #request.session['visit_count'] = num_visits + 1
    is_favourite = False
    #user = User.objects.get(username=request.user.username)
    ad = get_object_or_404(Ad, id=ad_id)    # shortcut, better for loose coupling design principle
    if request.user.favouritead_set.filter(ad=ad):
        is_favourite = True
    #last_message_sender = str(Ad.objects.get(id=ad.id).message_set.order_by('-sent_time')[0].sender)
    try:
        #last_message_sender = str(Ad.objects.get(id=ad.id).message_set.order_by('-sent_time')[0].sender)
        #last_message_sender = str(Ad.objects.get(id=ad.id).message_set.latest().sender)
        last_message_sender = str(Ad.objects.get(id=ad.id).message_set.latest('sent_time').sender)
        if last_message_sender == request.user.username:
            can_send_message = False      
        else:
            can_send_message = True
    except:
        last_message_sender = None
        can_send_message = True
        #pass
    if request.method == 'POST':
        if 'Message' in request.POST:
            form_message = MessageForm(request.POST)
            if form_message.is_valid():
                #TODO
                #ad_id = form.cleaned_data['ad_id']
                text = form_message.cleaned_data['text']
                #sent_time = form.cleaned_data['sent_time']
                #sender = form.cleaned_data['sender']
                if last_message_sender == request.user.username:
                    messages.warning(request, 'You sent the last message for this ad.')
                    can_send_message = False
                    #pass
                    #return HttpResponse('You are the last sender or you are not a valid User.')
                else:
                    #Message(ad=Ad.objects.get(id=ad.id), text=text, sender=User.objects.get(user_name=sender)).save()    #fix user, now it's allways 1st user
                    #Message(ad=Ad.objects.get(id=ad.id), text=text, sender=request.user).save()    #fix user, now it's allways 1st user
                    Message(ad=ad, text=text, sender=request.user).save()    #fix user, now it's allways 1st user
                    can_send_message = True
                    #request.session['last_message'] = True
                return HttpResponseRedirect(reverse('ad_messages:detail', args=[ad.id]))
        if 'Like' in request.POST:
            FavouriteAd(user=request.user, ad=ad).save()
            messages.success(request, 'Ad is successfully added to your favourites.')
            return HttpResponseRedirect(reverse('ad_messages:detail', args=[ad.id]))
        elif 'Dislike' in request.POST:
            request.user.favouritead_set.filter(ad=ad).delete()
            messages.success(request, 'Ad is removed from your favourites.')
            return HttpResponseRedirect(reverse('ad_messages:detail', args=[ad.id]))
        else:            
            return HttpResponseRedirect(reverse('ad_messages:detail', args=[ad.id]))
        

            
    else:
        form_message = MessageForm()
        #is_favourite_form = FavouriteForm(initial={'is_favourite':is_favourite})
    try:
        message_list = ad.message_set.order_by('-sent_time')[:]     # !!! how to reach foreignkeyed items !!!
    except:
        message_list = []
    context = {'ad': ad, 'message_list': message_list, 'form_message': form_message, 'is_favourite': is_favourite, 'last_message_sender' : last_message_sender, 'can_message_send' : can_send_message,}
    return render(request, 'ad_messages/ad_detail.html', context)



@login_required
def ad_create(request):
    """Creates a new ad."""

    ad_create_form = AdForm()
    context = {'ad_create_form' : ad_create_form,}
    if request.method == 'POST':
        ad_form = AdForm(request.POST)
        if ad_form.is_valid():
            title = ad_form.cleaned_data['title']
            description = ad_form.cleaned_data['description']
            price = ad_form.cleaned_data['price']
            ad = Ad(title=title, owner=request.user, description=description, price=price)
            ad.save()
            messages.success(request, 'Ad created successfully!')
            #ad = Ad.objects.get(ad=ad)
            return HttpResponseRedirect(reverse('ad_messages:detail', args=[ad.pk]))
    return render(request, 'ad_messages/ad_create.html', context)


@login_required
@user_is_ad_owner    #locks the ad_update function to the ad.owner only
def ad_update(request, ad_id):
    """Updates an existing ad."""

    ad = get_object_or_404(Ad, id=ad_id)    # shortcut, better for loose coupling design principle
    ad_update_form = AdForm(instance=ad)    #prefill the form
    context = {'ad_update_form' : ad_update_form, 'ad': ad,}

    if request.method == 'POST':
        ad_form = AdForm(request.POST)
        if ad_form.is_valid():
            ad.title = ad_form.cleaned_data['title']
            ad.description = ad_form.cleaned_data['description']
            ad.price = ad_form.cleaned_data['price']
            ad.save()
            messages.success(request, 'Ad updated successfully!')
            return HttpResponseRedirect(reverse('ad_messages:detail', args=[ad.id]))

    return render(request, 'ad_messages/ad_update.html', context)



def register_user(request):
    """Register a new user."""

    register_user_form = UserForm()
    context = {'register_user_form' : register_user_form,}
    if request.method == 'POST':
        register_user_form = UserForm(request.POST)
        if register_user_form.is_valid():
            username = register_user_form.cleaned_data['username']
            email = register_user_form.cleaned_data['email']
           # password = register_user_form.cleaned_data['password']
            #user = User(username=username, email=email, password=password)
            user = User(username=username, email=email,)
            user.save()
            user.is_active = False
            return HttpResponseRedirect(reverse('password_reset'))
    return render(request, 'ad_messages/register_user.html', context)


def signup(request):
    """Signup a new user."""

    if request.method == 'POST':
        form = SignUpForm(request.POST)    #Similar to fom = User(username=something, password=something) since we used User as model for this form.
        
        if form.is_valid():    #all standard validation (defined in the form fields) done if this is true
            ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation ''' 
        if result['success']:
        
            user = form.save(commit=False)    #saving this specific instance of user. We want to something more with the user before committing it to the db.
            user.is_active = False
            user.save()
            user.refresh_from_db()    # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data['birth_date']
            user.profile.bio = form.cleaned_data['bio']
            user.profile.location = form.cleaned_data['location']
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Sahibinden Account'
            message = render_to_string('ad_messages/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),    #https://stackoverflow.com/questions/47814228/django-2-python-3-4-cannot-decode-urlsafe-base64-decodeuidb64
                #'uid': urlsafe_base64_encode(user.pk),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('ad_messages:account_activation_sent')
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=user.username, password=raw_password)
            #login(request, user)
            #return HttpResponseRedirect(reverse('ad_messages:ad_list'))
        else:
            #messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return HttpResponse('Invalid reCAPTCHA. Please try again.')
    else:
        form = SignUpForm()
    return render(request, 'ad_messages/signup.html', {'form': form})



def account_activation_sent(request):
    return HttpResponse('Please confirm your email address to complete the registration.')



def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):    #https://stackoverflow.com/questions/45961459/multiple-authentication-backends-configured-and-therefore-must-provide-the-back
    try:
        #uid = force_text(urlsafe_base64_decode(uidb64))
        uid = urlsafe_base64_decode(uidb64).decode()    #https://stackoverflow.com/questions/47814228/django-2-python-3-4-cannot-decode-urlsafe-base64-decodeuidb64
        #uid = str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    #except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend)
        return redirect('ad_messages:ad_list')
    else:
        return render(request, 'ad_messages/account_activation_invalid.html')


# REST Framework
class AdListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ads to be viewed or edited.
    """
    #queryset = Ad.objects.all()
    #queryset = Ad.objects.order_by('-pub_date')[:]   
    queryset = Ad.objects.all()   
    serializer_class = AdSerializer