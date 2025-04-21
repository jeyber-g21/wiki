from django.shortcuts import render
import markdown2
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def converter(title):
    content = util.get_entry(title)
    markdowner = markdown2.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    
def entry(request, title):
    html = converter(title)
    if html == None:
        return render(request, "encyclopedia/errormessage.html")
    else:
        return render (request, "encyclopedia/entry.html", {
            "title": title,"info": html
        })

def search(request):
    if request.method == "POST":
        entry_s = request.POST['q']
        html = converter(entry_s)
        if html is not None:
            return render (request, "encyclopedia/entry.html", {
            "title": entry_s,"info": html})
        else:
            entries = util.list_entries()
            similar = []
            for en in entries:
                if entry_s.lower() in en.lower():
                    similar.append(en)
                    return render (request, "encyclopedia/search.html",{
                        "similar" : similar
                    })
                if html == None:
                   return render(request, "encyclopedia/errormessage.html")
        
                
def new_page(request):  
    if request.method == "GET":
       return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST['title']
        info = request.POST['info']
        title_verif = util.get_entry(title)
        if title_verif is not None:
            return render(request, "encyclopedia/error_2.html",{
                "message":"The entry already exist"
            })
        else:
            util.save_entry(title, info)
            html = converter(title)
            return render(request, "encyclopedia/entry.html",{
                "title":title, "info":html
            })
        
def edit_info(request):
    if request.method == "POST":
        title = request.POST['new_info']
        info = util.get_entry(title)
    return render(request, "encyclopedia/edit.html",{
        "title":title,"info":info
    })

def save_edit (request):
    if request.method == "POST":
        title = request.POST['title']
        info = request.POST['info']
        util.save_entry(title, info)
        html = converter(title)
        return render(request, "encyclopedia/entry.html",{
                "title":title, "info":html
            })

def random_page(request):
    title = random.choice(util.list_entries())
    html = converter(title)
    if html is not None:
       return render (request, "encyclopedia/entry.html", {
            "title": title,"info": html
        })
