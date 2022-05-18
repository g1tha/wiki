from cProfile import label
from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.forms import ModelForm, TextInput, Textarea
from random import randint
# Refer to models.py
from encyclopedia.models import NewPageModel

from . import util

class NewPageForm(ModelForm):
    """Creates form for a new page based NewPageModel in models.py to allow users to create and edit pages."""
    class Meta:
        model = NewPageModel
        fields = ['name', 'contents']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Enter name of page.', 'class': 'form-control', 'autocomplete': 'off'}),
            'contents': Textarea(attrs={'placeholder': "Enter title and contents for page in markdown language.", 'class': 'form-control'})
        }

def index(request):
    """Returns page index with list of entries."""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, name):
    """Renders articles from entries .md files, given a case-insensitive address in path."""
    entries = util.list_entries()
    for title in entries:
        if name.lower() == title.lower():
            markdowntext = util.get_entry(title)
            entry = Markdown().convert(markdowntext)
            name = title
            return render(request, "encyclopedia/article.html", {
                "entry": entry,
                "markdowntext": markdowntext,
                "title": name
            })
    return render(request, "encyclopedia/notfounderror.html", {
        "name": name
    })

def search(request):
    """Returns an article page if query is a direct match, otherwise returns a list of articles where query is a substring."""
    query = request.GET.get('q')
    entries = util.list_entries()
    results = []
    for title in entries:
        if query.lower() == title.lower():
            return HttpResponseRedirect(query)
        if query.lower() in title.lower():
            results.append(title)
    return render(request, "encyclopedia/search.html", {
    "entries": util.list_entries(),
    "results": results
    })

def newpage(request):
    """Allows users to create a new page, using NewPageForm. If name matches existing entry, user directed to error page with link to existing page which can be edited."""
    if request.method == "POST":
        form = NewPageForm(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            name = form.cleaned_data["name"]
            contents = form.cleaned_data["contents"]
            for entry in entries:
                if name.lower() == entry.lower():
                    return render(request, "encyclopedia/editerror.html", {
                        "name": name
                        })
                util.save_entry(name, contents)
                return HttpResponseRedirect('/wiki/' + name)
               
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })

def edit(request):
    """Edit function for edit links in articles. Requires csrftoken to prevent users navigating to function through address bar."""
    name = request.POST.get("title")
    csrftoken = request.POST.get("csrfmiddlewaretoken")
    contents = util.get_entry(name)
    data = {'name': name, 'contents': contents}
    if csrftoken:
        return render(request, "encyclopedia/editpage.html", {
            "form": NewPageForm(initial=data)
            })
    else:
        return HttpResponseRedirect('/') 

def editpage(request):
    """Allows users to submit a form to edit an existing article."""
    form = NewPageForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        contents = form.cleaned_data["contents"]
        util.save_entry(name, contents)
        return HttpResponseRedirect('/wiki/' + name)

def random(request):
    """Redirects users to a random page."""
    entries = util.list_entries()
    i = randint(0, len(entries) - 1)
    name = entries[i]
    return HttpResponseRedirect('/wiki/' + name)

