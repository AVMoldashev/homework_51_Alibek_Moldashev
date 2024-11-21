from django.shortcuts import render
from django.http import HttpResponseRedirect
from webapp.cat_db import CatDB
# Create your views here.


def index_view(request):
    return render(request, 'index.html')


def create_cat_view(request):
    name = request.POST.get('name').strip().capitalize()
    if name == "":
        return HttpResponseRedirect("/")
    cat = {
        'name': request.POST.get('name'),
        'age': 1,
        'food': 40,
        'happiness': 40,
        "picture": None,
        "is_sleeping": "НЕТ",
        "action": None
    }
    if cat["happiness"] > 30:
        cat["picture"] = "happy.jpg"
    elif 20 > cat["happiness"] < 30:
        cat["picture"] = "cat1.jpg"
    else:
        cat["picture"] = "sad_cat.jpg"
    CatDB.CAT = cat
    return HttpResponseRedirect("/display")

def display_cat(request):
    cat = {
       'name': CatDB.CAT["name"],
       'age': CatDB.CAT["age"],
       'food': CatDB.CAT["food"],
       'happiness': CatDB.CAT["happiness"],
       'is_sleeping': CatDB.CAT["is_sleeping"],
        "action": request.POST.get('action')
   }
    return render(request, 'cat_info.html', context={"cat": cat})


def action(request):
    CatDB.CAT = {
        'name': CatDB.CAT["name"],
        'age': CatDB.CAT["age"],
        'food': CatDB.CAT["food"],
        'happiness': CatDB.CAT["happiness"],
        'is_sleeping': CatDB.CAT["is_sleeping"],
        "action": request.POST.get('action')
    }
    if CatDB.CAT["action"] == "играть":
        if CatDB.CAT["is_sleeping"] == "ДА":
            CatDB.CAT["is_sleeping"] = "НЕТ"
            CatDB.CAT["happiness"] -= 5
        else:
            from random import randint
            rage = randint(1,3)
            if rage == 1:
                CatDB.CAT["happiness"] = 0
            else:
                CatDB.CAT["happiness"] += 15
            CatDB.CAT["food"] -= 10

    if CatDB.CAT["action"] == "кормить":
        if CatDB.CAT["is_sleeping"] == "ДА":
            pass
        else:
            CatDB.CAT["food"] += 15
            CatDB.CAT["happiness"] += 5
        if CatDB.CAT["food"] > 100:
            CatDB.CAT["happiness"] -= 30

    if CatDB.CAT["action"] == "спать":
        CatDB.CAT["is_sleeping"] = "ДА"
    return HttpResponseRedirect("/display")