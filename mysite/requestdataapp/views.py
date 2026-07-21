from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def process_get_view(request:HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
       "a": a,
        "b": b,
        "result": result,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)

def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, "requestdataapp/user-bio-form.html")

MAX_UPLOAD_SIZE = 10 * 1024  # 10 KB
def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES["myfile"]

        if myfile.size > MAX_UPLOAD_SIZE:
            return render(
                request,
                "requestdataapp/file-upload.html",
                {
                    "error": f"Файл слишком большой. Максимальный размер — "
                             f"{MAX_UPLOAD_SIZE} байт (10 КБ), "
                             f"а ваш файл — {myfile.size} байт."
                },
                status=400,
            )

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print("saved file", filename)

    return render(request, "requestdataapp/file-upload.html")