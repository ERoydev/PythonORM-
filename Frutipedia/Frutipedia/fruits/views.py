from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from .forms import CategoryAddForm, AddFruitForm, EditFruitForm, DeleteFruitForm
# Create your views here.
from .models import Fruit, Category


def index(request):
    return render(request, 'common/home.html')


def dashboard(request):
    fruits = Fruit.objects.all()

    context = {
        'fruits': fruits,
    }

    return render(request, 'common/dashboard.html', context)


class CreateFruitView(CreateView):
    model = Fruit
    form_class = AddFruitForm
    template_name = 'fruits/create-fruit.html'
    success_url = reverse_lazy('dashboard')


def details_fruit(request, pk):
    fruit = Fruit.objects.get(id=pk)

    context = {
        "fruit": fruit,
    }

    return render(request, 'fruits/details-fruit.html', context)


def edit_fruit(request, pk):
    fruit = Fruit.objects.get(id=pk)

    if request.method == 'GET':
        form = EditFruitForm(instance=fruit)

    else:
        # I need to specify the instance or it will create a new record in db instead of editing this changes
        form = EditFruitForm(request.POST, instance=fruit)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        "form": form,
        "fruit": fruit
    }

    return render(request, 'fruits/edit-fruit.html', context)


# CBV (Class Based Views)
class DeleteFruitView(DeleteView):
    model = Fruit
    form_class = DeleteFruitForm
    template_name = 'fruits/delete-fruit.html'
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object() # fruit = Fruit.objects.get(id=pk)
        form = self.form_class(instance=self.object) # form = EditFruitForm(instance=fruit)
        return self.render_to_response(self.get_context_data(form=form, object=self.object)) # return render(request, 'fruits/edit-fruit.html', context)

    def post(self, request, *args, **kwargs):
        self.objects = self.get_object()
        self.object.delete()
        return redirect(self.success_url)

def create_category(request):
    if request.method == "GET":
        form = CategoryAddForm()

    elif request.method == "POST":
        form = CategoryAddForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        "form": form,
    }

    return render(request, 'categories/create-category.html', context)