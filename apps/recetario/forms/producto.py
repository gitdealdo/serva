from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row  # , HTML
from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton
# TabHolder, Tab, PrependedAppendedText, PrependedText

from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.producto import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = ('',)

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)

        self.fields['nombre'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')
        self.fields['unidad'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')
        self.fields['categoria'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')
        self.fields['costo'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')

        self.fields['descripcion'].widget.attrs = {'rows': 2, }
        self.fields['nombre'].widget.attrs = {
            'placeholder': 'Ingrese nombre del producto'}
        self.fields['categoria'].label = 'Tipo producto'
        self.fields['costo'].label = 'Costo por unidad'

        self.helper = FormHelper()
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.form_id = 'form'

        self.helper.layout = Layout(

            Row(
                Div(Field('nombre', css_class='input-required'),
                    css_class='col-md-6'),
                Div(FieldWithButtons('categoria',
                                     StrictButton("<i class='fa fa-plus'></i>", css_class="btn-default", rel="tooltip", title="Agregar tipo", data_toggle="modal", data_target="#modal-id")), css_class='col-md-6'),
                Div(Field('stock_minimo', ), css_class='col-md-6'),
                Div(Field('stock', ), css_class='col-md-6'),
                Div(FieldWithButtons('unidad',
                                     StrictButton("<i class='fa fa-plus'></i>", css_class="btn-default", rel="tooltip", title="Agregar unidad", data_toggle="modal", data_target="#modal-unidad")), css_class='col-md-6'),
                Div(Field('costo', css_class="input-required"),
                    css_class='col-md-6'),
                Div(Field('descripcion', ), css_class='col-md-6'),
            ),

            FormActions(
                smtSave(),
                btnCancel(),
                btnReset(),
            ),
        )


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()
    # widgets = {
    #     'file': forms.FileInput(attrs={'class': 'form-control'}),
    # }
