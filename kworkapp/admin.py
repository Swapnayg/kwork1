import json
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_delete
from django_summernote.admin import SummernoteModelAdmin
from django.shortcuts import render
from kworkapp.models import Categories,UserGigPackages,UserGigPackage_Extra,UserSearchTerms,UserGig_Extra_Delivery,UserExtra_gigs,Usergig_faq,Usergig_image,Usergig_requirement,Parameter,Category_package_Extra_Service,Category_package_Details, CharacterLimit,UserAvailable,UserGigs,UserGigsTags, SellerLevels,Contactus, Languages, LearnTopics, LearningTopicCounts, LearningTopicDetails, SubCategories, SubSubCategories, TopicDetails, User,PageEditor, UserLanguages, UserProfileDetails, supportMapping, supportTopic
from mainKwork import settings
from django.core.files.base import ContentFile
from .forms import UserChangeForm, UserCreationForm
from django.urls import URLPattern, path,include
from django.contrib.auth.models import Group
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
import pycountry

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username','first_name','seller_level','last_name', 'name', 'is_admin', 'is_staff', 'is_active','avatar','country',"profile_type",'terms')
    list_filter = ('is_admin', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username','seller_level', 'name', 'password','country',"profile_type",'terms')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2','country',"profile_type",'terms')}
        ),
    )
    search_fields = ('email', 'username', 'name')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

class AdminPageEditor(admin.ModelAdmin):
    list_display = ['page_name','page_slug','timestamp','edit_page_mode']
    #def has_add_permission(self, request, obj=None):
        #return False

    #def has_change_permission(self, request, obj=None):
        #return False

    #def has_delete_permission(self, request, obj=None):
        #return False

admin.site.register(PageEditor, AdminPageEditor)


class AdminSellerLevels(admin.ModelAdmin):
    list_display = ['level_name','No_of_gigs']
    def has_add_permission(self, request, obj=None):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

admin.site.register(SellerLevels, AdminSellerLevels)

class AdminsupportTopic(admin.ModelAdmin):
    list_display = ['support_topic_Name','topic_category','timestamp']

admin.site.register(supportTopic, AdminsupportTopic)

class AdminsupportMapping(admin.ModelAdmin):
    list_display = ['suport_topic','map_to','timestamp']

admin.site.register(supportMapping, AdminsupportMapping)

class AdminContactus(admin.ModelAdmin):
    list_display = ['id','email','message','status','created_at','updated_at']

admin.site.register(Contactus, AdminContactus)

class AdminTopicDetails(SummernoteModelAdmin):
    list_display = ['topic_Name','topic_Desc','timestamp']
    summernote_fields = ('topic_Desc', )
    class Media:
        css = {'all': ('assets/css/frontend/topic_Details.css', )} 

admin.site.register(TopicDetails, AdminTopicDetails)

class AdminLearnTopics(admin.ModelAdmin):
    list_display = ['topic_names','created_at']

admin.site.register(LearnTopics, AdminLearnTopics)

class AdminCategory_package_Details(admin.ModelAdmin):
    list_display = ['category_name','helper_txt','display_name','display_type']

admin.site.register(Category_package_Details, AdminCategory_package_Details)

class AdminParameter(admin.ModelAdmin):
    list_display = ['parameter_name','parameter_value']

admin.site.register(Parameter, AdminParameter)

class AdminCategory_package_Extra_Service(admin.ModelAdmin):
    list_display = ['category_name','helper_txt','display_name','display_type']

admin.site.register(Category_package_Extra_Service, AdminCategory_package_Extra_Service)

class AdminLearningTopicDetails(admin.ModelAdmin):
    list_display = ['topic_Name','topic_description','image_Text']

admin.site.register(LearningTopicDetails, AdminLearningTopicDetails)

class AdminLearningTopicCounts(admin.ModelAdmin):
    list_display = ['topic_name','ip_address']

admin.site.register(LearningTopicCounts, AdminLearningTopicCounts)

class AdminCategories(admin.ModelAdmin):
    list_display = ['category_Name','image','slug','category_quote']

admin.site.register(Categories, AdminCategories)

class AdminSubCategories(admin.ModelAdmin):
    list_display = ['category_Name','sub_category_Name','image','slug']

admin.site.register(SubCategories, AdminSubCategories)

class AdminSubSubCategories(admin.ModelAdmin):
    list_display = ['category_Name','sub_category_Name','sub_sub_category_Name','slug','Tags']
    
    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js','assets/js/sub_sub_category.js')

admin.site.register(SubSubCategories, AdminSubSubCategories)


class AdminCharacterLimit(admin.ModelAdmin):
    list_display = ['Char_category_Name','Hint_text','Max_No_of_char_allowed']
    #readonly_fields = ['Char_category_Name']

admin.site.register(CharacterLimit, AdminCharacterLimit)


class AdminUserProfileDetails(admin.ModelAdmin):
    list_display = ['main_category','sub_category','profile_title','profess_overview','user_id']
    
    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js','assets/js/sub_sub_category1.js')
        
admin.site.register(UserProfileDetails, AdminUserProfileDetails)

class AdminLanguages(admin.ModelAdmin):
    list_display = ['lng_Name','lng_slug']

admin.site.register(Languages, AdminLanguages)

class AdminUserLanguages(admin.ModelAdmin):
    list_display = ['language_name','lang_prof','user_id']

admin.site.register(UserLanguages, AdminUserLanguages)

class AdminUserSearchTerms(admin.ModelAdmin):
    list_display = ['search_words','ip_address','search_types']

admin.site.register(UserSearchTerms, AdminUserSearchTerms)


class AdminUserGigs(admin.ModelAdmin):
    list_display = ['gig_title','gig_category','gig_sub_category','gig_description','gig_status','user_id','gig_impressions']

admin.site.register(UserGigs, AdminUserGigs)


class AdminUserAvailable(admin.ModelAdmin):
    list_display = ['available_from','available_to','available_mssg','available_for_new','available_types','gig_name','user_id']

admin.site.register(UserAvailable, AdminUserAvailable)


class AdminUserPackageGig(admin.ModelAdmin):
    list_display = ['package_type','package_title','package_description','package_delivery','package_revisions','package_data','package_price','package_gig_name','user_id']

admin.site.register(UserGigPackages, AdminUserPackageGig)

class AdminUserGigPackage_Extra(admin.ModelAdmin):
    list_display = ['package_data','package_gig_name','user_id']

admin.site.register(UserGigPackage_Extra, AdminUserGigPackage_Extra)


class AdminUserGig_Extra_Delivery(admin.ModelAdmin):
    list_display = ['package_type','delivery_in','extra_price','package_gig_name','user_id']

admin.site.register(UserGig_Extra_Delivery, AdminUserGig_Extra_Delivery)


class AdminUserExtra_gigs(admin.ModelAdmin):
    list_display = ['extra_gig_title','extra_gig_description','extra_gig_price','extra_gig_duration','package_gig_name','user_id']

admin.site.register(UserExtra_gigs, AdminUserExtra_gigs)


class AdminUsergig_faq(admin.ModelAdmin):
    list_display = ['gig_faq_question','gig_faq_answer','package_gig_name','user_id']

admin.site.register(Usergig_faq, AdminUsergig_faq)

class AdminUsergig_image(admin.ModelAdmin):
    list_display = ['gig_image','package_gig_name','user_id']

admin.site.register(Usergig_image, AdminUsergig_image)


class AdminUsergig_requirement(admin.ModelAdmin):
    list_display = ['gig_req_question','gig_req_ans_type','package_gig_name','user_id']

admin.site.register(Usergig_requirement, AdminUsergig_requirement)


class AdminUserGigsTags(admin.ModelAdmin):
    list_display = ['gig_tag_name','gig_name','user_id']

admin.site.register(UserGigsTags, AdminUserGigsTags)

def get_admin_urls(urls):
    def get_urls():
        my_urls =  [
           path('content_edit/<str:Id>/', content_editView,name='content_edit'), 
        ]
        return my_urls + urls
    return get_urls

admin.autodiscover()

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls

def content_editView(request,Id=''):
    print(Id+ ".html")
    return render(request , 'contents.html',{'templateName':Id+ ".html"})

