from django import forms
# from crispy_forms.helper import FormHelper, Layout
# from crispy_forms.layout import Field, Div, Row  # , HTML
# from crispy_forms.bootstrap import FormActions  # , TabHolder, Tab, \
# # PrependedAppendedText, PrependedText

# from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.categoria import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nombre',)
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder':
                       'Ingrese nombre', 'required': 'true'}),
        }


# class TipoForm(forms.ModelForm):
#     class Meta:
#         model = Tipo
#         fields = ('nombre',)

#     def __init__(self, *args, **kwargs):
#         super(TipoForm, self).__init__(*args, **kwargs)

#         self.fields['nombre'].help_text = u'<small class="help-error"></small> %s' % (u' ')

#         self.fields['nombre'].widget.attrs = {'placeholder': 'Ingrese nombre', }

#         self.helper = FormHelper()
#         self.helper.form_class = 'js-validate form-vertical'
#         self.helper.form_id = 'form'

#         self.helper.layout = Layout(

#             Field('nombre', css_class='input-required'),

#             FormActions(
#                 smtSave(),
#                 btnCancel(),
#                 btnReset(),
#             ),
#         )
