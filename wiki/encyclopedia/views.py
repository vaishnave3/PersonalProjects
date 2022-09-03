from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import Markdown
from django.urls import reverse 
markdowner = Markdown ()
import markdown
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display(request, title):
    content = util.get_entry(title)
    if content is None : 
        return render(request, "encyclopedia/pageunavail.html", {
            "title" : title
        })
    html = markdown.markdown(content) if content else None
    return render(request, "encyclopedia/display.html", {
        "title" : title,
        "entry" : html
    })

def search(request):
    if request.method == 'GET':
        name = request.GET.get('q')
        content = util.get_entry(name)
        html = markdown.markdown(content) if content else None
        titles = util.list_entries()
        entries = [] 
        for i in titles :
            if i.upper() == name.upper() :
                return render(request, "encyclopedia/display.html", {
                    "title" : name,
                    "entry" : html
                })
        for i in titles :
            if name.upper() in i.upper():
                entries.append(i)
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def newpage(request):
    return render(request, "encyclopedia/newpage.html",{
    })

def save(request):
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        strings = util.list_entries()
        for i in strings :
            if title == i :
                return render(request, "encyclopedia/alrexists.html",{
                    "title" : title
                })
        util.save_entry(title, text)

    return HttpResponseRedirect(reverse(index))

def edit(request, entry):
    entry2 = util.get_entry(entry)
    html = markdown.markdown(entry2) if entry else None
    return render(request, "encyclopedia/edit.html",{
        "title" : entry,
        "text" : html
    })
    
def saveedit(request, edit_title):
    if request.method == 'POST':
        text = request.POST['text']
        util.save_entry(edit_title, text)

    return HttpResponseRedirect(reverse(index))

def randompage(request):
    strings = util.list_entries()
    rand = random.choice(strings)
    return render(request, "encyclopedia/randompage.html",{
        "entry" : rand
    })