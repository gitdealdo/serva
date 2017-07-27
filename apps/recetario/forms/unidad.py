from django import forms
# from crispy_forms.helper import FormHelper, Layout
# from crispy_forms.layout import Field, Div, Row  # , HTML
# from crispy_forms.bootstrap import FormActions  # , TabHolder, Tab, \
# # PrependedAppendedText, PrependedText

# from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.unidad import Unidad


class UnidadForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ('nombre', 'simbolo')
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder':
                       'Ingrese nombre', 'required': 'true'}),
            'simbolo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder':
                       'Ingrese símbolo', 'required': 'true'}),
        }


# class UnidadForm(forms.ModelForm):
#     class Meta:
#         model = Unidad
#         fields = ('nombre', 'simbolo',)

#     def __init__(self, *args, **kwargs):
#         super(UnidadForm, self).__init__(*args, **kwargs)

#         self.fields['nombre'].help_text = u'<small class="help-error"></small> %s' % (u' ')
#         self.fields['simbolo'].help_text = u'<small class="help-error"></small> %s' % (u' ')

#         self.fields['nombre'].widget.attrs = {'placeholder': 'Ingrese nombre', }
#         self.fields['simbolo'].widget.attrs = {'placeholder': 'Ingrese símbolo', }

#         self.helper = FormHelper()
#         self.helper.form_class = 'js-validate form-vertical'
#         self.helper.form_id = 'form'

#         self.helper.layout = Layout(

#             # Row(
#             #     Div(Field('nombre', css_class='input-required'), css_class='col-md-6'),
#             #     Div(Field('simbolo', css_class='input-required'), css_class='col-md-6'),
#             # ),
#             Field('nombre', css_class='input-required'),
#             Field('simbolo', css_class='input-required'),

#             FormActions(
#                 smtSave(),
#                 btnCancel(),
#                 btnReset(),
#             ),
#         )
