from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def contacts(request):
    if request.method == 'POST':
        # Обработка данных формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Получено сообщение от {name} ({phone}): {message}")

    return render(request, 'contacts.html')