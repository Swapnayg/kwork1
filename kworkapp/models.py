import datetime
from operator import truediv
from django.utils import timezone
import os
from django.forms import DateField
from django_countries.fields import CountryField
import shortuuid
from django.core.files import File
from django.db import models
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
import urllib
from shortuuid.django_fields import ShortUUIDField
from mainKwork import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from taggit.managers import TaggableManager


class MytypeField(models.Field):
    def db_type(self, connection):
        return 'timestamp'

class SellerLevels(models.Model):
    BOOL_CHOICES =[('level1', 'New or higher'),('level2', 'Advanced or higher'),('level3', 'Professional')]
    level_name =  models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,default="Basic",null=True)
    No_of_gigs = models.CharField(max_length=200,blank=True,default="0",null=True)
    
    class Meta:
        verbose_name = _("Seller Level")
        verbose_name_plural = _("Seller Levels")

    def __str__(self):
        return str(self.level_name)

class UserManager(BaseUserManager):
    def _create_user(self, email, username=None, is_admin=False, is_staff=False, is_active=True, password=None, country=None, avatar=None):
        'Method for actual creation of a user'
        if not email:
            raise ValueError('User must have an email')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_admin=is_admin,
            is_staff=is_staff,
            is_active=is_active,
            country=country,
            avatar=avatar
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, username=None, password=None, country=None, avatar=None):
        'Create a simple user'
        return self._create_user(email=email, username=username, password=password,country=country,avatar=avatar)

    def create_staffuser(self, email=None, username=None, password=None, country=None, avatar=None):
        'Create a staff user'
        return self._create_user(email=email, username=username, is_staff=True, password=password,country=country,avatar=avatar)

    def create_superuser(self, email=None, username=None, password=None, country=None, avatar=None):
        'Create a super user'
        return self._create_user(
            email=email, username=username, is_admin=True,
             is_staff=True, is_active=True, password=password,country=country,avatar=avatar
        )

class User(AbstractBaseUser):
    BOOL_CHOICES =[('Buyer', 'Buyer'),('Seller', 'Seller')]
    BOOL_CHOICES_Levels =[('level1', 'New or higher'),('level2', 'Advanced or higher'),('level3', 'Professional')]
    email = models.EmailField(max_length=255, unique=True,default="",blank=True,null=True)
    username = models.CharField(max_length=150, unique=False,default="",blank=True,null=True)
    first_name = models.CharField(max_length=250,blank=True,default="",null=True)
    last_name = models.CharField(max_length=250,blank=True,default="",null=True)
    name =models.CharField(max_length=200,blank=True,default="",null=True)
    country =  CountryField(blank=True,default="",null=True)
    avatar = models.CharField(max_length=500, blank=True,default="",null=True)
    avg_respons = models.CharField(max_length=500, blank=True,default="",null=True)
    last_delivery = models.CharField(max_length=500, blank=True,default="",null=True)
    ordersin_progress = models.CharField(max_length=500, blank=True,default="",null=True)
    avg_delivery_time = models.CharField(max_length=500, blank=True,default="",null=True)
    seller_level =  models.CharField(max_length=200,choices=BOOL_CHOICES_Levels,blank=True,default="level1",null=True)
    profile_type = models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,default="",null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    code = models.IntegerField(default=False)
    is_staff = models.BooleanField(default=False)
    terms = models.BooleanField(default=False)
    updated_at = MytypeField
    created_at = MytypeField
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        'Does the user have a specific permission?'
        return self.is_admin

    def has_module_perms(self, app_label):
        'Does the user have permissions to view the app `app_label`?'
        return self.is_admin

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_all_permissions(user=None):
        if user.is_admin:
            return set()

    @property
    def has_staff_perm(self):
        'Is the user a member of staff?'
        return self.is_staff

    @property
    def has_active_perm(self):
        'Is the user active?'
        return self.is_active

    @property
    def has_admin_perm(self):
        'Is the user is super admin?'
        return self.is_admin

class Conversation(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="convo_starter")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="convo_participant")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")

    def __str__(self):
        return self.timestamp

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="message_sender")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="message_receiver")
    text = models.CharField(max_length=200)
    attachment = models.ImageField(blank=True)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return self.timestamp

class PageEditor(models.Model):
    page_name = models.CharField(max_length=500)
    page_slug = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def edit_page_mode(self):
        return format_html(
        '<a class="btn" target="_blank" href="/admin/content_edit/{}/">Edit Contents</a>',
        self.page_slug,
    )
    class Meta:
        verbose_name = _("Page Editor")
        verbose_name_plural = _("Page Editor")

    def __str__(self):
        return self.page_slug



class supportTopic(models.Model):
    support_topic_Name = models.CharField(max_length=500)
    topic_category = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Support Topic")
        verbose_name_plural = _("Support Topics")

    def __str__(self):
        return self.support_topic_Name

class supportMapping(models.Model):
    suport_topic = models.ForeignKey(supportTopic, on_delete=models.CASCADE,related_name="suport_topic")
    map_to =    models.ForeignKey(supportTopic, on_delete=models.CASCADE)   
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Support Mapping")
        verbose_name_plural = _("Support Mapping")

    def __str__(self):
        return str(self.timestamp)

class TopicDetails(models.Model):
    topic_Name = models.ForeignKey(supportTopic, on_delete=models.CASCADE,related_name="topic_Name",null=False,blank=False)
    topic_Desc =  models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Topic Details")
        verbose_name_plural = _("Topic Details")

    def __str__(self):
        return str(self.timestamp)


class Contactus(models.Model):
    BOOL_CHOICES =[('Received', 'Received'),('Contacted', 'Contacted'),]
    id = ShortUUIDField(length=6,max_length=6,alphabet="123456",primary_key=True,)
    email = models.EmailField(max_length=250, blank=True, null=True)
    message = models.CharField(max_length=1000, blank=True, null=True)
    status =  models.CharField(max_length=200,choices=BOOL_CHOICES,default='NA',)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return str(self.id)

class LearnTopics(models.Model):
    topic_names = models.CharField(max_length=1000, blank=True, null=True,unique=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Learning Topic")
        verbose_name_plural = _("Learning Topics")

    def __str__(self):
        return str(self.topic_names)

def servicefilename(instance, filename):
    ext = filename.split('.')[-1]
    filenm = os.path.splitext(filename)[0]
    filename = "%s_%s.%s" % ("Learning",filenm, ext)
    return os.path.join( 'learning/'+filename)

class LearningTopicDetails(models.Model):
    topic_Name = models.CharField(max_length=500, blank=True, null=True,unique=True)
    timeof_read_in_minute = models.CharField(max_length=200, blank=True, null=True)
    topic_description = models.CharField(max_length=1000, blank=True, null=True)
    image = models.FileField(upload_to = servicefilename ,max_length=255, null=True,blank=True)
    image_Text =  models.CharField(max_length=200, blank=True, null=True)
    video_url =  models.URLField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Learning Topic Detail")
        verbose_name_plural = _("Learning Topic Details")

    def __str__(self):
        return str(self.topic_Name)

class LearningTopicCounts(models.Model):
    topic_name = models.ForeignKey(LearningTopicDetails, on_delete=models.CASCADE,related_name="Learning_topic_Name",null=False,blank=False)
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        verbose_name = _("Learning Topic Count")
        verbose_name_plural = _("Learning Topic Counts")

    def __str__(self):
        return str(self.topic_name)

def categoryfilename(instance, filename):
    ext = filename.split('.')[-1]
    filenm = os.path.splitext(filename)[0]
    filename = "%s_%s.%s" % (instance.category_Name.split()[0],filenm, ext)
    return os.path.join( 'category/'+filename)

def subcategoryfilename(instance, filename):
    ext = filename.split('.')[-1]
    filenm = os.path.splitext(filename)[0]
    filename = "%s_%s.%s" % (instance.sub_category_Name.split()[0],filenm, ext)
    return os.path.join( 'category/subcategory/'+filename)

class Categories(models.Model):
    image = models.FileField(upload_to = categoryfilename ,max_length=255, null=True,blank=True,help_text='Max width and height of the image will be 480:330')
    category_quote = models.CharField(max_length=800, blank=True, null=True)
    category_Name = models.CharField(max_length=500, blank=True, null=True)
    slug = models.CharField(max_length=300, blank=True, null=True)
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return str(self.category_Name)

class SubCategories(models.Model):
    category_Name = models.ForeignKey(Categories, on_delete=models.CASCADE,related_name="Category_Name",null=False,blank=False)
    sub_category_Name = models.CharField(max_length=500, blank=True, null=True)
    image = models.FileField(upload_to = subcategoryfilename ,max_length=255, null=True,blank=True,help_text='Max width and height of the image will be 480:330')
    slug = models.CharField(max_length=300, blank=True, null=True)
    class Meta:
        verbose_name = _("Sub Category")
        verbose_name_plural = _("Sub Categories")

    def __str__(self):
        return str(self.sub_category_Name)


class SubSubCategories(models.Model):
    category_Name = models.ForeignKey(Categories, on_delete=models.CASCADE,related_name="MainCategory_Name",null=False,blank=False)
    sub_category_Name = models.ForeignKey(SubCategories, on_delete=models.CASCADE,related_name="SubCategory_Name",null=False,blank=False)
    sub_sub_category_Name = models.CharField(max_length=500, blank=True, null=True)
    slug = models.CharField(max_length=300, blank=True, null=True)
    tags = TaggableManager()

    def Tags(self):
        return ",".join([str(p) for p in self.tags.all()])

    class Meta:
        verbose_name = _("Main Menu")
        verbose_name_plural = _("Main Menus")

    def __str__(self):
        return str(self.sub_sub_category_Name)


class CharacterLimit(models.Model):
    Char_category_Name = models.CharField(max_length=500, blank=True, null=True)
    Hint_text = models.CharField(max_length=800, blank=True, null=True)
    Max_No_of_char_allowed = models.IntegerField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = _("Character Limit")
        verbose_name_plural = _("Character Limits")

    def __str__(self):
        return str(self.Char_category_Name)


class UserProfileDetails(models.Model):
    main_category = models.ForeignKey(Categories, on_delete=models.CASCADE,related_name="main_category",null=True,blank=True)
    sub_category = models.ForeignKey(SubCategories, on_delete=models.CASCADE,related_name="sub_category",null=True,blank=True)
    profile_title = models.CharField(max_length=800, blank=True, null=True)
    profess_overview = models.CharField(max_length=1000, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    
    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profile")

    def __str__(self):
        return str(self.profile_title)

class Languages(models.Model):
    lng_Name = models.CharField(max_length=300, blank=True, null=True)
    lng_slug = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return str(self.lng_Name)

class UserLanguages(models.Model):
    BOOL_CHOICES =[('Basic', 'Basic'),('Fluent', 'Fluent'),('Conversational', 'Conversational')]
    language_name =  models.ForeignKey(Languages, on_delete=models.CASCADE,null=False,blank=False)
    lang_prof = models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,default="Basic",null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("User Language")
        verbose_name_plural = _("User Languages")

    def __str__(self):
        return str(self.language_name)



    
class Category_package_Details(models.Model):
    BOOL_CHOICES =[('number', 'Number'),('boolean', 'Boolean')]
    category_name = models.ForeignKey(SubSubCategories, on_delete=models.CASCADE,null=False,blank=False)
    display_name = models.CharField(max_length=1000,blank=True,default="",null=True)
    helper_txt = models.CharField(max_length=1000,blank=True,default="",null=True)
    display_type =   models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,null=True)
    
    class Meta:
        verbose_name = _("Category Package")
        verbose_name_plural = _("Category Packages")

    def __str__(self):
        return str(self.display_name)

class Parameter(models.Model):
    BOOL_CHOICES =[('delivery_time', 'Delivery Time'),('extra_days', 'Extra Days'),('extra_time', 'Extra Time'),('no_revisions', 'No. of Revisions')]
    parameter_name =   models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,null=True)
    parameter_value = models.CharField(max_length=1000,blank=True,default="",null=True)
    
    class Meta:
        verbose_name = _("Add On Gig Params")
        verbose_name_plural = _("Add On Gig Params")

    def __str__(self):
        return str(self.parameter_value)
    
class Category_package_Extra_Service(models.Model):
    BOOL_CHOICES =[('number', 'Number'),('extra_time', 'Extra Time'),('none', 'None')]
    category_name = models.ForeignKey(SubSubCategories, on_delete=models.CASCADE,null=False,blank=False)
    display_name = models.CharField(max_length=1000,blank=True,default="",null=True)
    helper_txt = models.CharField(max_length=1000,blank=True,default="",null=True)
    display_type =   models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,null=True)
    
    class Meta:
        verbose_name = _("Category Extra Services")
        verbose_name_plural = _("Category Extra Services")

    def __str__(self):
        return str(self.display_name)


class UserGigs(models.Model):
    BOOL_CHOICES_STATUS =[('active', 'Active'),('pending', 'Pending'),('modification', 'Modification'),('draft', 'Draft'),('denied', 'Denied'),('paused', 'Paused')]
    gig_title =   models.CharField(max_length=1000,blank=True,default="",null=True)
    gig_category = models.ForeignKey(Categories, on_delete=models.CASCADE,null=True,blank=True)
    gig_sub_category = models.ForeignKey(SubSubCategories, on_delete=models.CASCADE,null=True,blank=True)
    gig_description = models.TextField(blank=True,default="",null=True)
    gig_status =   models.CharField(max_length=200,choices=BOOL_CHOICES_STATUS,default="",blank=True,null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Details")
        verbose_name_plural = _("Gig Details")

    def __str__(self):
        return str(self.gig_title)
    
    
class UserGigsTags(models.Model):
    BOOL_CHOICES =[('Basic', 'Basic'),('Fluent', 'Fluent'),('Conversational', 'Conversational')]
    gig_tag_name = models.CharField(max_length=500,blank=True,default="",null=True)
    gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Tags")
        verbose_name_plural = _("Gig Tags")

    def __str__(self):
        return str(self.gig_tag_name)
    
    
class UserGigPackages(models.Model):
    BOOL_CHOICES =[('basic', 'Basic'),('standard', 'Standard'),('enterprise', 'Enterprise')]
    package_type =   models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,null=True)
    package_title = models.CharField(max_length=500,blank=True,default="",null=True)
    package_description = models.TextField(blank=True,default="",null=True)
    package_delivery =  models.ForeignKey(Parameter, on_delete=models.CASCADE,related_name="package_delivery",null=False,blank=False)
    package_revisions =  models.ForeignKey(Parameter, on_delete=models.CASCADE,related_name="package_revisions",null=False,blank=False)
    package_data =  models.TextField(blank=True,default="",null=True)
    package_price = models.CharField(max_length=300,blank=True,default="",null=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Packages")
        verbose_name_plural = _("Gig Packages")

    def __str__(self):
        return str(self.package_title)
    
    
class UserGigPackage_Extra(models.Model):
    package_data =  models.TextField(blank=True,default="",null=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Package Extra")
        verbose_name_plural = _("Gig Package Extra")

    def __str__(self):
        return str(self.user_id)

class UserExtra_gigs(models.Model):
    extra_gig_title = models.CharField(max_length=500,blank=True,default="",null=True)
    extra_gig_description =  models.TextField(blank=True,default="",null=True)
    extra_gig_price = models.CharField(max_length=500,blank=True,default="",null=True)
    extra_gig_duration = models.ForeignKey(Parameter, on_delete=models.CASCADE,null=False,blank=False)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Extra Gig")
        verbose_name_plural = _("Extra Gigs")

    def __str__(self):
        return str(self.extra_gig_title)
    
    
class Usergig_faq(models.Model):
    gig_faq_question = models.CharField(max_length=800,blank=True,default="",null=True)
    gig_faq_answer =  models.TextField(blank=True,default="",null=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Faq")
        verbose_name_plural = _("Gig Faqs")

    def __str__(self):
        return str(self.gig_faq_question)
    
class Usergig_image(models.Model):
    gig_image = models.ImageField(blank=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Image")
        verbose_name_plural = _("Gig Images")

    def __str__(self):
        return str(self.gig_image)
    
    
class Usergig_requirement(models.Model):
    gig_req_question =  models.CharField(max_length=800,blank=True,default="",null=True)
    gig_req_ans_type =  models.CharField(max_length=800,blank=True,default="",null=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Requirement")
        verbose_name_plural = _("Gig Requirements")

    def __str__(self):
        return str(self.gig_req_question)

