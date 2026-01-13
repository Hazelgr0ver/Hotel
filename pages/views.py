from django.shortcuts import render


def about(request):
    return render(request, 'pages/about.html')


def rules(request):
    return render(request, 'pages/rules.html')


def contacts(request):
    return render(request, 'pages/contacts.html')


def gallery(request):
    return render(request, 'pages/gallery.html')
