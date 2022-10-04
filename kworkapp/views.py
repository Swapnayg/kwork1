from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from re import sub
import smtplib
from tabnanny import verbose
from django.views import View
from urllib.parse import urlparse
import whatismyip
from django_countries import countries
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from django.core import serializers
import json
from kworkapp.models import Categories,UserGigPackages,UserGigPackage_Extra,UserExtra_gigs,Usergig_faq,Usergig_image,Usergig_requirement,Parameter,Category_package_Extra_Service,Category_package_Details, CharacterLimit,UserGigs,UserGigsTags, SellerLevels,Contactus, Languages, LearnTopics, LearningTopicCounts, LearningTopicDetails, SubCategories, SubSubCategories, TopicDetails, User,PageEditor, UserLanguages, UserProfileDetails, supportMapping, supportTopic
import operator


class indexView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'index.html')

class menu_pageView(View):
    return_url = None
    def get(self , request,category=''):
        category_details = Categories.objects.get(category_Name=category)
        sub_category = SubCategories.objects.filter(category_Name=category_details)
        return render(request , 'menu_page.html',{"details":category_details,"sub_details":sub_category})


class all_gigs_pageView(View):
    return_url = None
    def get(self , request,category='',subcategry='',topic=''):
        tagslist= []
        sub_sub_category = []
        if(len(subcategry)== 0):
            category_details = Categories.objects.get(category_Name=category)
            sub_categoryd = SubCategories.objects.get(category_Name=category_details,sub_category_Name=topic)
            sub_sub_category = SubSubCategories.objects.filter(category_Name=category_details,sub_category_Name=sub_categoryd)
            for sub in sub_sub_category:
                for sub_cat in sub.tags.all():
                    tagslist.append(sub_cat.name.strip())
        else:
            category_details = Categories.objects.get(category_Name=category)
            sub_categoryd = SubCategories.objects.get(category_Name=category_details,sub_category_Name=subcategry)
            sub_sub_category = SubSubCategories.objects.filter(category_Name=category_details,sub_category_Name=sub_categoryd)
            for sub in sub_sub_category:
                for sub_cat in sub.tags.all():
                    tagslist.append(sub_cat.name.strip())
        return render(request , 'gigs_page.html',{"details":category_details,"sub_details":sub_categoryd,"sub_topics":sub_sub_category,"tagslist":tagslist})

class aboutView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'about.html')

class privacyView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'privacy.html')

class gig_View_View(View):
    return_url = None
    def get(self , request,username='',gig_title=''):
        try:    
            userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
            languages = Languages.objects.exclude(lng_slug= u'english').order_by('lng_Name')
            userProfileDetails = UserProfileDetails.objects.get(user_id=userDetails)
            userlang = []
            english_profi = ''
            userlanguages = UserLanguages.objects.filter(user_id=userDetails)
            for lang in userlanguages:
                if(lang.language_name.lng_Name == "English"):
                    english_profi = lang.lang_prof
                userlang.append({"name":lang.language_name.lng_Name,"proficiency":lang.lang_prof})                  
            categories = Categories.objects.all()
            countrylist =[]
            for code, name in list(countries):
                countrylist.append({"name":name,"code":code})
            characters = []
            title_char=0
            overview_char = 0
            frontend_url = request.META.get('HTTP_REFERER')
            url1 = urlparse(frontend_url)
            charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="account_professional_overview") | Q(Char_category_Name= "account_title"))
            for c in charcterlimits:
                if(c.Char_category_Name == "account_title"):
                    title_char = c.Max_No_of_char_allowed
                elif(c.Char_category_Name == "account_professional_overview"):
                    overview_char = c.Max_No_of_char_allowed
        except:
            return render(request , 'register.html')
        return render(request , 'Dashboard/view_gig.html',{"Countrylist":countrylist,"languages":languages,"profile_Details":userProfileDetails,"userlanguages":userlang,"title_char":title_char,"overview_char":overview_char,"UserDetails":userDetails,"Categories":categories,'userlangs':json.dumps(userlang),"english_prof":english_profi,"current_url":str(str(url1.scheme) +"://"  + str(url1.netloc) )})

class buyer_protectionView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'buyer_protection.html')

class term_serviceView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'terms.html')

class for_freelancerView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'for_freelancer.html')

class earn_letorkbdoneView(View):
    return_url = None
    def get(self , request,username=''):
        learning_topics = LearnTopics.objects.all()
        learning_Details = []
        learning_topics_Details = LearningTopicDetails.objects.all()
        num_counts = 0
        for l_details in learning_topics_Details:
            num_counts = LearningTopicCounts.objects.filter(topic_name=l_details).count()
            learning_Details.append({"id":l_details.id,"topic_Name":l_details.topic_Name,"timeof_read_in_minute":l_details.timeof_read_in_minute,"topic_description":l_details.topic_description,"image":l_details.image,"image_Text":l_details.image_Text,"video_url":l_details.video_url,"num_counts":num_counts})
        return render(request , 'earn_letworkbdone.html',{"topics":learning_topics,"topics_Details":learning_Details})

class categoriesView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'categories.html')

class affiliate_programView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'affiliate_program.html')

class reviews_View(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'reviews.html')

class prohibited_service_View(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'prohibited_service.html')
    
class approval_process_View(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'approval_process.html')

class faq_View(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'faq.html')


class contact_support_View(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'contact_support.html')

class partners_View(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'partners.html')


class signup_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'register.html')

class login_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'login.html')

class profile_view(View):
    return_url = None
    def get(self , request,username=''):
        try: 
            userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
            languages = Languages.objects.exclude(lng_slug= u'english').order_by('lng_Name')
            userProfileDetails = UserProfileDetails.objects.get(user_id=userDetails)
            userlang = []
            english_profi = ''
            userlanguages = UserLanguages.objects.filter(user_id=userDetails)
            for lang in userlanguages:
                if(lang.language_name.lng_Name == "English"):
                    english_profi = lang.lang_prof
                userlang.append({"name":lang.language_name.lng_Name,"proficiency":lang.lang_prof})                  
            categories = Categories.objects.all()
            countrylist =[]
            for code, name in list(countries):
                countrylist.append({"name":name,"code":code})
            characters = []
            title_char=0
            overview_char = 0
            frontend_url = request.META.get('HTTP_REFERER')
            url1 = urlparse(frontend_url)
            charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="account_professional_overview") | Q(Char_category_Name= "account_title"))
            for c in charcterlimits:
                if(c.Char_category_Name == "account_title"):
                    title_char = c.Max_No_of_char_allowed
                elif(c.Char_category_Name == "account_professional_overview"):
                    overview_char = c.Max_No_of_char_allowed
        except:
            return render(request , 'register.html')
        return render(request , 'Dashboard/profile.html',{"Countrylist":countrylist,"languages":languages,"profile_Details":userProfileDetails,"userlanguages":userlang,"title_char":title_char,"overview_char":overview_char,"UserDetails":userDetails,"Categories":categories,'userlangs':json.dumps(userlang),"english_prof":english_profi,"current_url":str(str(url1.scheme) +"://"  + str(url1.netloc) )})      

class buyer_dashboard_view(View):
    return_url = None
    def get(self , request,username=''):
        request.session['userpage'] =	"buyer"
        return render(request , 'Dashboard/buyer_dashboard.html')


def logout_social(request):
    logout(request)
    return redirect('index')
    
class seller_dashboard_view(View):
    return_url = None
    def get(self , request,username=''):
        request.session['userpage'] =	"seller"
        return render(request , 'Dashboard/seller_dashboard.html')

class seller_main_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/seller_dashboard.html')

class Manage_request_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/manage_request.html')

class Manage_request_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/manage_request.html')

class post_request_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/post_request.html')

class billing_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/billing.html')

class refer_program_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'refer_earn.html')

class inbox_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/chat.html')

class favourites_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/favourites.html')

class create_gig_view(View):
    return_url = None
    def get(self , request,username='',gigid=0):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:  
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                characters = []
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="gig_title") | Q(Char_category_Name= "gig_package_title") | Q(Char_category_Name= "gig_package_description")  | Q(Char_category_Name= "gig_extra_title") | Q(Char_category_Name= "gig_extra_description")  | Q(Char_category_Name= "gig_description")  | Q(Char_category_Name= "gig_faq_question")  | Q(Char_category_Name= "gig_faq_answer")  | Q(Char_category_Name= "gig_requirements_ques") | Q(Char_category_Name= "gig_requirements_ans"))
                for c in charcterlimits:
                    if(c.Char_category_Name == "gig_title"):
                        characters.append({"gig_title":c.Max_No_of_char_allowed})
                    elif(c.Char_category_Name == "gig_package_title"):
                        characters.append({"gig_package_title":c.Max_No_of_char_allowed})
                    elif(c.Char_category_Name == "gig_package_description"):
                        characters.append({"gig_package_description":c.Max_No_of_char_allowed})
                    elif(c.Char_category_Name == "gig_extra_description"):
                        characters.append({"gig_extra_description":c.Max_No_of_char_allowed})
                    elif(c.Char_category_Name == "gig_extra_title"):
                        characters.append({"gig_extra_title":c.Max_No_of_char_allowed})
                    elif(c.Char_category_Name == "gig_description"):
                        characters.append({"gig_description":c.Max_No_of_char_allowed})
                    elif(c.Char_category_Name == "gig_faq_question"):
                        characters.append({"gig_faq_question":c.Max_No_of_char_allowed})
                    elif(c.Char_category_Name == "gig_faq_answer"):
                        characters.append({"gig_faq_answer":c.Max_No_of_char_allowed})
                    elif(c.Char_category_Name == "gig_requirements_ques"):
                        characters.append({"gig_requirements_ques":c.Max_No_of_char_allowed})
                    elif(c.Char_category_Name == "gig_requirements_ans"):
                        characters.append({"gig_requirements_ans":c.Max_No_of_char_allowed})
                    categorieslist = Categories.objects.all() 
                    delivery_time = []      
                    no_revisions = []   
                    extra_days = [] 
                    extra_time = []
                    delivery_time = Parameter.objects.filter(Q(parameter_name="delivery_time"))
                    no_revisions = Parameter.objects.filter(Q(parameter_name="no_revisions"))
                    extra_days = Parameter.objects.filter(Q(parameter_name="extra_days"))
                    extra_time = Parameter.objects.filter(Q(parameter_name="extra_time"))
                return render(request , 'Dashboard/create_gig.html',{"characters":characters,"category":categorieslist,"Delivery_Time":delivery_time,"No_Revisions":no_revisions,"Extra_Days":extra_days,"Extra_Time":extra_time})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')
        
class buyer_manage_orders_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/buyermanage_orders.html')

class seller_manage_orders_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/seller_manage_orders.html')

class buyer_request_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/buyer_request.html')

class manage_gigs_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:    
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                return render(request , 'Dashboard/manage_gigs.html',{"active_gigs":[1,2],"pending_gigs":[1],"require_modif":[1,2,3],"draft_gigs":[1,2,5,6],"denied_gigs":[1,2,5,6,5,9],"paused_gigs":[1,9,0,5,7,8,6,9]})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class earnings_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/earnings.html')

class order_activities_view(View):
    return_url = None
    def get(self , request,username='',orderid=''):
        return render(request , 'Dashboard/order_activity.html')
    
class resolution_view(View):
    return_url = None
    def get(self , request,username='',orderid=''):
        return render(request , 'Dashboard/resolution.html')

class account_settings_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:  
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                languages = Languages.objects.exclude(lng_slug= u'english').order_by('lng_Name')
                userProfileDetails = UserProfileDetails.objects.get(user_id=userDetails)
                userlang = []
                english_profi = ''
                userlanguages = UserLanguages.objects.filter(user_id=userDetails)
                for lang in userlanguages:
                    if(lang.language_name.lng_Name == "English"):
                        english_profi = lang.lang_prof
                    userlang.append({"name":lang.language_name.lng_Name,"proficiency":lang.lang_prof})                  
                categories = Categories.objects.all()
                countrylist =[]
                for code, name in list(countries):
                    countrylist.append({"name":name,"code":code})
                characters = []
                title_char=0
                overview_char = 0
                frontend_url = request.META.get('HTTP_REFERER')
                url1 = urlparse(frontend_url)
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="account_professional_overview") | Q(Char_category_Name= "account_title"))
                for c in charcterlimits:
                    if(c.Char_category_Name == "account_title"):
                        title_char = c.Max_No_of_char_allowed
                    elif(c.Char_category_Name == "account_professional_overview"):
                        overview_char = c.Max_No_of_char_allowed
                return render(request , 'Dashboard/account_settings.html',{"Countrylist":countrylist,"languages":languages,"profile_Details":userProfileDetails,"userlanguages":userlang,"title_char":title_char,"overview_char":overview_char,"UserDetails":userDetails,"Categories":categories,'userlangs':json.dumps(userlang),"english_prof":english_profi,"current_url":str(str(url1.scheme) +"://"  + str(url1.netloc) )})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class dashboard_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:   
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)            
                truefactor = ''
                try:
                    if(len(userDetails.profile_type) == 0):
                        truefactor = 'true'
                    elif(userDetails.profile_type == None):
                        truefactor = 'true'
                except:
                    truefactor = 'true'
                if(truefactor == 'true'):
                    languages = Languages.objects.exclude(lng_slug= u'english').order_by('lng_Name')
                    userProfileDetails = UserProfileDetails.objects.get(user_id=userDetails)
                    userlang = []
                    english_profi = ''
                    userlanguages = UserLanguages.objects.filter(user_id=userDetails)
                    for lang in userlanguages:
                        if(lang.language_name.lng_Name == "English"):
                            english_profi = lang.lang_prof
                        userlang.append({"name":lang.language_name.lng_Name,"proficiency":lang.lang_prof})                  
                    categories = Categories.objects.all()
                    countrylist =[]
                    for code, name in list(countries):
                        countrylist.append({"name":name,"code":code})
                    characters = []
                    title_char=0
                    overview_char = 0
                    frontend_url = request.META.get('HTTP_REFERER')
                    url1 = urlparse(frontend_url)
                    charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="account_professional_overview") | Q(Char_category_Name= "account_title"))
                    for c in charcterlimits:
                        if(c.Char_category_Name == "account_title"):
                            title_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name == "account_professional_overview"):
                            overview_char = c.Max_No_of_char_allowed
                    request.session['userpage'] =	"seller"
                    return render(request , 'Dashboard/account_settings.html',{"Countrylist":countrylist,"languages":languages,"profile_Details":userProfileDetails,"userlanguages":userlang,"title_char":title_char,"overview_char":overview_char,"UserDetails":userDetails,"Categories":categories,'userlangs':json.dumps(userlang),"english_prof":english_profi,"current_url":str(str(url1.scheme) +"://"  + str(url1.netloc) )})
                elif(userDetails.profile_type== "Buyer"):
                    request.session['userpage'] =	"buyer"
                    return render(request , 'Dashboard/buyer_dashboard.html')
                elif(userDetails.profile_type== "Seller"):
                    request.session['userpage'] =	"seller"
                    return render(request , 'Dashboard/seller_dashboard.html')
                else:
                    return render(request , 'register.html')
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')
                
@csrf_exempt
def save_content_view(request):
    if request.method == 'POST':
        ucontent = request.POST.get("ucontent")
        upageName = request.POST.get("upageName")
        htmlcontent = ''
        with open("kworkapp/templates/"+upageName + '.html', 'r') as f:
            htmlcontent = f.read()
        soup=BeautifulSoup(htmlcontent,'html.parser')
        soup.find('div',attrs={"class":"all_page"}).replace_with(ucontent)
        with open("kworkapp/templates/"+upageName + '.html', "w", encoding = 'utf-8') as file:
            file.write(HTMLParser().unescape(str(soup.prettify()).replace("&lt;","<").replace("&gt;",">").replace("&nbsp;"," ").replace("&amp;","&").replace("&quot;",'"').replace("&apos;","'").replace("&cent;","¢").replace("&pound;","£").replace("&yen;","¥").replace("&euro;","€").replace("&copy;","©").replace("&reg;","®").replace("a&#769;","`").replace("a&#770;","^").replace("a&#771;","~").replace("a&#771;","~")))
        return HttpResponse('sucess')

@csrf_exempt
def Imgupload_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist("files") 
        urls = []
        if len(files) != 0:
            for file in files:
                fs= FileSystemStorage(location= settings.MEDIA_ROOT +'/images/')
                file_path=fs.save(file.name.replace(' ','_'),file) 
                url = '/media/images/'+file_path
                urls.append(url)
        else:
            print('No File') 
        responseData = {'data':urls}
        return JsonResponse(responseData,safe=False)

@csrf_exempt
def get_menus_view(request):
    if request.method == 'GET':
        umenuname = request.GET['umenuname']
        data = []
        if(umenuname == "start"):
            menulist = list(supportTopic.objects.order_by().values_list('topic_category').distinct())
            for m in menulist:
                if ''.join(map(str, m)).find("- ") == -1:
                    data.append({"title":str(''.join(map(str, m))),"actual_name":str(''.join(map(str, m))),"has_child":1})
        else:
            suport_topic = supportTopic.objects.get(support_topic_Name = umenuname)
            menulist = list(supportMapping.objects.filter(suport_topic = suport_topic))
            for m in menulist:
                child = ''
                child_topic = supportTopic.objects.get(support_topic_Name = m.map_to.support_topic_Name)
                childlist = list(supportMapping.objects.filter(suport_topic = child_topic))
                if(len(childlist) > 0):
                    child = "1"
                else:
                    child = "0"
                title_name = ''
                if str(m.map_to.support_topic_Name).find("- ") == -1:
                    title_name = m.map_to.support_topic_Name
                else:
                    title_namelist = m.map_to.support_topic_Name.split("-")
                    title_name = title_namelist[1].strip()
                data.append({"title":title_name,"actual_name":m.map_to.support_topic_Name,"has_child":child})
        data.sort(key=operator.itemgetter('title'))
        return JsonResponse(data,safe=False)


@csrf_exempt
def get_menus_data_view(request):
    if request.method == 'GET':
        umenuname = request.GET['umenuname']
        data = []
        try:
            suport_topic = supportTopic.objects.get(support_topic_Name = umenuname)
            data1 = TopicDetails.objects.filter(topic_Name = suport_topic)
            for d in data1:
                data.append({"title":d.topic_Name.support_topic_Name,"contents":d.topic_Desc})
        except:
            data = []
        return JsonResponse(data,safe=False)

def SendEmailAct(sendto,message,subject):
    sender_address = 'info@letworkbedone.com'
    sender_password = 'xu11yC%5DF=Q'
    themsg = MIMEMultipart()
    themsg['Subject'] = subject
    themsg['To'] = sendto
    themsg['From'] = sender_address
    themsg.attach(MIMEText(message, 'html'))
    themsg = themsg.as_string()
    smtp = smtplib.SMTP_SSL('letworkbedone.com', 465)
    smtp.login(sender_address, sender_password)
    smtp.sendmail(sender_address, sendto, themsg)
    smtp.quit()
    return "mail Sent" 

@csrf_exempt
def post_contact_support_view(request):
    if request.method == 'GET':
        uemail_address = request.GET['uemail_address']
        uform_message = request.GET['uform_message']
        contact_us = Contactus(email=uemail_address,message=uform_message)
        contact_us.save()
        ticket = contact_us.id
        mail_content = """
<!doctype html>
<html lang="en-US">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <title>Let'sworkbedone - Reset Password</title>
    <meta name="description" content="Reset Password Email Template.">
    <style type="text/css">
        a:hover {text-decoration: underline !important;}
    </style>
</head>

<body marginheight="0" topmargin="0" marginwidth="0" style="margin: 0px; background-color: #f2f3f8;" leftmargin="0">
    <table cellspacing="0" border="0" cellpadding="0" width="100%" bgcolor="#f2f3f8"
        style="@import url(https://fonts.googleapis.com/css?family=Rubik:300,400,500,700|Open+Sans:300,400,600,700); font-family: 'Open Sans', sans-serif;">
        <tr>
            <td>
                <table style="background-color: #f2f3f8; max-width:670px;  margin:0 auto;" width="100%" border="0"
                    align="center" cellpadding="0" cellspacing="0">
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                          <a href="https://letworkbedone.com/" title="logo" target="_blank">
                            <img width="250" src="https://i.ibb.co/2ghjzv2/logo.png" title="logo" alt="logo">
                          </a>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td>
                            <table width="95%" border="0" cellpadding="0" cellspacing="0"
                                style="max-width:670px;background:#fff; border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);box-shadow:0 6px 18px 0 rgba(0,0,0,.06);">
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                                <tr>
                                    <td style="text-align:center;">
                                        <h1 style="color:#1e1e2d; font-weight:500; margin:0;font-size:32px;font-family:'Rubik',sans-serif;">Letsworkbedone Support</h1>
                                    </td>
                                </tr>
                                <tr style="text-align:left;">
                                  <td style="">    <span style="display:inline-block; vertical-align:middle; Padding:15px;">Thank you for contacting Letsworkbedone Support. Your request ("""+ticket+""") has been received and will be reviewed by our support staff.</span>
    <span style="display:inline-block; vertical-align:middle; Padding:15px;"> Kindly note that our email support hours are from 8:00AM to 7:00PM (Saturday to Thursday) and we will attempt to get back to you as soon as possible during business hours.</span>
	  <span style="display:inline-block; vertical-align:middle; Padding:15px;"> You can add additional comments to your request by replying to this email.</span>
	    
  </td> 
                                </tr>
								<tr style="text-align:left;">
                                   <span style="display:inline-block; vertical-align:middle; Padding:15px;">Thank you</span>
								</tr>
								<tr style="text-align:left;">
                               <span style="display:inline-block; vertical-align:middle; Padding:15px;">Support</span>
								</tr>
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                            </table>
                        </td>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                            <p style="font-size:14px; color:rgba(69, 80, 86, 0.7411764705882353); line-height:18px; margin:0 0 0;">&copy; <strong>www.letsworkbedone.com</strong></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body></html>"""

        mail_contentAdmin = """
<!doctype html>
<html lang="en-US">

<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <title>Let'sworkbedone - Reset Password</title>
    <meta name="description" content="Reset Password Email Template.">
    <style type="text/css">
        a:hover {text-decoration: underline !important;}
    </style>
</head>

<body marginheight="0" topmargin="0" marginwidth="0" style="margin: 0px; background-color: #f2f3f8;" leftmargin="0">
    <table cellspacing="0" border="0" cellpadding="0" width="100%" bgcolor="#f2f3f8"
        style="@import url(https://fonts.googleapis.com/css?family=Rubik:300,400,500,600|Open+Sans:300,400,600,600); font-family: 'Open Sans', sans-serif;">
        <tr>
            <td>
                <table style="background-color: #f2f3f8; max-width:670px;  margin:0 auto;" width="100%" border="0"
                    align="center" cellpadding="0" cellspacing="0">
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                          <a href="https://letworkbedone.com/" title="logo" target="_blank">
                            <img width="250" src="https://i.ibb.co/2ghjzv2/logo.png" title="logo" alt="logo">
                          </a>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td>
                            <table width="95%" border="0" cellpadding="0" cellspacing="0"
                                style="max-width:670px;background:#fff; border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 14px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 14px 0 rgba(0,0,0,.06);box-shadow:0 6px 14px 0 rgba(0,0,0,.06);">
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                                <tr>
                                    <td style="text-align:center;">
                                        <h1 style="color:#1e1e2d; font-weight:500; margin:0;font-size:32px;font-family:'Rubik',sans-serif;">Contact Received From:</h1>
                                    </td>
                                </tr>
                                <tr style="text-align:left;">
                                  <td style=""><span style="display:inline-block; vertical-align:middle; Padding:20px;"><span style="font-weight:600;font-size:14px;">Ticket Number :</span> """+ticket+"""</span></td> 
                                </tr>
                                <tr style="text-align:left;">
                                 <span style="display:inline-block; vertical-align:middle; Padding:20px;"><span style="font-weight:600;font-size:14px;">Email Address :</span> """+uemail_address+"""</span>
								</tr>
								<tr style="text-align:left;">
                                <span style="display:inline-block; vertical-align:middle; Padding:20px;"><span style="font-weight:600;font-size:14px;">Message :</span> """+uform_message.capitalize()+"""</span>
								</tr>
								<tr style="text-align:left;">
                                <span style="display:inline-block; vertical-align:middle; Padding:20px;">Thank you.</span>
								</tr>
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                            </table>
                        </td>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                            <p style="font-size:14px; color:rgba(69, 80, 86, 0.7411764705882353); line-height:14px; margin:0 0 0;">&copy; <strong>www.letsworkbedone.com</strong></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>

</html>"""
        SendEmailAct(uemail_address,mail_content,"Letworkbedone - Contact Received")
        SendEmailAct("info@letworkbedone.com",mail_contentAdmin,"Letworkbedone - Contact Received")
        return HttpResponse('success')

def get_articles_view(request):
    if request.method == 'GET':
        data = []
        support_list = []
        article_name = request.GET['article_name']
        try:
            suport_topic = supportTopic.objects.filter(support_topic_Name__contains=article_name)
            pathlists = []
            for support in suport_topic:
                suport_topic = supportTopic.objects.get(support_topic_Name = support.support_topic_Name)
                data1 = TopicDetails.objects.get(topic_Name = int(suport_topic.id))
                support_list.append(support.support_topic_Name)
                data.append({"title":data1.topic_Name.support_topic_Name,"contents":data1.topic_Desc})
        except:
            data = []
            support_list = []
        return JsonResponse(data,safe=False)

def subcategories_for_category_view(request):
    if request.method == 'GET':
        category_id = request.GET['category_id']
        category = Categories.objects.get(id = category_id)
        sub_category = SubCategories.objects.filter(category_Name=category)
        tmpJson = serializers.serialize("json",sub_category)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))


def post_increase_count_view(request):
    if request.method == 'GET':
        ulesson_id = request.GET['ulesson_id']
        uip_address = str(whatismyip.whatismyip())
        topic_details = LearningTopicDetails.objects.get(pk = ulesson_id)
        num_counts = 0
        if(LearningTopicCounts.objects.filter(topic_name=topic_details,ip_address=uip_address).exists() == False):
            learning_topic = LearningTopicCounts(topic_name=topic_details,ip_address=uip_address)
            learning_topic.save()
        num_counts = LearningTopicCounts.objects.filter(topic_name=topic_details).count()
    return HttpResponse(num_counts)

def get_all_categories_view(request):
    if request.method == 'GET':
        data = []
        main_categories = []
        sub_categories =[]
        all_categories = []
        category_list = Categories.objects.all()
        for category in category_list:
            category_inst = Categories.objects.get(category_Name=category.category_Name)
            main_categories.append({"category":category.category_Name})
            sub_cagetory_list = SubCategories.objects.filter(category_Name = category_inst)
            for sub_category in sub_cagetory_list:
                sub_category_inst = SubCategories.objects.get(category_Name=category_inst, sub_category_Name = sub_category.sub_category_Name)
                sub_sub_cagetory_list = SubSubCategories.objects.filter(category_Name = category_inst,sub_category_Name= sub_category_inst)                    
                for sub_sub_category in sub_sub_cagetory_list:
                    all_categories.append({"category":category.category_Name,"subcategory":sub_category.sub_category_Name,"subsubcategory":sub_sub_category.sub_sub_category_Name})
                sub_categories.append({"category":category.category_Name,"subcategory": sub_category.sub_category_Name,"lengthsubmenu":len(sub_sub_cagetory_list)})
        data = {'main_menu' : json.dumps(main_categories),'sub_menu' : json.dumps(sub_categories),'sub_sub_menu' : json.dumps(all_categories)}
        return JsonResponse(json.dumps(data),safe=False)


def get_sub_categories_view(request):
    if request.method == 'GET':
        data = []
        usub_category = request.GET['sub_category']
        category = Categories.objects.get(category_Name=usub_category)
        sub_categories = SubCategories.objects.filter(category_Name=category)
        for sub_cat in sub_categories:
            data.append({'sub_cat_name':sub_cat.sub_category_Name,'sub_cat_id':sub_cat.id})
        return JsonResponse(data,safe=False)

@csrf_exempt
def Prof_image_upload_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist("files")
        userid =  request.POST.get("user_id")
        userDetails = User.objects.get(pk=userid)
        frontend_url = request.META.get('HTTP_REFERER')
        url1 = urlparse(frontend_url)
        urls = []
        if len(files) != 0:
            for file in files:
                fs= FileSystemStorage(location= settings.MEDIA_ROOT +'/profile/')
                file_path=fs.save(file.name.replace(' ','_'),file) 
                url = '/media/profile/'+file_path
                urls.append(url)
                userDetails.avatar = url1.scheme +"://"  + url1.netloc  + url
                userDetails.save()
        else:
            print('No File') 
        responseData = {'data':urls}
        return JsonResponse(responseData,safe=False)

def post_user_Details_view(request):
    if request.method == 'GET':
        usercountry = request.GET['usercountry']
        userrole = request.GET['userrole']
        userterms = request.GET['userterms']
        userid = request.GET['userid']
        term_val = ''
        if userterms == "true": term_val = True
        else:
            term_val = False
        userDetails = User.objects.get(pk=userid)
        userDetails.country = usercountry
        userDetails.terms = term_val
        userDetails.profile_type = userrole
        userDetails.save()
    return HttpResponse("success")

def post_useremail_Details_view(request):
    if request.method == 'GET':
        useremail = request.GET['useremail']
        usercountry = request.GET['usercountry']
        userrole = request.GET['userrole']
        userterms = request.GET['userterms']
        userid = request.GET['userid']
        term_val = ''
        if userterms == "true": term_val = True
        else:
            term_val = False
        userDetails = User.objects.get(pk=userid)
        userDetails.email = useremail
        userDetails.country = usercountry
        userDetails.terms = term_val
        userDetails.profile_type = userrole
        userDetails.save()
    return HttpResponse("success")


def post_user_category_view(request):
    if request.method == 'GET':
        ucategory = request.GET['ucategory']
        usubcategory = request.GET['usubcategory']
        userid = request.GET['userid']
        userDetails = User.objects.get(pk=userid)
        category_int = Categories.objects.get(id=ucategory)
        sub_category_int = SubCategories.objects.get(id=usubcategory)
        userprofile = UserProfileDetails.objects.get(user_id=userDetails)
        userprofile.main_category = category_int
        userprofile.sub_category = sub_category_int
        userprofile.save()
    return HttpResponse("success")

@csrf_exempt
def post_user_languages_view(request):
    if request.method == 'POST':
        ulanguages = request.POST['ulanguages']
        userid =  request.POST.get("userid")
        userDetails = User.objects.get(pk=userid)
        data = json.loads(ulanguages)
        UserLanguages.objects.filter(user_id=userDetails).delete()
        for d in data:
            name = d['name']
            value = d['value']
            langua_inst = Languages.objects.get(lng_slug=name)
            user_lang = UserLanguages(language_name=langua_inst,lang_prof=value,user_id=userDetails)
            user_lang.save()
    return HttpResponse("success")


def post_user_overview_view(request):
    if request.method == 'GET':
        utitle = request.GET['utitle']
        uoverview = request.GET['uoverview']
        userid = request.GET['userid']
        userDetails = User.objects.get(pk=userid)
        userprofile = UserProfileDetails.objects.get(user_id=userDetails)
        userprofile.profile_title = utitle
        userprofile.profess_overview = uoverview
        userprofile.save()
    return HttpResponse("success")



def post_create_gig_view(request):
    if request.method == 'GET':
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:    
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                numberof_gigs = SellerLevels.objects.get(level_name=str(userDetails.seller_level))
                gigs_used = 0
                gig_id = 0
                if(UserGigs.objects.filter(user_id=userDetails).exists() == True):
                    gigs_used = UserGigs.objects.filter(user_id=userDetails).count()
                if(gigs_used == int(numberof_gigs.No_of_gigs)):
                    gig_id = 0
                else:
                    user_gig_obj = UserGigs(user_id=userDetails)
                    user_gig_obj.save()
                    gig_id = int(user_gig_obj.pk)
                return HttpResponse(gig_id)
            except:
                return HttpResponse('error')
        else:
            return HttpResponse('error')
        
        
def post_sub_category_details_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        select_id = request.GET['select_id']
        userDetails = User.objects.get(pk=userid)
        sub_subcatDetails = []
        category_inst = Categories.objects.get(id=select_id)
        _subcatDetails = SubSubCategories.objects.filter(category_Name= category_inst)
        for subcat in _subcatDetails:
            sub_subcatDetails.append({"cat_name":subcat.sub_sub_category_Name,"cat_id":subcat.id})
        return JsonResponse(sub_subcatDetails,safe=False)



def post_tags_category_details_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        category_id = request.GET['category_id']
        sub_category_id = request.GET['sub_category_id']
        userDetails = User.objects.get(pk=userid)
        taglist = []
        sub_category_inst = SubSubCategories.objects.get(id=sub_category_id)
        for tag in sub_category_inst.tags.all():
            taglist.append({"text":tag.name,"value":tag.name})
        category_packages = []
        extra_category_packages = []
        package_inst = Category_package_Details.objects.filter(category_name=sub_category_inst)
        for pckg in package_inst:
            category_packages.append({"package_name":pckg.display_name,"package_type":pckg.display_type,"helper_txt":pckg.helper_txt})
        extra_package_inst = Category_package_Extra_Service.objects.filter(category_name=sub_category_inst)
        for extra_pckg in extra_package_inst:
            extra_category_packages.append({"e_package_name":extra_pckg.display_name,"e_package_type":extra_pckg.display_type,"e_helper_txt":extra_pckg.helper_txt})
        responseData = {'tagsOPbj':taglist,'pckgObj':category_packages,'extraPckgObj':extra_category_packages}
        return JsonResponse(responseData,safe=False)




