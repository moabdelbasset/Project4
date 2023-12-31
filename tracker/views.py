from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from .models import Tracker
from .forms import TrackerForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from itertools import groupby
from operator import attrgetter
from .services import fetch_calories


class Trackers(ListView):
    """View all food"""

    template_name = "tracker/trackers.html"
    model = Tracker
    context_object_name = "trackers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped_by_date = {}

        for date, group in groupby(
            self.object_list.order_by("-date"), lambda x: x.date
        ):
            grouped_entries = list(group)
            total_calories = sum(entry.calories or 0 for entry in grouped_entries)
            grouped_by_date[date] = {
                "entries": grouped_entries,
                "total_calories": total_calories,
            }

        context["trackers_grouped"] = grouped_by_date
        return context

    def get_queryset(self):
        return Tracker.objects.filter(user=self.request.user.profile)


# Create your views here.
class AddTracker(LoginRequiredMixin, CreateView):
    """
    Add a tracker view
    """

    template_name = "tracker/add_tracker.html"
    model = Tracker
    form_class = TrackerForm
    success_url = "/tracker/"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        # profile = self.request.user.profile
        form.instance.user = self.request.user.profile
        calories, error = fetch_calories(
            form.instance.title, form.instance.portion_size
        )
        if error:
            form.add_error(None, error)
            return self.form_invalid(form)
        form.instance.calories = calories
        return super(AddTracker, self).form_valid(form)


class EditTracker(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit entered tracker"""

    template_name = "tracker/edit_tracker.html"
    model = Tracker
    form_class = TrackerForm
    success_url = "/tracker/"

    def test_func(self):
        return self.request.user.profile == self.get_object().user

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = self.request.user.profile
        form.instance.user = self.request.user.profile
        calories, error = fetch_calories(
            form.instance.title, form.instance.portion_size
        )
        if error:
            form.add_error(None, error)
            return self.form_invalid(form)
        form.instance.calories = calories
        return super(EditTracker, self).form_valid(form)


class DeleteTracker(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete entered tracker"""

    model = Tracker
    success_url = "/tracker/"

    def test_func(self):
        return self.request.user.profile == self.get_object().user
