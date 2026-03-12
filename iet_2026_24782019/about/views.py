from django.shortcuts import render

# Pastikan nama fungsinya 'about_page'
def about_page(request):
    return render(request, 'about/about.html')