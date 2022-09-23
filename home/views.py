from django.shortcuts import render
from broadcast.models import News, PlayerProfile, Broadcast
from django.views.generic import ListView


# Create your views here.


def home(request):
    context = {
        'news': News.objects.all()[:3]
    }
    return render(request, 'home/home.html', context)


class NewsListView(ListView):
    model = News
    context_object_name = 'blogs'
    template_name = 'home/news.html'
    paginate_by = 12


class NewsDetailsListView(ListView):
    model = News
    context_object_name = 'blog'
    template_name = 'home/news_detals.html'

    def get_queryset(self):
        return News.objects.get(pk=self.kwargs['pk'])


class PlayerProfileListView(ListView):
    model = PlayerProfile
    context_object_name = 'players'
    template_name = 'home/player.html'
    paginate_by = 12


class PlayerDetailsListView(ListView):
    model = PlayerProfile
    context_object_name = 'player'
    template_name = 'home/players_details.html'

    def get_queryset(self):
        return PlayerProfile.objects.get(pk=self.kwargs['pk'])


class LiveMatchesListView(ListView):
    model = Broadcast
    context_object_name = 'matches'
    template_name = 'home/live_match.html'
    paginate_by = 12


class LiveMatchesDetailsListView(ListView):
    model = Broadcast
    context_object_name = 'match'
    template_name = 'home/live_match_details.html'

    def get_queryset(self):
        return Broadcast.objects.get(pk=self.kwargs['pk'])


