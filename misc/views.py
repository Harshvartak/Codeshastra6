from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import *
from account.decorators import *
from .logic import sendmail
import requests


def home(request):
    return render(request,'misc\home.html')


def home2(request):
    return render(request,'misc\home2.html')



@patient_required
@login_required(login_url='/accounts/login')
def create(request):
    if request.method=='POST':
        if request.POST['title'] and request.POST['Addition']:
            diary = Diary()
            diary.title=request.POST['title']
            text = request.POST['Addition']
            diary.Addition=request.POST['Addition']
            diary.pub_date=timezone.datetime.now()
            diary.user=request.user
            diary.save()
            URL = ' https://1hm9dv9vtg.execute-api.ap-south-1.amazonaws.com/prod'

            data = {
              "body": text,
              "resource": "/{proxy+}",
              "path": "/path/to/resource",
              "httpMethod": "POST",
              "isBase64Encoded": True,
              "queryStringParameters": {
                "foo": "bar"
              },
              "multiValueQueryStringParameters": {
                "foo": [
                  "bar"
                ]
              },
              "pathParameters": {
                "proxy": "/path/to/resource"
              },
              "stageVariables": {
                "baz": "qux"
              },
              "headers": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "en-US,en;q=0.8",
                "Cache-Control": "max-age=0",
                "CloudFront-Forwarded-Proto": "https",
                "CloudFront-Is-Desktop-Viewer": "true",
                "CloudFront-Is-Mobile-Viewer": "false",
                "CloudFront-Is-SmartTV-Viewer": "false",
                "CloudFront-Is-Tablet-Viewer": "false",
                "CloudFront-Viewer-Country": "US",
                "Host": "1234567890.execute-api.ap-south-1.amazonaws.com",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Custom User Agent String",
                "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
                "X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==",
                "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
                "X-Forwarded-Port": "443",
                "X-Forwarded-Proto": "https"
              },
              "multiValueHeaders": {
                "Accept": [
                  "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
                ],
                "Accept-Encoding": [
                  "gzip, deflate, sdch"
                ],
                "Accept-Language": [
                  "en-US,en;q=0.8"
                ],
                "Cache-Control": [
                  "max-age=0"
                ],
                "CloudFront-Forwarded-Proto": [
                  "https"
                ],
                "CloudFront-Is-Desktop-Viewer": [
                  "true"
                ],
                "CloudFront-Is-Mobile-Viewer": [
                  "false"
                ],
                "CloudFront-Is-SmartTV-Viewer": [
                  "false"
                ],
                "CloudFront-Is-Tablet-Viewer": [
                  "false"
                ],
                "CloudFront-Viewer-Country": [
                  "US"
                ],
                "Host": [
                  "0123456789.execute-api.ap-south-1.amazonaws.com"
                ],
                "Upgrade-Insecure-Requests": [
                  "1"
                ],
                "User-Agent": [
                  "Custom User Agent String"
                ],
                "Via": [
                  "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)"
                ],
                "X-Amz-Cf-Id": [
                  "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA=="
                ],
                "X-Forwarded-For": [
                  "127.0.0.1, 127.0.0.2"
                ],
                "X-Forwarded-Port": [
                  "443"
                ],
                "X-Forwarded-Proto": [
                  "https"
                ]
              },
              "requestContext": {
                "accountId": "123456789012",
                "resourceId": "123456",
                "stage": "prod",
                "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
                "requestTime": "09/Apr/2015:12:34:56 +0000",
                "requestTimeEpoch": 1428582896000,
                "identity": {
                  "cognitoIdentityPoolId": None,
                  "accountId": None,
                  "cognitoIdentityId": None,
                  "caller": None,
                  "accessKey": None,
                  "sourceIp": "127.0.0.1",
                  "cognitoAuthenticationType": None,
                  "cognitoAuthenticationProvider": None,
                  "userArn": None,
                  "userAgent": "Custom User Agent String",
                  "user": None
                },
                "path": "/prod/path/to/resource",
                "resourcePath": "/{proxy+}",
                "httpMethod": "POST",
                "apiId": "1234567890",
                "protocol": "HTTP/1.1"
              }
            }
            r = requests.post(url = URL, data = data)
            if r.json() == 0.0:
                sendmail('khandorvatsal@gmail.com','Vatsal','Harsh needs attention!','<p>According to our model, Harsh wrote a rather negative/abnormal diary entry.Try talking to him for a bit?</p><p>Regards,<br>Team PsychoSaiyan')
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
def comment(request, pk):
    post = get_object_or_404(Diary, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.psychiatrist=request.user
            comment.save()
            return redirect('detail2',product_id=pk)
    else:
        form = CommentForm()
    return render(request, 'misc/add_comment_to_post.html', {'form': form})



def detail2(request,product_id):
	diary=get_object_or_404(Diary, pk=product_id)
	return render(request,'misc/detail2.html',{'diary':diary})


def diary_all2(request):
    diary=Diary.objects.all()
    return render(request,'misc/diary2.html',{'diary':diary})


def quiz(request):
    return render(request,'misc/quiz.html')


def score(request):
    sum = 0
    for i in range(1,15):
        sum+=int(request.POST.get('w{}'.format(i),False))
    name = 'Ritik'
    sendmail('ritikpmota@gmail.com',name,'Your score!','<p>Good work taking the test again! Here is your score:</p><p><b><u>{} out of 70.</b></u></p><p>Keep taking these tests to gove you and your therapist regular updates of how youre doing!'.format(sum))
    sendmail('govind.thakur11@gmail.com','Govind','Score update on {}'.format(name),'<p>The patient just took the quiz again, and the score is:</p><p><b><u>{} out of 70.</b></u></p><p>Like always, we leave it to you to take the next call.'.format(sum))
    return render(request, 'misc/score.html',{'score':sum})



@therapist_required
@login_required(login_url='/accounts/login')
def Assign(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.creator=request.user
            comment.save()
            return redirect('display')
    else:
        form = TaskForm()
    return render(request, 'misc/task_assign.html', {'form': form})





@login_required(login_url='/accounts/login')
def display(request):
    task=Task.objects.all()
    return render(request,'misc/task.html',{'task':task})



@login_required(login_url='/accounts/login')
def display2(request):
    task=Task.objects.all()
    return render(request,'misc/task2.html',{'task':task})


def done2(request,pk):
    task=get_object_or_404(Task, pk=pk)
    task.is_complete=True
    task.save()
    task2=Task.objects.all()
    return render(request,'misc/task2.html',{'task':task2})
