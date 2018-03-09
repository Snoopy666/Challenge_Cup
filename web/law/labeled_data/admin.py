from django.contrib import admin
from labeled_data.models import User, Data, Label, LabelId
# Register your models here.


class DataAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'short_data', 'num_labeling', 'num_labeled_')

    def num_labeled_(self, obj):
        return obj.num_labeled - obj.num_labeling

    def short_data(self, obj):
        return obj.data[:55] + '...'


class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'num_labeled', 'labeling')


class LabelAdmin(admin.ModelAdmin):
    fields = ('data', 'label', 'author')

    def colored_data(self, obj):
        return obj.data


admin.site.register(User, UserAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(LabelId)