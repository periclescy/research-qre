from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


# ------------- OPTION ------------- #
class PostOption(admin.ModelAdmin):
    list_display = ('id', 'sample_count', 'countdown_per_pic', 'language', 'headline_el', 'headline_en',
                    'instructions_el', 'instructions_en', 'footer_el', 'footer_en')


class MyOption(Option):
    class Meta:
        proxy = True
        verbose_name_plural = "~ Import/Export Options"


class MyOptionIEAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Option, PostOption)
admin.site.register(MyOption, MyOptionIEAdmin)


# ------------- PAIR ------------- #
class PostPair(admin.ModelAdmin):
    list_display = ('id',
                    'image_pri', 'caption_pri_el', 'caption_pri_en',
                    'image_sec', 'caption_pri_el', 'caption_pri_en',
                    'description_el', 'description_en')


class MyPair(Pair):
    class Meta:
        proxy = True
        verbose_name_plural = "~ Import/Export Pairs"


class MyPairIEAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Pair, PostPair)
admin.site.register(MyPair, MyPairIEAdmin)


# ------------- TARGET ------------- #
class PostTarget(admin.ModelAdmin):
    list_display = ('id', 'pair', 'x_pri', 'y_pri', 'w_pri', 'h_pri', 'x_sec', 'y_sec', 'w_sec', 'h_sec')


class MyTarget(Target):
    class Meta:
        proxy = True
        verbose_name_plural = "~ Import/Export Targets"


class MyTargetIEAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Target, PostTarget)
admin.site.register(MyTarget, MyTargetIEAdmin)


# ------------- USER ------------- #
class PostUser(admin.ModelAdmin):
    list_display = ('id', 'session', 'gender', 'age', 'education', 'sector',
                    'knowledge')


class MyUser(User):
    class Meta:
        proxy = True
        verbose_name_plural = "~ Import/Export Users"


class MyUserIEAdmin(ImportExportModelAdmin):
    pass


admin.site.register(User, PostUser)
admin.site.register(MyUser, MyUserIEAdmin)


# ------------- DATA ------------- #
class PostData(admin.ModelAdmin):
    list_display = ('id', 'session', 'timestamp', 'status', 'score', 'pair', 'filename_pri', 'filename_sec',
                    'xtl_pri', 'ytl_pri', 'xbr_pri', 'ybr_pri', 'xtl_sec', 'ytl_sec', 'xbr_sec', 'ybr_sec',
                    'countdown_per_pic')


class MyData(Data):
    class Meta:
        proxy = True
        verbose_name_plural = "~ Import/Export Data"


class MyDataIEAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Data, PostData)
admin.site.register(MyData, MyDataIEAdmin)


# ------------- RANK ------------- #
class PostRank(admin.ModelAdmin):
    list_display = ('id', 'session', 'pair', 'success', 'failure', 'accuracy', 'response')


class MyRank(Data):
    class Meta:
        proxy = True
        verbose_name_plural = "~ Import/Export Rank"


class MyRankIEAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Rank, PostRank)
admin.site.register(MyRank, MyRankIEAdmin)
