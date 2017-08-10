from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import Group
from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm  # UserChangeForm
# _*_ coding: utf-8 _*_
# from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from crispy_forms.helper import FormHelper, Layout
# Fieldset, ButtonHolder, Submit, Button, Reset, HTML
from crispy_forms.layout import Field, Submit, Div, Row
# PrependedText,  AppendedText,PrependedAppendedText
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from ..models import Person

User = get_user_model()


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['first_name'] = forms.CharField(
            label=capfirst(_(u'first name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['last_name'] = forms.CharField(
            label=capfirst(_(u'last name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['identity_type'] = forms.CharField(
            label=capfirst(_(u'identity type')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['birth_date'] = forms.DateField(
            label=capfirst(_(u'birth date')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['identity_type'].widget = forms.Select(
            choices=Person.IDENTITY_TYPE_CHOICES)
        self.fields['identity_num'] = forms.CharField(
            label=capfirst(_(u'identity num')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['cellphone'] = forms.CharField(
            label=capfirst(_(u'cellphone')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['address'] = forms.CharField(
            label=capfirst(_(u'address')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['grupo'] = forms.ModelChoiceField(
            label='Rol', queryset=Group.objects.all(), initial=0)
        self.fields['photo'] = forms.ImageField(
            label=capfirst(_(u'Photo')), required=False,
            initial='persons/user.png',
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Available formats are JPG, GIF, and PNG.'),
        )
        self.fields['acept'] = forms.BooleanField(
            label=capfirst(
                _(u'I accept the Terms of Service and Privacy Policy.')),
            required=True,
            # widget=forms.CheckboxInput(),
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )

        self.helper = FormHelper()
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(
                    Field('email',),
                    Field('username', autofocus=True,
                          css_class='input-required'),
                    Field('password1',),
                    Field('password2',),
                    css_class='col-md-4'),
                Div(
                    Field('grupo',),
                    Field('first_name',),
                    Field('last_name',),
                    Field('identity_type',),
                    Field('identity_num',),
                    Field('birth_date',),
                    css_class='col-md-4'),
                Div(
                    Field('cellphone',),
                    Field('address',),
                    Field('photo'),
                    Field('acept',),
                    css_class='col-md-4'),
            ),
            FormActions(
                smtSave(),
                btnCancel(),
                css_class='pull-right'
            ),
        )


class UserPersonForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(UserPersonForm, self).__init__(*args, **kwargs)

        self.fields['first_name'] = forms.CharField(
            label=capfirst(_(u'first name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['last_name'] = forms.CharField(
            label=capfirst(_(u'last name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['identity_type'] = forms.CharField(
            label=capfirst(_(u'identity type')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['birth_date'] = forms.DateField(
            label=capfirst(_(u'birth date')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['identity_type'].widget = forms.Select(
            choices=Person.IDENTITY_TYPE_CHOICES)
        self.fields['identity_num'] = forms.CharField(
            label=capfirst(_(u'identity num')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['cellphone'] = forms.CharField(
            label=capfirst(_(u'cellphone')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['address'] = forms.CharField(
            label=capfirst(_(u'address')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['about'] = forms.CharField(
            label=capfirst(_(u'My description')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['about'].widget = SummernoteWidget(
            attrs={'width': '100%', 'height': '25em'})
        self.fields['photo'] = forms.ImageField(
            label=capfirst(_(u'Photo')), required=False,
            initial='persons/user.png',
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Available formats are JPG, GIF, and PNG.'),
        )

        self.helper = FormHelper()
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(
                    Field('email',),
                    Field('first_name',),
                    Field('last_name',),
                    Field('identity_type',),
                    Field('identity_num',),
                    css_class='col-md-4'),
                Div(
                    Field('birth_date',),
                    Field('cellphone',),
                    Field('address',),
                    Field('photo'),
                    css_class='col-md-4'),
                Div(
                    Field('about',),
                    css_class='col-md-4'),
            ),
            FormActions(
                smtSave(),
                css_class='pull-right'
            ),
        )


# class PasswordChangeForm(PasswordChangeForm):
#     error_css_class = 'has-error'
#     error_messages = {'password_incorrect': "Contraseña incorrecta"}
#     old_password = forms.CharField(required=True, widget=forms.PasswordInput(
#         attrs={'class': 'form-control'}),
#         error_messages={'required': 'Το συνθηματικό δε μπορεί να είναι κενό'})
#     new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(
#         attrs={'class': 'form-control'}),
#         error_messages={'required': 'Το συνθηματικό δε μπορεί να είναι κενό'})
#     new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(
#         attrs={'class': 'form-control'}),
#     error_messages={'required': 'Το συνθηματικό δε μπορεί να είναι κενό'})


class PasswordChangeCustomForm(forms.Form):

    oldpassword = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'placeholder': 'Ingrese contraseña anterior',
               'class': 'form-control'}), label="Contraseña anterior")
    newpassword1 = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'placeholder': 'Ingrese contraseña nueva',
               'class': 'form-control'}), label='Contraseña nueva')
    newpassword2 = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirme contraseña nueva',
               'class': 'form-control'}), label='Confirme contraseña nueva')

    def clean(self):
        if 'newpassword1' in self.cleaned_data and 'newpassword2' in self.cleaned_data:
            if self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
