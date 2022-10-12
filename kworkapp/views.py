from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from re import sub
import smtplib
from datetime import datetime, timedelta
from dateutil import relativedelta
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
from kworkapp.models import Categories,UserGigPackages,UserGigPackage_Extra,Seller_Reviews,Buyer_Reviews,UserGigsImpressions,User_orders,UserSearchTerms,UserGig_Extra_Delivery,UserExtra_gigs,Usergig_faq,Usergig_image,Usergig_requirement,Parameter,Category_package_Extra_Service,Category_package_Details, CharacterLimit,UserAvailable,UserGigs,UserGigsTags, SellerLevels,Contactus, Languages, LearnTopics, LearningTopicCounts, LearningTopicDetails, SubCategories, SubSubCategories, TopicDetails, User,PageEditor, UserLanguages, UserProfileDetails, supportMapping, supportTopic
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
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try: 
                userDetails = User.objects.get(username=username)
                userProfileDetails = UserProfileDetails.objects.get(user_id=userDetails)
                userlanguages = UserLanguages.objects.filter(user_id=userDetails)
                userlang = []
                for lang in userlanguages:
                    userlang.append({"name":lang.language_name.lng_Name,"proficiency":lang.lang_prof})  
                active_gig_details = []
                draft_gig_details = []
                user_gigs_details = UserGigs.objects.filter(user_id=userDetails)
                seller_reviews = Seller_Reviews.objects.filter(s_review_to=userDetails)
                buyer_reviews = Buyer_Reviews.objects.filter(b_review_to=userDetails)
                comm_count = 0
                recc_count = 0
                serv_count = 0
                seller_count = 0
                buyer_count = 0
                s_review_date = ''
                b_review_date = ''
                seller_rev_data = []
                buyer_rev_data = []
                for s_review in seller_reviews:
                    comm_count = comm_count + int(s_review.communication)
                    recc_count = recc_count + int(s_review.recommendation)
                    serv_count = serv_count + int(s_review.service)
                    seller_count = seller_count + int(s_review.average_val)
                    start_date = datetime.strptime(str(s_review.review_date), "%Y-%m-%d %H:%M:%S")
                    end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    diff = relativedelta.relativedelta(end_date, start_date)
                    if(diff.years == 0 and diff.months == 0):
                        if(diff.days == 0):
                            s_review_date = 'today'
                        else:
                            s_review_date = str(diff.days) + ' days'
                    elif(diff.months != 0 and diff.years == 0):
                        if(diff.months == 1):
                            s_review_date = str(diff.months) + ' month'
                        else:
                            s_review_date = str(diff.months) + ' months'
                    elif(diff.years != 0):
                        if(diff.years == 1):
                            s_review_date = str(diff.years) + ' year'
                        else:
                            s_review_date = str(diff.years) + ' years'
                    country_flag_icon = '/static/assets/images/flags/'+ s_review.s_review_from.country.code.lower()+ '.svg'
                    seller_rev_data.append({"message":s_review.review_message,"review":s_review.average_val,"sender":s_review.s_review_from,"review_date":s_review_date,"country_flag":country_flag_icon})
                for b_review in buyer_reviews:
                    buyer_count = buyer_count + int(b_review.rating_val)
                    start_date = datetime.strptime(str(b_review.review_date), "%Y-%m-%d %H:%M:%S")
                    end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    diff = relativedelta.relativedelta(end_date, start_date)
                    if(diff.years == 0 and diff.months == 0):
                        if(diff.days == 0):
                            b_review_date = 'today'
                        else:
                            b_review_date = str(diff.days) + ' days'
                    elif(diff.months != 0 and diff.years == 0):
                        if(diff.months == 1):
                            b_review_date = str(diff.months) + ' month'
                        else:
                            b_review_date = str(diff.months) + ' months'
                    elif(diff.years != 0):
                        if(diff.years == 1):
                            b_review_date = str(diff.years) + ' year'
                        else:
                            b_review_date = str(diff.years) + ' years'
                    b_country_flag_icon = '/static/assets/images/flags/'+ b_review.b_review_from.country.code.lower()+ '.svg'
                    buyer_rev_data.append({"message":b_review.review_message,"review":b_review.rating_val,"sender":b_review.b_review_from,"review_date":b_review_date,"country_flag":b_country_flag_icon})
                try:
                    seller_count = round(seller_count/len(seller_reviews),1)
                except:
                    seller_count = 0
                try:
                    comm_count = round(comm_count/len(seller_reviews),1)
                except:
                    comm_count = 0
                try:
                    recc_count = round(recc_count/len(seller_reviews),1)
                except:
                    recc_count = 0
                try:
                    serv_count = round(serv_count/len(seller_reviews),1)
                except:
                    serv_count = 0
                user_availability= []
                try:
                    user_availability = UserAvailable.objects.get(Q(user_id=userDetails))
                except:
                    user_availability = []
                charcterlimits = CharacterLimit.objects.get(Q(Char_category_Name="available_reason"))
                for u_gig in user_gigs_details:
                    userpack= UserGigPackages.objects.filter(package_gig_name=u_gig , user_id = userDetails , package_type= 'basic').first() 
                    gig_image = Usergig_image.objects.filter(user_id=userDetails,package_gig_name=u_gig).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                    else:
                        gig_image_url = ''
                    if(userpack != None):
                        start_price = userpack.package_price
                    else:
                        start_price = 0 
                    if(u_gig.gig_status == "active"):
                        active_gig_details.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"start_price":start_price})
                    elif(u_gig.gig_status == "draft"):
                        draft_gig_details.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"start_price":start_price})
                return render(request , 'Dashboard/profile.html',{'userDetails':userDetails,"profile_Details":userProfileDetails,"userlanguages":userlang,"active_gigs":active_gig_details,"draft_gigs":draft_gig_details,"seller_reviews":seller_rev_data,"seller_count":seller_count,"comm_count":comm_count,"recc_count":recc_count,"serv_count":serv_count,"buyer_reviews":buyer_rev_data,"character_avail":int(charcterlimits.Max_No_of_char_allowed),"user_avail":user_availability})                 
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

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
            # try:    
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                activegigs = []
                pendinggigs = []
                modifgigs = []
                drafgigs = []
                deniedgigs = []
                pausedgigs = []
                user_gigs_details = UserGigs.objects.filter(user_id=userDetails)
                for u_gig in user_gigs_details:
                    gig_image = Usergig_image.objects.filter(user_id=userDetails,package_gig_name=u_gig).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                    else:
                        gig_image_url = ''
                    last_month = datetime.today() - timedelta(days=30)
                    ugig_impressions = UserGigsImpressions.objects.filter(user_id=userDetails,gig_name=u_gig,impress_date__gte=last_month).count()
                    user_order_details = User_orders.objects.filter(user_id=userDetails,package_gig_name=u_gig,order_date__gte=last_month).count()
                    cancelled_orders =  User_orders.objects.filter(user_id=userDetails,package_gig_name=u_gig, order_status= 'cancel').count()
                    try:
                        cancel_perc = int((cancelled_orders * 100) / (user_order_details))
                    except:
                        cancel_perc = 0
                    if(u_gig.gig_status == "active"):
                        activegigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                    elif(u_gig.gig_status == "pending"):
                        pendinggigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                    elif(u_gig.gig_status == "modification"):
                        modifgigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                    elif(u_gig.gig_status == "draft"):
                        drafgigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                    elif(u_gig.gig_status == "denied"):
                        deniedgigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                    elif(u_gig.gig_status == "paused"):
                        pausedgigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                return render(request , 'Dashboard/manage_gigs.html',{"active_gigs":activegigs,"pending_gigs":pendinggigs,"require_modif":modifgigs,"draft_gigs":drafgigs,"denied_gigs":deniedgigs,"paused_gigs":pausedgigs})
            # except:
            #     return render(request , 'register.html')
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
    
@csrf_exempt
def gig_image_upload_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist("files")
        userid =  request.POST.get("user_id")
        gig_id =  request.POST.get("gig_id")
        userDetails = User.objects.get(pk=userid)
        frontend_url = request.META.get('HTTP_REFERER')
        url1 = urlparse(frontend_url)
        urls = []
        if len(files) != 0:
            for file in files:
                fs= FileSystemStorage(location= settings.MEDIA_ROOT +'/gig_images/')
                file_path=fs.save(gig_id+"_"+file.name.replace(' ','_'),file) 
                url = '/media/gig_images/'+file_path
                urls.append(url)
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
    
    
@csrf_exempt
def post_gig_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        u_gigtitle = request.POST.get("u_gigtitle")
        u_gig_category = request.POST.get("u_gig_category")
        u_gig_sub_category = request.POST.get("u_gig_sub_category")
        u_gig_tags = request.POST['u_gig_tags']
        data = json.loads(u_gig_tags)
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        gigDetails.gig_title = u_gigtitle
        gigDetails.gig_category =  Categories.objects.get(pk=u_gig_category)
        gigDetails.gig_sub_category =  SubSubCategories.objects.get(pk=u_gig_sub_category)
        gigDetails.save()
        UserGigsTags.objects.filter(gig_name=gigDetails ,user_id = userDetails).delete()
        for d in data:
            usertags = UserGigsTags(gig_tag_name= d,gig_name=gigDetails ,user_id = userDetails)
            usertags.save()
        return HttpResponse('sucess')


@csrf_exempt
def post_packages_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        u_gigtitle = request.POST.get("u_gigtitle")
        u_gig_category = request.POST.get("u_gig_category")
        u_gig_sub_category = request.POST.get("u_gig_sub_category")
        u_gig_tags = request.POST['u_gig_tags']
        data = json.loads(u_gig_tags)
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        gigDetails.gig_title = u_gigtitle
        gigDetails.gig_category =  Categories.objects.get(pk=u_gig_category)
        gigDetails.gig_sub_category =  SubSubCategories.objects.get(pk=u_gig_sub_category)
        gigDetails.save()
        UserGigsTags.objects.filter(gig_name=gigDetails ,user_id = userDetails).delete()
        for d in data:
            usertags = UserGigsTags(gig_tag_name= d,gig_name=gigDetails ,user_id = userDetails)
            usertags.save()
        return HttpResponse('sucess')


@csrf_exempt
def post_packages_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        u_package_details = request.POST['u_package_details']
        u_package_details1 = request.POST['u_package_details1']
        u_package_details2 = request.POST['u_package_details2']
        u_extra_delivery = request.POST['u_extra_delivery']
        u_extra_package_details = request.POST['u_add_on_package_details']
        u_add_on_gig = request.POST['u_add_on_gig']
        data_package_details = json.loads(u_package_details)
        data_package_details1 = json.loads(u_package_details1)
        data_package_details2 = json.loads(u_package_details2)
        data_extra_delivery = json.loads(u_extra_delivery)
        data_extra_package_details = json.loads(u_extra_package_details)
        data_add_on_gig = json.loads(u_add_on_gig)
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id, user_id = userDetails)
        UserGigPackages.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
        UserGigPackage_Extra.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
        UserExtra_gigs.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
        UserGig_Extra_Delivery.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
        pack_data_analysys = data_package_details[0]
        dist_keys = pack_data_analysys.keys()
        package_array = []
        for i,key in enumerate(dist_keys):
            if "pack_data_" in key:
                package_array.append({"name":pack_data_analysys[key]["name"],"value":pack_data_analysys[key]["value"]})
        for data_packages in data_package_details:
            pack_delivery = Parameter.objects.get(parameter_value =str(data_packages["pack_duration"]),parameter_name="delivery_time")
            pack_revision = Parameter.objects.get(parameter_value =str(data_packages["pack_revision"]),parameter_name="no_revisions")
            user_gig_packages = UserGigPackages(package_type=data_packages["pack_type"],package_title=data_packages["pack_title"],package_description=data_packages["pack_description"],package_delivery=pack_delivery,package_revisions=pack_revision,package_price=data_packages["pack_price"],package_data=str(package_array),package_gig_name= gigDetails,user_id=userDetails)
            user_gig_packages.save()
        if(len(data_package_details1) != 0):
            pack_data_analysys1 = data_package_details1[0]
            dist_keys1 = pack_data_analysys1.keys()
            package_array1 = []
            for i,key in enumerate(dist_keys1):
                if "pack_data_" in key:
                    package_array1.append({"name":pack_data_analysys1[key]["name"],"value":pack_data_analysys1[key]["value"]})
            for data_packages1 in data_package_details1:
                pack_delivery1 = Parameter.objects.get(parameter_value =str(data_packages1["pack_duration"]),parameter_name="delivery_time")
                pack_revision1 = Parameter.objects.get(parameter_value =str(data_packages1["pack_revision"]),parameter_name="no_revisions")
                user_gig_packages = UserGigPackages(package_type=data_packages1["pack_type"],package_title=data_packages1["pack_title"],package_description=data_packages1["pack_description"],package_delivery=pack_delivery1,package_revisions=pack_revision1,package_price=data_packages1["pack_price"],package_data=str(package_array1),package_gig_name= gigDetails,user_id=userDetails)
                user_gig_packages.save()
        if(len(data_package_details2) != 0):
            pack_data_analysys2 = data_package_details2[0]
            dist_keys2 = pack_data_analysys2.keys()
            package_array2 = []
            for i,key in enumerate(dist_keys2):
                if "pack_data_" in key:
                    package_array2.append({"name":pack_data_analysys2[key]["name"],"value":pack_data_analysys2[key]["value"]})
            for data_packages2 in data_package_details2:
                pack_delivery2 = Parameter.objects.get(parameter_value =str(data_packages2["pack_duration"]),parameter_name="delivery_time")
                pack_revision2 = Parameter.objects.get(parameter_value =str(data_packages2["pack_revision"]),parameter_name="no_revisions")
                user_gig_packages = UserGigPackages(package_type=data_packages2["pack_type"],package_title=data_packages2["pack_title"],package_description=data_packages2["pack_description"],package_delivery=pack_delivery2,package_revisions=pack_revision2,package_price=data_packages2["pack_price"],package_data=str(package_array2),package_gig_name= gigDetails,user_id=userDetails)
                user_gig_packages.save() 
        for extra_delivery in data_extra_delivery:
            extra_days = Parameter.objects.get(parameter_value =str(extra_delivery["days"]),parameter_name="extra_days")
            extra_delivery_gig = UserGig_Extra_Delivery(package_type= extra_delivery["name"],delivery_in= extra_days,extra_price= extra_delivery["price"],package_gig_name= gigDetails,user_id=userDetails)
            extra_delivery_gig.save()
        user_extra_data = UserGigPackage_Extra(package_data= str(data_extra_package_details),package_gig_name= gigDetails,user_id=userDetails)
        user_extra_data.save();
        for ad_on_gig in data_add_on_gig:
            gig_extra_days = Parameter.objects.get(parameter_value =str(ad_on_gig["gig_duration"]),parameter_name="extra_days")
            extra_gig_days = UserExtra_gigs(extra_gig_title= ad_on_gig["gig_title"],extra_gig_description= ad_on_gig["gig_description"],extra_gig_price= ad_on_gig["gig_price"],extra_gig_duration=gig_extra_days,package_gig_name= gigDetails,user_id=userDetails)
            extra_gig_days.save()
        return HttpResponse('sucess')

@csrf_exempt
def post_gig_desp_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        u_gig_description = request.POST.get("u_gig_description")
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        gigDetails.gig_description = u_gig_description
        gigDetails.save()
        return HttpResponse('sucess')
    
    
@csrf_exempt
def post_gig_des_faq_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        u_gig_description = request.POST.get("u_gig_description")
        u_gig_faq_ques = request.POST.get("u_gig_faq_ques")
        u_gig_faq_answer = request.POST.get("u_gig_faq_answer")
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        gigDetails.gig_description = u_gig_description
        gigDetails.save()
        Usergig_faq.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
        user_gig_faqsobj = Usergig_faq(gig_faq_question=u_gig_faq_ques,gig_faq_answer=u_gig_faq_answer,package_gig_name= gigDetails,user_id=userDetails)
        user_gig_faqsobj.save()
        return HttpResponse('sucess')



@csrf_exempt
def post_rquirements_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        u_requirements = request.POST['u_requirements']
        data_requirements = json.loads(u_requirements)
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        Usergig_requirement.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
        for req_question in data_requirements:
            user_gig_req= Usergig_requirement(gig_req_question=req_question['name'],gig_req_ans_type="Free Text",package_gig_name= gigDetails,user_id=userDetails)
            user_gig_req.save()
        return HttpResponse('sucess')


@csrf_exempt
def post_images_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        u_images = request.POST['u_images']
        data_images = json.loads(u_images)
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        Usergig_image.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
        for gig_img in data_images:
            if(len(gig_img['name'].strip()) != 0):
                user_gig_img= Usergig_image(gig_image=gig_img['name'],package_gig_name= gigDetails,user_id=userDetails)
                user_gig_img.save()
        return HttpResponse('sucess')


@csrf_exempt
def post_publish_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        gigDetails.gig_status = "pending"
        gigDetails.save();
        return HttpResponse('sucess')

def get_gig_details_view(request):
    if request.method == 'GET':
        data = []
        u_gig_id = request.GET['u_gig_id']
        u_user_id = request.GET['u_user_id']
        userDetails =  User.objects.get(pk=u_user_id)
        data_gig_details = []
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        data_gig_details.append({"title":gigDetails.gig_title,"gig_category":str(gigDetails.gig_category.id),"gig_sub_category":str(gigDetails.gig_sub_category.id),"gig_description":gigDetails.gig_description})
        gigTags =  UserGigsTags.objects.filter(gig_name=gigDetails , user_id = userDetails)
        gigTags_tmpJson = serializers.serialize("json",gigTags)
        gigTags_tmpObj = json.loads(gigTags_tmpJson)
        gigPackages =  UserGigPackages.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
        package_data = []
        extra_delivery_data = []
        extra_gigs_data = []
        for gig_package in gigPackages:
            package_data.append({"package_type":gig_package.package_type,"package_title":gig_package.package_title,"package_description":gig_package.package_description,"package_delivery":gig_package.package_delivery.parameter_value,"package_revisions":gig_package.package_revisions.parameter_value,"package_data":gig_package.package_data,"package_price":gig_package.package_price})
        gig_extra_delivery =  UserGig_Extra_Delivery.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
        for gig_ex_delivery in gig_extra_delivery:
            extra_delivery_data.append({"package_type":gig_ex_delivery.package_type,"delivery_in":gig_ex_delivery.delivery_in.parameter_value,"extra_price":gig_ex_delivery.extra_price})
        gig_extra_pack =  UserGigPackage_Extra.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
        gig_extra_pack_tmpJson = serializers.serialize("json",gig_extra_pack)
        gig_extra_pack_tmpObj = json.loads(gig_extra_pack_tmpJson)
        extra_gigs =  UserExtra_gigs.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
        for gig_ex in extra_gigs:
            extra_gigs_data.append({"extra_gig_title":gig_ex.extra_gig_title,"extra_gig_description":gig_ex.extra_gig_description,"extra_gig_price":gig_ex.extra_gig_price,"extra_gig_duration":gig_ex.extra_gig_duration.parameter_value})
        gig_faqs =  Usergig_faq.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
        gig_faqs_tmpJson = serializers.serialize("json",gig_faqs)
        gig_faqs_tmpObj = json.loads(gig_faqs_tmpJson)
        gig_requirements =  Usergig_requirement.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
        gig_requirements_tmpJson = serializers.serialize("json",gig_requirements)
        gig_requirements_tmpObj = json.loads(gig_requirements_tmpJson)
        gig_image =  Usergig_image.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
        gig_image_tmpJson = serializers.serialize("json",gig_image)
        gig_image_tmpObj = json.loads(gig_image_tmpJson)
        response_data = {"gig_details":json.dumps(data_gig_details), "gig_tags":gigTags_tmpObj,"gig_packages":package_data, "gig_extra_delivery":extra_delivery_data, "gig_extra_pack":gig_extra_pack_tmpObj, "extra_gigs":extra_gigs_data, "gig_faqs":gig_faqs_tmpObj, "gig_requirements":gig_requirements_tmpObj, "gig_image":gig_image_tmpObj}
        return JsonResponse(response_data,safe=False)    
     
    
def post_pause_gig_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        gig_id = request.GET['gig_id']
        userDetails =  User.objects.get(pk=userid)
        gigDetails =  UserGigs.objects.get(pk=gig_id , user_id = userDetails)
        gigDetails.gig_status = 'paused'
        gigDetails.save()
        return HttpResponse('sucess')

def post_delete_gig_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        gig_id = request.GET['gig_id']
        userDetails =  User.objects.get(pk=userid)
        gigDetails =  UserGigs.objects.get(pk=gig_id , user_id = userDetails).delete()
        return HttpResponse('sucess')
    
    
@csrf_exempt
def post_availability_view(request):
    if request.method == 'POST':
        userid = request.POST.get("userid")
        unva_from = request.POST.get("unva_from")
        unva_to = request.POST.get("unva_to")
        reason = request.POST.get("reason")
        avail_message = request.POST.get("avail_message")
        checked_new = request.POST.get("checked_new")
        userDetails =  User.objects.get(pk=userid)
        availablity =  UserAvailable.objects.filter(user_id = userDetails).delete()
        user_avail_obj = UserAvailable(available_from=unva_from,available_to=unva_to,available_mssg=avail_message,available_for_new=checked_new,available_types=reason,user_id=userDetails)
        user_avail_obj.save()
        return HttpResponse('sucess')
    
    
@csrf_exempt
def post_avail_delete_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        avail_id = request.GET['avail_id']
        userDetails =  User.objects.get(pk=userid)
        availablity =  UserAvailable.objects.filter(user_id = userDetails).delete()
        return HttpResponse('sucess')

def get_availability_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        try:
            user_avail = UserAvailable.objects.filter(user_id = userid)
            tmpJson = serializers.serialize("json",user_avail)
            tmpObj = json.loads(tmpJson)
        except:
            tmpObj = []
        return HttpResponse(json.dumps(tmpObj))