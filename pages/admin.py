from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


# ------------- OPTION ------------- #
class PostOption(admin.ModelAdmin):
    list_display = ('id', 'brake_time', 'headline', 'instructions', 'footer')


class MyOption(Option):
    class Meta:
        proxy = True
        verbose_name_plural = "~ Import/Export Options"


class MyOptionIEAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Option, PostOption)
admin.site.register(MyOption, MyOptionIEAdmin)


# ------------- USER ------------- #
class PostUser(admin.ModelAdmin):
    list_display = ('id', 'team', 'session', 'gender', 'age', 'education', 'district', 'residence')


class MyUser(User):
    class Meta:
        proxy = True
        verbose_name_plural = "~ Import/Export Users"


class MyUserIEAdmin(ImportExportModelAdmin):
    pass


admin.site.register(User, PostUser)
admin.site.register(MyUser, MyUserIEAdmin)


# ------------- SECTION ------------- #
class PostSection(admin.ModelAdmin):
    list_display = ('id', 'section', 'answer_category')


class MySection(Question):
    class Meta:
        proxy = True
        verbose_name_plural = "~ Import/Export Sections"


class MySectionIEAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Section, PostSection)
admin.site.register(MySection, MySectionIEAdmin)


# ------------- QUESTION ------------- #
class PostQuestion(admin.ModelAdmin):
    list_display = ('id', 'section', 'question', 'section')


class MyQuestion(Question):
    class Meta:
        proxy = True
        verbose_name_plural = "~ Import/Export Questions"


class MyQuestionIEAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Question, PostQuestion)
admin.site.register(MyQuestion, MyQuestionIEAdmin)


# ------------- DATA ------------- #
class PostData(admin.ModelAdmin):
    list_display = ('id', 'session', 'timestamp',  'status', 'section', 'question', 'selection', 'team')


class MyData(Data):
    class Meta:
        proxy = True
        verbose_name_plural = "~ Import/Export Data"


class MyDataIEAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Data, PostData)
admin.site.register(MyData, MyDataIEAdmin)
