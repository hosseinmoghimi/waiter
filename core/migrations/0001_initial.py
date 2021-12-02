# Generated by Django 3.2.2 on 2021-10-01 12:22

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان')),
                ('sub_title', models.CharField(blank=True, max_length=300, null=True, verbose_name='زیر عنوان')),
                ('image_thumbnail_origin', models.ImageField(blank=True, null=True, upload_to='core/images/Page/Thumbnail/', verbose_name='تصویر کوچک')),
                ('archive', models.BooleanField(default=False, verbose_name='بایگانی شود؟')),
                ('for_home', models.BooleanField(default=False, verbose_name='نمایش در خانه')),
                ('panel', tinymce.models.HTMLField(blank=True, null=True, verbose_name='پنل')),
                ('short_description', tinymce.models.HTMLField(blank=True, null=True, verbose_name='توضیح کوتاه')),
                ('description', tinymce.models.HTMLField(blank=True, null=True, verbose_name='توضیح کامل')),
                ('image_header_origin', models.ImageField(blank=True, null=True, upload_to='core/images/Page/Header/', verbose_name='تصویر سربرگ')),
                ('image_main_origin', models.ImageField(blank=True, null=True, upload_to='core/images/Page/Main/', verbose_name='تصویر اصلی')),
                ('priority', models.IntegerField(default=100, verbose_name='اولویت / ترتیب')),
                ('status', models.CharField(blank=True, max_length=50, null=True, verbose_name='status')),
                ('color', models.CharField(blank=True, choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, null=True, verbose_name='رنگ')),
                ('meta_data', models.CharField(blank=True, max_length=100, null=True, verbose_name='متا دیتا')),
                ('app_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='نام اپ')),
                ('class_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='نام کلاس')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='افزوده شده در')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='اصلاح شده در')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.profile', verbose_name='ایجاد شده توسط')),
            ],
            options={
                'verbose_name': 'BasicPage',
                'verbose_name_plural': 'BasicPages',
            },
        ),
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='name')),
                ('icon_fa', models.CharField(blank=True, max_length=50, null=True, verbose_name='fa')),
                ('icon_material', models.CharField(blank=True, max_length=50, null=True, verbose_name='material_icon')),
                ('icon_svg', models.TextField(blank=True, null=True, verbose_name='svg_icon')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='color')),
                ('width', models.IntegerField(blank=True, null=True, verbose_name='عرض آیکون')),
                ('height', models.IntegerField(blank=True, null=True, verbose_name='ارتفاع آیکون')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='core/images/Icon/', verbose_name='تصویر آیکون')),
            ],
            options={
                'verbose_name': 'Icon',
                'verbose_name_plural': 'Icons',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='عنوان تصویر')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='شرح تصویر')),
                ('thumbnail_origin', models.ImageField(blank=True, null=True, upload_to='core/images/Gallery/Photo/Thumbnail/', verbose_name='تصویر کوچک')),
                ('image_main_origin', models.ImageField(blank=True, null=True, upload_to='core/images/Gallery/Photo/Main/', verbose_name='تصویر اصلی')),
                ('image_header_origin', models.ImageField(blank=True, null=True, upload_to='core/images/Gallery/Photo/Header/', verbose_name='تصویر سربرگ')),
                ('archive', models.BooleanField(default=False, verbose_name='بایگانی شود?')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('location', models.CharField(blank=True, max_length=50, null=True, verbose_name='موقعیت مکانی تصویر')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='افزوده شده در')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='اصلاح شده در')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.profile', verbose_name='پروفایل')),
            ],
            options={
                'verbose_name': 'GalleryPhoto',
                'verbose_name_plural': 'تصاویر',
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, choices=[('web', 'web'), ('stock', 'stock'), ('calendar', 'calendar'), ('resume', 'resume'), ('realestate', 'realestate'), ('projectmanager', 'projectmanager'), ('accounting', 'accounting'), ('help', 'help'), ('farm', 'farm'), ('core', 'core'), ('market', 'market')], max_length=20, null=True, verbose_name='app_name')),
                ('name', models.CharField(max_length=50, verbose_name='نام')),
                ('value_origin', models.CharField(blank=True, max_length=10000, null=True, verbose_name='مقدار')),
            ],
            options={
                'verbose_name': 'پارامتر',
                'verbose_name_plural': 'پارامتر ها',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=50, verbose_name='app_name')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('image_origin', models.ImageField(upload_to='core/images/picture/', verbose_name='image')),
            ],
            options={
                'verbose_name': 'Picture',
                'verbose_name_plural': 'Pictures',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('icon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.icon')),
                ('download_counter', models.IntegerField(default=0, verbose_name='تعداد دانلود')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('file', models.FileField(blank=True, null=True, upload_to='core/Document', verbose_name='فایل ضمیمه')),
                ('mirror_link', models.CharField(blank=True, max_length=10000, null=True, verbose_name='آدرس بیرونی')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='افزوده شده در')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='اصلاح شده در')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='پروفایل')),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'اسناد',
            },
            bases=('core.icon',),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('icon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.icon')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('url', models.CharField(default='#', max_length=2000, verbose_name='آدرس لینک')),
                ('new_tab', models.BooleanField(default=False, verbose_name='در صفحه جدید باز شود؟')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='افزوده شده در')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='اصلاح شده در')),
                ('profile_adder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='پروفایل')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'لینک ها',
            },
            bases=('core.icon',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.icon', verbose_name='icon')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='PageLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.basicpage', verbose_name='page')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'PageLike',
                'verbose_name_plural': 'PageLikes',
            },
        ),
        migrations.CreateModel(
            name='PageImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.image', verbose_name='image')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.basicpage', verbose_name='page')),
            ],
            options={
                'verbose_name': 'PageImage',
                'verbose_name_plural': 'PageImages',
            },
        ),
        migrations.CreateModel(
            name='PageComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', tinymce.models.HTMLField(verbose_name='comment')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.basicpage', verbose_name='page')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'PageComment',
                'verbose_name_plural': 'PageComments',
            },
        ),
        migrations.AddField(
            model_name='basicpage',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.icon', verbose_name='icon'),
        ),
        migrations.AddField(
            model_name='basicpage',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childs', to='core.basicpage', verbose_name='والد'),
        ),
        migrations.AddField(
            model_name='basicpage',
            name='related_pages',
            field=models.ManyToManyField(blank=True, to='core.BasicPage', verbose_name='صفحات مرتبط'),
        ),
        migrations.AddField(
            model_name='basicpage',
            name='tags',
            field=models.ManyToManyField(blank=True, to='core.Tag', verbose_name='برچسب ها'),
        ),
        migrations.CreateModel(
            name='NavLink',
            fields=[
                ('link_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.link')),
                ('app_name', models.CharField(choices=[('web', 'web'), ('stock', 'stock'), ('calendar', 'calendar'), ('resume', 'resume'), ('realestate', 'realestate'), ('projectmanager', 'projectmanager'), ('accounting', 'accounting'), ('help', 'help'), ('farm', 'farm'), ('core', 'core'), ('market', 'market')], max_length=50, verbose_name='app_name')),
            ],
            options={
                'verbose_name': 'NavLink',
                'verbose_name_plural': 'NavLinks',
            },
            bases=('core.link',),
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('link_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.link')),
                ('app_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='اپلیکیشن')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'SocialLink',
                'verbose_name_plural': 'شبکه اجتماعی',
            },
            bases=('core.link',),
        ),
        migrations.CreateModel(
            name='PageLink',
            fields=[
                ('link_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.link')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='links', to='core.basicpage', verbose_name='page')),
            ],
            options={
                'verbose_name': 'لینک صفحات',
                'verbose_name_plural': 'لینک های صفحات',
            },
            bases=('core.link',),
        ),
        migrations.CreateModel(
            name='PageDocument',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.document')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='core.basicpage', verbose_name='page')),
            ],
            bases=('core.document',),
        ),
    ]
