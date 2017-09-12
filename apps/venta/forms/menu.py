from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML, Button
from crispy_forms.bootstrap import FormActions, TabHolder, Tab, \
    PrependedAppendedText, PrependedText

from ..models.menu import Menu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ('',)

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)

        self.fields['tipo_menu'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')
        self.fields['fecha'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')

        self.helper = FormHelper()
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.form_id = 'form'

        self.helper.layout = Layout(
            Div(
                Field('tipo_menu', css_class='input-required'),
                Field('fecha', css_class='input-required'),
                css_class="modal-body",
            ),
            Div(
                FormActions(
                    smtSave(),
                    Button('cancel', 'Cancel', data_dismiss="modal", css_class="btn-default")
                ),
                css_class='modal-footer'
            )
        )
