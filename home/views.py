from django.shortcuts import render
from django.utils.decorators import method_decorator

from broadcast.models import News, PlayerProfile, Broadcast
from django.views.generic import ListView


# Create your views here.
from decorators import is_login


def home(request):
    context = {
        'news': News.objects.all()[:3],
        'active':'home'
    }
    return render(request, 'home/home.html', context)


class NewsListView(ListView):
    model = News
    context_object_name = 'blogs'
    template_name = 'home/news.html'
    paginate_by = 12

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'news'
        return context


class NewsDetailsListView(ListView):
    model = News
    context_object_name = 'blog'
    template_name = 'home/news_detals.html'

    def get_queryset(self):
        return News.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'news'
        return context


class PlayerProfileListView(ListView):
    model = PlayerProfile
    context_object_name = 'players'
    template_name = 'home/player.html'
    paginate_by = 12
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'players'
        return context


class PlayerDetailsListView(ListView):
    model = PlayerProfile
    context_object_name = 'player'
    template_name = 'home/players_details.html'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'players'
        return context

    def get_queryset(self):
        return PlayerProfile.objects.get(pk=self.kwargs['pk'])

@method_decorator(is_login(), name='dispatch')
class LiveMatchesListView(ListView):
    model = Broadcast
    context_object_name = 'matches'
    template_name = 'home/live_match.html'
    paginate_by = 12

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'matches'
        return context

@method_decorator(is_login(), name='dispatch')
class LiveMatchesDetailsListView(ListView):
    model = Broadcast
    context_object_name = 'match'
    template_name = 'home/live_match_details.html'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'matches'
        return context

    def get_queryset(self):
        return Broadcast.objects.get(pk=self.kwargs['pk'])


