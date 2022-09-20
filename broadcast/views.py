from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import BroadcastForm
from .models import Broadcast
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.

class BroadCastCreateView(CreateView):
    form_class = BroadcastForm
    success_url = 'nosuccess'
    template_name = 'broadcast/create.html'

    def get_success_url(self):
        broadcast_type = self.object.categories
        return reverse_lazy('broadcast:list_broadcast', kwargs={'type': broadcast_type})


class BroadCastListView(ListView):
    model = Broadcast
    context_object_name = 'videos'
    template_name = 'broadcast/list.html'

    def get_queryset(self):
        if self.kwargs['type'] == 'Live':
            print(Broadcast.objects.filter(categories__name='Live'))
            return Broadcast.objects.filter(categories__name='Live')
        else:
            return Broadcast.objects.filter(categories__name='Highlights')


class BroadCastUpdateView(UpdateView):
    form_class = BroadcastForm
    model = Broadcast
    template_name = 'broadcast/update.html'

    def get_success_url(self):
        broadcast_type = self.object.categories
        return reverse_lazy('broadcast:list_broadcast', kwargs={'type': broadcast_type})


def delete_video(request):
    if request.method == 'POST':
        Broadcast.objects.filter(pk=request.POST['pk']).delete()
        messages.success(request, f'Video Deleted Successfully')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def view_video(request, pk):
    broad_cast = Broadcast.objects.get(pk=pk)
    broad_cast.total_view = broad_cast.total_view+1
    broad_cast.save()
    context = {
        'videos': broad_cast
    }
    return render(request, 'broadcast/view.html', context)
