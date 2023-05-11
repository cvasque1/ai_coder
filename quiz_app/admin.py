from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Quiz, Question, AnswerChoice

class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with email as the unique identifier"""
    ordering = ('email',)
    list_display = ('email', 'company_name', 'is_staff')
    search_fields = ('email', 'company_name')
    readonly_fields = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('company_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'company_name', 'password1', 'password2'),
        }),
    )


class QuestionInline(admin.TabularInline):
    model = Quiz.questions.through


class QuizAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
    ]
    exclude = ('questions',)


class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerChoiceInline,
    ]



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
