from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import *
from account.decorators import *

def home(request):
    return render(request,'misc\home.html')




@patient_required
@login_required(login_url='/accounts/login')
def create(request):
	if request.method=='POST':
		if request.POST['title'] and request.POST['Addition']:
			diary = Diary()
			diary.title=request.POST['title']
			diary.Addition=request.POST['Addition']
			diary.pub_date=timezone.datetime.now()
			diary.user=request.user
			diary.save()
			return redirect('/diary/'+str(diary.id))

		else:
			return render(request,'misc/create.html',{ 'error':'All fields are required' })

	else:
		return render(request,'misc/create.html')


def detail(request,product_id):
	diary=get_object_or_404(Diary, pk=product_id)
	return render(request,'misc/detail.html',{'diary':diary})


def diary_all(request):
    diary=Diary.objects.all()
    return render(request,'misc/diary.html',{'diary':diary})



@therapist_required
@login_required(login_url='/accounts/login')
def comment(request,diary_id):
    diary=get_object_or_404(Diary, pk=diary_id)
    if request.method=='POST':
        form = CommentForm(request.POST)
        if request.POST['test']:
            comment = form.save(commit=False)
            comment.author=request.user
            comment.post=diary
            comment.save()
            return redirect('misc/detail', pk=diary.id)
        else:
            form=CommentForm()
        return render(request, 'misc/add_comment_to_post.html',{'form':form} )
