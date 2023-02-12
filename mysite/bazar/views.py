
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.utils import timezone
from .models import CharityEvent, Item, UserProfile, ReservedItem
from .forms import SignUpForm, LoginForm, CreateEventForm,ItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class IndexView(View):
    template_name = 'bazar/index.html'

    def get(self, request, *args, **kwargs):
        events = CharityEvent.objects.filter(Q(end_date__gte=timezone.now()) | Q(end_date__isnull=True))
        context = {
            'charity_events': events
        }
        return render(request, self.template_name, context)

    def post(self,request,*args, **kwargs):
        search_query = request.POST.get('search_query')
        items = Item.objects.filter(description__icontains=search_query)
        context = {'items': items}
        return render(request,  self.template_name, context)



class ReservedItemsView(View):
    def get(self, request):
        reserved_items = ReservedItem.objects.filter(user=request.user)
        context = {'reserved_items': reserved_items}
        return render(request, 'bazar/reserved_items.html', context)


class ReserveItemsView(View):
    def post(self, request, item_id):
        item = Item.objects.get(id=item_id)
        ReservedItem.objects.create(item = item, user = request.user)
        return redirect('bazar:reserved_items')

class AddItemView(View):
    def get(self, request, event_id):
        event = CharityEvent.objects.filter(pk = event_id).first()
        form = ItemForm()

        context = {
            'form': form,
            'charity_event': event,
            'event_id': event_id
        }
        
        return render(request, 'bazar/create_item.html', context)


    def post(self, request, event_id):
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            event = CharityEvent.objects.get(id=event_id)
            item = Item(charity_event=event, user = request.user, description=form.cleaned_data['description'], photo=form.cleaned_data['photo'], price = form.cleaned_data['price'])
            item.save()
            return redirect('bazar:index')
        return render(request, 'bazar/create_item.html', {'form': form})



class CreateEventView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = CreateEventForm()
        return render(request, 'bazar/create_event.html', {'form': form})

    def post(self, request):
        form = CreateEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('bazar:index')
        return render(request, 'bazar/create_event.html', {'form': form})

class EventDetailView(View):
    template_name = 'bazar/event_detail.html'

    def get(self, request, *args, **kwargs):
        event = get_object_or_404(CharityEvent, pk=kwargs['pk'])
        items = Item.objects.filter(charity_event=event)
        context = {
            'charity_event': event,
            'items': items
        }
        return render(request, self.template_name, context)

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'bazar/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('bazar:index')
        return render(request, 'bazar/login.html', {'form': form})
        

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "account_created":False,
        }
        return render(request, 'bazar/signup.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        userExists = User.objects.filter(username=email).first()

        if userExists:
            context = {
                "message":"Já existe um usuário com esse email",
                 "account_created":False,
            }
            return render(request, 'bazar/signup.html', context)

        user_created = User.objects.create_user(username=email, password=password)
        profile_created = UserProfile.objects.create(user=user_created, name = name, phone = phone)

        user_created.save()
        profile_created.save()
        context = {
                "message":"Sua conta foi criada. Vamos Fazer Login!",
                "account_created":True,
            }
        return render(request, 'bazar/signup.html', context)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('bazar:index')

        