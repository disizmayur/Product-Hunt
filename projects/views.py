from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import product
from django .utils import timezone
# Create your views here.
def home(request):
    products = product.objects
    return render(request, 'projects/home.html',{'products':products})
@login_required
def create(request):
    if request.method=="POST":
        if request.POST['title'] and  request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['icon'] :
            products=product()
            products.title=request.POST['title']
            products.body=request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('http://'):
                products.url=request.POST['url']
            else:
               products.url= 'http://' +request.POST['url']
            products.icon=request.FILES['icon']
            products.image=request.FILES['image']
            products.pub_date=timezone.datetime.now()
            products.hunter= request.user
            products.save()
            return redirect('/projects/'+ str(products.id))

        else:
            return render(request,'projects/create.html',{'error':"All fields are required"})
    return render(request,'projects/create.html')


def detail(request,products_id):
    products=get_object_or_404(product,pk=products_id)
    return render(request,'projects/detail.html',{'products':products})

@login_required(login_url="/accounts/signup")
def upvote(request, products_id):
    if request.method == 'POST':
        products = get_object_or_404(product, pk=products_id)
        products.votes_total += 1
        products.save()
        return redirect('/projects/' + str(products.id))