import markdown2
import random
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


class EntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def random_entry(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return HttpResponseRedirect(
        reverse("display_entry", kwargs={"title": random_title})
    )


def display_entry(request, title):
    entry_data = util.get_entry(title)
    if entry_data:
        html = markdown2.markdown(entry_data)
        return render(
            request, "encyclopedia/entry.html", {"title": title, "data": html}
        )
    else:
        return render(request, "encyclopedia/not-found.html", {"title": title})


def add(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                return render(request, "encyclopedia/exists.html", {"title": title})
            else:
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/add.html", {"form": form})
    return render(request, "encyclopedia/add.html", {"form": EntryForm()})


def edit(request, title):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(
                reverse("display_entry", kwargs={"title": title})
            )
        else:
            return render(
                request, "encyclopedia/edit.html", {"title": title, "form": form}
            )

    content = util.get_entry(title)
    pre_filled_form = EntryForm({"title": title, "content": content})
    return render(
        request, "encyclopedia/edit.html", {"title": title, "form": pre_filled_form}
    )
