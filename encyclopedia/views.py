import re
from markdown2 import markdown

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
        "entry": markdown(util.get_entry(title))
    })


def results(request):
    query = request.GET["q"]
    result = re.compile(query, re.I)
    expected = re.compile('\\b' + query + '\\b', re.I)
    results = list(filter(expected.search, util.list_entries()))
    if len(results) == 1:
        return HttpResponseRedirect(reverse("wiki", args=results))
    elif len(results) == 0:
        results = list(filter(result.search, util.list_entries()))
    return render(request, "encyclopedia/results.html", {
        "q": query,
        "results": results
    })


def new_page(request):
    return render(request, "encyclopedia/new_page.html", {
    })


def create_new_page(request):
    if request.method == "GET":
        checked = ""
        title = request.GET["title"]
        content = request.GET["content"]
        check = re.compile('\\b' + title + '\\b', re.I)
        if not title or not content:
            checked = "Invalid Request Made. Please Review Title and Content."
            return render(request, "encyclopedia/new_page.html", {
                "checked": checked
            })
        elif len(list(filter(check.match, util.list_entries()))) == 0:
            checked = "Saved..."
            util.save_entry(title, content)
            return render(request, "encyclopedia/new_page.html", {
                "checked": checked
            })
        else:
            checked = "TITLE already exists..."
            return render(request, "encyclopedia/new_page.html", {
                "checked": checked,
                "title": title,
                "content": content
            })
