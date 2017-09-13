from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML, Button
from crispy_forms.bootstrap import FormActions, TabHolder, Tab, \
    PrependedAppendedText, PrependedText

from ..models.insumos_detalle import InsumosDetalle


class InsumosDetalleForm(forms.ModelForm):
    class Meta:
        model = InsumosDetalle
        exclude = ('detalle',)

    def __init__(self, *args, **kwargs):
        super(InsumosDetalleForm, self).__init__(*args, **kwargs)

        self.fields['insumo'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')
        self.fields['cantidad'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')
        # print(kwargs['initial']['detalle_id'])
        self.helper = FormHelper()
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.form_id = 'form'

        self.helper.layout = Layout(
            Div(
                HTML('<button type="button" class="close" data-dismiss="modal" \
                aria-hidden="true">&times;</button>\
                <h4 class="modal-title"><i class="fa fa-info"></i>\
                Formulario Insumos detalle</h4>'),
                css_class="modal-header modal-header-primary",
            ),
            Div(
                Field('insumo', css_class='input-required select2', style="width:100%"),
                Field('cantidad', css_class='input-required'),
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
