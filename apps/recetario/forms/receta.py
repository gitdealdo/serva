from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row  # , HTML
from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.receta import Receta


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        exclude = ('autor',)

    def __init__(self, *args, **kwargs):
        super(RecetaForm, self).__init__(*args, **kwargs)

        self.fields['nombre'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')
        self.fields['porcion'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')
        self.fields['tipo_receta'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')
        self.fields['descripcion'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')
        self.fields['nombre'].widget.attrs = {
            'placeholder': 'Ingrese nombre de la receta'}
        self.fields['porcion'].widget.attrs = {
            'placeholder': 'Ingrese porciones'}
        self.fields['tipo_receta'].label = 'Tipo de receta'
        self.fields['descripcion'].widget.attrs = {
            'rows': 2, 'placeholder': 'Ingrese una breve descripción', }
        self.fields['preparacion'].widget = SummernoteWidget(
            attrs={'width': '100%', 'height': '35em'})

        self.helper = FormHelper()
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.form_id = 'form'

        self.helper.layout = Layout(

            Row(
                Div(Field('nombre', css_class='input-required'),
                    Field('porcion', css_class='input-required'),
                    Field('descripcion', ),
                    FieldWithButtons('tipo_receta',
                                     StrictButton("<i class='fa fa-plus'></i>",
                                                  css_class="btn-default",
                                                  rel="tooltip",
                                                  title="Agregar tipo receta",
                                                  data_toggle="modal",
                                                  data_target="#modal-id")),
                    Field('imagen', ),
                    css_class='col-md-6'),
                Div(Field('preparacion', css_class="input-required"),
                    css_class='col-md-6'),
            ),

            FormActions(
                smtSave(),
                btnCancel(),
                btnReset(),
            ),
        )
