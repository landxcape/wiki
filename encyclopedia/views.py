import re

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "entry": util.get_entry(title)
    })


def results(request):
    query = request.GET["q"]
    result = re.compile(query, re.I)
    results = list(filter(result.search, util.list_entries()))
    if len(results) == 1 and re.match('\\b' + query + '\\b', results[0], re.I):
        return HttpResponseRedirect(reverse("wiki", args=results))
    return render(request, "encyclopedia/results.html", {
        "q": query,
        "results": results
    })
