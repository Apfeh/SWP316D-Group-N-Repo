from django.shortcuts import render, get_object_or_404, redirect
from .models import InsuredPerson
from django.urls import reverse

def index(request):
    insured_persons = InsuredPerson.objects.all()
    return render(request, 'insured_persons.html', {'insured_persons': insured_persons})

def delete_insured_person(request, id):
    person = get_object_or_404(InsuredPerson, id=id)
    if request.method == 'POST':
        person.delete()
        return redirect(reverse('insured_persons_list'))
    return redirect(reverse('insured_persons_list'))
