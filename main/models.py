from django.db import models
from django.core.exceptions import ValidationError

class Location(models.Model):
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return '/locations'

    def __str__(self):
        return self.name

class Place(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def get_absolute_url(self):
        return '/places'

    def __str__(self):
        return self.name

class Event(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    def get_absolute_url(self):
        return '/events'

    # Переопределяем методы clean и save для проверки даты
    def clean(self):
        # Проверка, что дата окончания не раньше даты начала
        if self.date_end < self.date_start:
            raise ValidationError('Дата окончания события не может быть раньше даты начала.')

        # Проверка, что событие не пересекается с другими событиями на том же месте
        overlapping_events = Event.objects.filter(
            place=self.place,
            date_start__lt=self.date_end,
            date_end__gt=self.date_start
        ).exclude(id=self.id)  # Исключаем текущее событие при обновлении
        if overlapping_events.exists():
            raise ValidationError('В это время уже есть событие в этом месте.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super(Event, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name