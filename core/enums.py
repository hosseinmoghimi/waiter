from core.settings import SITE_URL
from django.db.models import TextChoices
from django.utils.translation import gettext as _
from enum import Enum

class PictureNameEnums(TextChoices):
    LOGO="لوگو",_("لوگو")


class UnitNameEnum(TextChoices):
    ADAD="عدد",_("عدد")
    GERAM="گرم",_("گرم")
    KILOGERAM="کیلوگرم",_("کیلوگرم")
    TON="تن",_("تن")
    METER="متر",_("متر")
    METER2="متر مربع",_("متر مربع")
    METER3="متر مکعب",_("متر مکعب")
    PART="قطعه",_("قطعه")
    SHAKHEH="شاخه",_("شاخه")
    DASTGAH="دستگاه",_("دستگاه")
    SERVICE="سرویس",_("سرویس")
    PACK="بسته",_("بسته")
    POCKET="کیسه",_("کیسه")

class AppNameEnum(TextChoices):
    # drassistant='drassistant',_('drassistant')
    tax='tax',_('tax')
    web='web',_('web')
    salary='salary',_('salary')
    stock='stock',_('stock')
    calendar='calendar',_('calendar')
    resume='resume',_('resume')
    realestate='realestate',_('realestate')
    projectmanager='projectmanager',_('projectmanager')
    # market='market',_('market')
    # transport='transport',_('transport')
    accounting='accounting',_('accounting')
    help='help',_('help')
    farm='farm',_('farm')
    core='core',_('core')
    market='market',_('market')
    # dashboard='dashboard',_('dashboard')
    # realestate='realestate',_('realestate')
    # vehicles='vehicles',_('vehicles')
    # projectcontrol='projectcontrol',_('projectcontrol')
  
class TextDirectionEnum(TextChoices):
    Rtl='rtl',_('rtl')
    Ltr='ltr',_('ltr')

class IconsEnum(TextChoices):
    # aaaaaaa='aaaaaaaaaa',_('aaaaaaaaaaa')
    # aaaaaaa='aaaaaaaaaa',_('aaaaaaaaaaa')
    # aaaaaaa='aaaaaaaaaa',_('aaaaaaaaaaa')
    # aaaaaaa='aaaaaaaaaa',_('aaaaaaaaaaa')
    account_circle='account_circle',_('account_circle')
    add_shopping_cart='add_shopping_cart',_('add_shopping_cart')
    apartment='apartment',_('apartment')
    alarm='alarm',_('alarm')
    attach_file='attach_file',_('attach_file')
    attach_money='attach_money',_('attach_money')
    backup='backup',_('backup')
    build='build',_('build')
    card_travel='card_travel',_('card_travel')
    chat='chat',_('chat')
    construction='construction',_('construction')
    dashboard='dashboard',_('dashboard')
    delete='delete',_('delete')
    description='description',_('description')
    emoji_objects='emoji_objects',_('emoji_objects')
    engineering='engineering',_('engineering')
    extension='extension',_('extension')
    face='face',_('face')
    facebook='facebook',_('facebook')
    favorite='favorite',_('favorite')
    fingerprint='fingerprint',_('fingerprint')
    get_app='get_app',_('get_app')
    help_outline='help_outline',_('help_outline')
    home='home',_('home')
    important_devices='important_devices',_('important_devices')
    link='link',_('link')
    linked_camera='linked_camera',_('linked_camera')
    local_shipping='local_shipping',_('local_shipping')
    lock='lock',_('lock')
    mail='mail',_('mail')
    menu='menu',_('menu')
    movie_filter='movie_filter',_('movie_filter')
    network_check='network_check',_('network_check')
    notification_important='notification_important',_('notification_important')
    palette='palette',_('palette')
    phone='phone',_('phone')
    place='place',_('place')
    psychology='psychology',_('psychology')
    publish='publish',_('publish')
    reply='reply',_('reply')
    schedule='schedule',_('schedule')
    school='school',_('school')
    send='send',_('send')
    settings='settings',_('settings')
    share='share',_('share')
    sync='sync',_('sync')
    traffic='traffic',_('traffic')
    two_wheeler='two_wheeler',_('two_wheeler')
    verified_user='verified_user',_('verified_user')
    vpn_key='vpn_key',_('vpn_key')
    weekend='weekend',_('weekend')


class ParametersEnum(TextChoices):
    SHOW_ARCHIVES="نمایش فایل های آرشیو شده",_("نمایش فایل های آرشیو شده")
    VISITOR_COUNTER="VISITOR_COUNTER",_("VISITOR_COUNTER")
    GOOGLE_API_KEY='GOOGLE_API_KEY',_('GOOGLE_API_KEY')
    GOOGLE_GPS_X='GOOGLE_GPS_X',_('GOOGLE_GPS_X')
    GOOGLE_GPS_Y='GOOGLE_GPS_Y',_('GOOGLE_GPS_Y')
    ABOUT_US='درباره ما کامل',_('درباره ما کامل')
    ABOUT_US_SHORT='درباره ما کوتاه',_('درباره ما کوتاه')
    ABOUT_US_TITLE='عنوان درباره ما',_('عنوان درباره ما')
    ADDRESS='آدرس',_('آدرس')
    CURRENCY='واحد پول',_('واحد پول')
    CONTACT_US='ارتباط با ما',_('ارتباط با ما')
    CSRF_FAILURE_MESSAGE='پیام درخواست نامعتبر',_('پیام درخواست نامعتبر')
    EMAIL='ایمیل',_('ایمیل')
    FAX='فکس',_('فکس')
    GOOGLE_SEARCH_CONSOLE_TAG='تگ سرچ گوگل',_('تگ سرچ گوگل')
    LOCATION='موقعیت در گوگل مپ',_('موقعیت در گوگل مپ')     
    MOBILE='موبایل',_('موبایل')
    NAV_BACK_COLOR='رنگ زمینه منوی بالای سایت',_('رنگ زمینه منوی بالای سایت')
    NAV_TEXT_COLOR='رنگ متن منوی بالای سایت',_('رنگ متن منوی بالای سایت')
    OUR_TEAM_LINK='لینک تیم ما',_('لینک تیم ما')
    OUR_TEAM_TITLE='عنوان تیم ما',_('عنوان تیم ما')
    POSTAL_CODE='کد پستی',_('کد پستی')
    PRE_TILTE='پیش عنوان',_('پیش عنوان')
    SLOGAN='شرح کوتاه',_('شرح کوتاه')
    TEL='تلفن',_('تلفن')
    TERMS='قوانین',_('قوانین')
    THEME_COLOR='رنگ سربرگ کروم در موبایل',_('رنگ سربرگ کروم در موبایل')
    TITLE='عنوان',_('عنوان')
    URL='لینک',_('لینک')
    VIDEO_LINK='لینک ویدیو',_('لینک ویدیو')
    VIDEO_TITLE='عنوان ویدیو',_('عنوان ویدیو')





class MainPicEnum(TextChoices):    
    FAVICON='آیکون سایت',_('آیکون سایت')     
    CAROUSEL='سایت',_('سایت')    
    FAQ='سوالات',_('سوالات')     
    SEARCH='جستجو',_('جستجو')    
    VIDEO='ویدیو',_('ویدیو')
    ABOUT='درباره ما',_('درباره ما')
    CONTACT_HEADER='سربرگ ارتباط با ما',_('سربرگ ارتباط با ما')
    LOADING='لودینگ',_('لودینگ')
    LOGO='لوگو',_('لوگو')
    BIG_LOGO='لوگوی بزرگ',_('لوگوی بزرگ')
    DARK_LOGO='لوگوی تیره',_('لوگوی تیره')
    LIGHT_LOGO='لوگوی روشن',_('لوگوی روشن')
    BLOG_HEADER='سربرگ مقاله',_('سربرگ مقاله')
    OUR_WORK_HEADER='سربرگ پروژه',_('سربرگ پروژه')
    PAGE_HEADER_DEFAULT='سربرگ پیش فرض برای صفحات',_('سربرگ پیش فرض برای صفحات')
    ABOUT_HEADER='سربرگ درباره ما',_('سربرگ درباره ما')
    TAG_HEADER='سربرگ برچسب',_('سربرگ برچسب')
   
class ColorEnum(TextChoices):
    SUCCESS = 'success', _('success')
    DANGER = 'danger', _('danger')
    WARNING = 'warning', _('warning')
    PRIMARY = 'primary', _('primary')
    SECONDARY = 'secondary', _('secondary')
    INFO = 'info', _('info')
    LIGHT = 'light', _('light')
    ROSE = 'rose', _('rose')
    DARK = 'dark', _('dark') 

my_apps=[
        {
            'name':'charity',
            'title':'خیریه',
            'color':'primary',
            'url':'/charity/'
        },
        {
            'name':'todocalendar',
            'title':'سررسید',
            'color':'primary',
            'url':'/calendar/'
        },
        {
            'name':'drassistant',
            'title':'سلامت',
            'color':'danger',
            'url':'/drassistant/'
        },
        {
            'name':'projectmanager',
            'title':'مدیریت پروژه',
            'color':'success',
            'url':'/projectmanager/'
        },
        {
            'name':'stock',
            'title':'سهام',
            'color':'warning',
            'url':'/stock/'
        },
        {
            'name':'transport',
            'title':'حمل و نقل',
            'color':'rose',
            'url':'/transport/'
        },
        {
            'name':'market',
            'title':'مارکت',
            'color':'danger',
            'url':'/market/'
        },
        {
            'name':'leopusher',
            'title':'اطلاع رسانی',
            'color':'primary',
            'url':'/leopusher/'
        },
        {
            'name':'realestate',
            'title':'املاک',
            'color':'warning',
            'url':'/realestate/'
        },
        {
            'name':'vehicles',
            'title':'ماشین آلات',
            'color':'primary',
            'url':'/vehicles/'
        },
        {
            'name':'web',
            'title':'وب سایت',
            'color':'success',
            'url':'/'
        },
        {
            'name':'projectcontrol',
            'title':'کنترل پروژه',
            'color':'rose',
            'url':'/projectcontrol/'
        },
          {
            'name':'bms',
            'title':'ساختمان هوشمند',
            'color':'primary',
            'url':'/bms/'
        },
          {
            'name':'livestock',
            'title':'دامپروری',
            'color':'rose',
            'url':'/livestock/'
        },
    ]
    