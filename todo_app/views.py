from django.urls import reverse, reverse_lazy
from django.views.generic import(
    ListView, 
    CreateView,
    UpdateView,
    DeleteView,

)


from .models import ToDoList, ToDoItem  


class ListListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"  # Substitua pelo seu template Nome do contexto para a lista de objetos

class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context
    
class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Adicionar nova Lista"
        return context
    
class ItemCreate(CreateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_initial(self):
        initial_datal = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_datal["todo_list"] = todo_list
        return initial_datal
    
    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs ["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Adicionar nova tarefa"
        return context
    
    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list.id])

class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Atualizar tarefa"
        return context
    
    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list.id])
    
class ListDelete(DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index")


class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context