from django.test import TestCase

# Create your tests here.
class SingnupView(generic.View):
    def get(self,request):
        context = {
        'form':CreateUserForm(),
        }
        return render(request,'account/signup.html',context)
    def post(self,request):
        
        form=CreateUserForm(request.POST) 
       
	      
        if form.is_valid():
            user=form.save(commit=False)
            email = request.POST.get('email')
            email_check=User.objects.filter(email=user.email)
            
            if email_check.count():
                messages.error(request,'This email already exists')
                return render(request,'account/signup.html',{'form':form})
            else:
                name=user.first_name
                user.username=name
                user.first_name=name.split(' ')[0]
                user.last_name=name.split(' ')[-1]
                user.is_active = False # Deactivate account till it is confirmed
                user.save()
                current_site = get_current_site(request=request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('account/active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })
                send_email = EmailMessage(mail_subject, message, to=[email])
                send_email.send()
                messages.success(
                    request=request,
                    message="Please confirm your email address to complete the registration"
                )
                return redirect('app_user:signup')
        
                
        else:
            messages.success(request,'Please fill in the correct information')
            return redirect('app_user:signup')
 

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
            # user is valid and active -> is_active
            # request.user == user
                login(request, user)
                return redirect("/")
        else:
            messages.error(request,'This email already exists')
            return redirect("/")
    return render(request, "account/signin.html", {"form": form})


def activate(request, uidb64, token):