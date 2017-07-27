from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row  # , HTML
from crispy_forms.bootstrap import FormActions  # , TabHolder, Tab, \
# PrependedAppendedText, PrependedText

from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.receta import Receta


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        exclude = ('user', 'costo',)

    def __init__(self, *args, **kwargs):
        super(RecetaForm, self).__init__(*args, **kwargs)

        self.fields['nombre'].help_text = u'<small class="help-error"></small> %s' % (u' ')
        self.fields['porcion'].help_text = u'<small class="help-error"></small> %s' % (u' ')
        self.fields['categoria'].help_text = u'<small class="help-error"></small> %s' % (u' ')
        self.fields['descripcion'].help_text = u'<small class="help-error"></small> %s' % (u' ')
        self.fields['preparacion'].help_text = u'<small class="help-error"></small> %s' % (u' ')

        self.fields['nombre'].widget.attrs = {'placeholder': 'Ingrese nombre de la receta'}
        self.fields['porcion'].widget.attrs = {'placeholder': 'Ingrese porciones'}
        self.fields['descripcion'].widget.attrs = {'rows': 2, }
        self.fields['preparacion'].widget.attrs = {'rows': 6, }

        self.helper = FormHelper()
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.form_id = 'form'

        self.helper.layout = Layout(

            Row(
                Div(Field('nombre', css_class='input-required'),
                    Field('porcion', css_class='input-required'),
                    Field('categoria', ),
                    Field('imagen', ),
                    css_class='col-md-6'),
                Div(Field('descripcion', ),
                    Field('preparacion', css_class="input-required"),
                    css_class='col-md-6'),
            ),

            FormActions(
                smtSave(),
                btnCancel(),
                btnReset(),
            ),
        )
