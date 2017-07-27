from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field  # , Div  , Row, HTML
from crispy_forms.bootstrap import FormActions  # , TabHolder, Tab, \
# PrependedAppendedText, PrependedText

from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.ingrediente import Ingrediente


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        exclude = ('receta',)

    def __init__(self, *args, **kwargs):
        super(IngredienteForm, self).__init__(*args, **kwargs)

        self.fields['producto'].help_text = u'<small class="help-error"></small> %s' % (u' ')
        self.fields['cantidad'].help_text = u'<small class="help-error"></small> %s' % (u' ')

        self.helper = FormHelper()
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.form_id = 'form'

        self.helper.layout = Layout(

            Field('producto', css_class='input-required'),
            Field('cantidad', css_class='input-required'),

            FormActions(
                smtSave(),
                btnCancel(),
                btnReset(),
            ),
        )
