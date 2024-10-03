from django.shortcuts import render, redirect
from .models import Location, Place, Event
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth import login as dj_login, authenticate, logout as dj_logout
from .forms import LoginForm, RegisterForm, LocationForm, PlaceForm, EventForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError

# Представления, связанные с  авторизацией
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            dj_login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                dj_login(request, user)
                return redirect('/')
            else:
                return render(request, 'main/login.html', {'message':'Неправильное имя пользователя или пароль'})
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

@login_required(login_url=login)
def logout(request):
    dj_logout(request)
    return redirect('/login')

@login_required(login_url=login)
def profile(request):
    return render(request, 'main/profile.html')

# Представления, связанные с локациями
def locations(request):
    locations = Location.objects.all()
    context = {
        'locations': locations
    }
    return render(request, 'main/locations.html', context)

@login_required(login_url=login)
def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/locations')
    else:
        form = LocationForm()
    
    context = {
        'form': form
    }
    return render(request, 'main/add_location.html', context)

@method_decorator(login_required, name='dispatch')
class update_location(UpdateView):
    model = Location
    template_name = 'main/update_location.html'
    form_class = LocationForm

@method_decorator(login_required, name='dispatch')
class delete_location(DeleteView):
    model = Location
    success_url = '/locations'
    template_name = 'main/delete_location.html'

#Представления, связанные с местами
def places(request):
    places = Place.objects.all()
    context = {
        'places': places
    }
    return render(request, 'main/places.html', context)

@login_required(login_url=login)
def add_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/places')
    else:
        form = PlaceForm()
    context = {
        'form': form
    }
    return render(request, 'main/add_place.html', context)

@method_decorator(login_required, name='dispatch')
class update_place(UpdateView):
    model = Place
    template_name = 'main/update_place.html'
    form_class = PlaceForm

@method_decorator(login_required, name='dispatch')
class delete_place(DeleteView):
    model = Place
    success_url = '/places'
    template_name = 'main/delete_place.html'

# Представления, связанные с событиями
def events(request):
    place_id = request.GET.get('place')
    location_id = request.GET.get('location')
    datetime_start = request.GET.get('date-time-start')
    datetime_end = request.GET.get('date-time-end')
    events = Event.objects.all()

    # Фильтрация
    if place_id:
        events = events.filter(place_id=place_id)
    if location_id:
        events = events.filter(place__location_id=location_id)
    if datetime_start and datetime_end:
        events = events.filter(date_start__gte=datetime_start, date_end__lte=datetime_end)
    elif datetime_start:
        events = events.filter(date_start=datetime_start)
    elif datetime_end:
        events = events.filter(date_end=datetime_end)

    context = {
        'events': events,
        'places': Place.objects.all(),
        'locations': Location.objects.all()
    }
    return render(request, 'main/events.html', context)

@login_required(login_url=login)
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            try:
                new_event = form.save(commit=False)
                new_event.clean()
                new_event.save()
                return redirect('/events')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = EventForm()

    context = {
        'form': form
    }
    return render(request, 'main/add_event.html', context)

@method_decorator(login_required, name='dispatch')
class update_event(UpdateView):
    model = Event
    template_name = 'main/update_event.html'
    form_class = EventForm

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
class delete_event(DeleteView):
    model = Event
    success_url = '/events'
    template_name = 'main/delete_event.html'