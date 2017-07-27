from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row  # , HTML
from crispy_forms.bootstrap import FormActions  # , TabHolder, Tab, \
# PrependedAppendedText, PrependedText

from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.producto import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = ('',)

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)

        self.fields['nombre'].help_text = u'<small class="help-error"></small> %s' % (u' ')
        self.fields['unidad'].help_text = u'<small class="help-error"></small> %s' % (u' ')
        self.fields['tipo'].help_text = u'<small class="help-error"></small> %s' % (u' ')
        self.fields['costo'].help_text = u'<small class="help-error"></small> %s' % (u' ')

        self.fields['descripcion'].widget.attrs = {'rows': 2, }
        self.fields['nombre'].widget.attrs = {'placeholder': 'Ingrese nombre del producto'}
        self.fields['tipo'].label = 'Tipo/Categoria'
        self.fields['costo'].label = 'Costo por unidad'

        self.helper = FormHelper()
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.form_id = 'form'

        self.helper.layout = Layout(

            Row(
                Div(Field('nombre', css_class='input-required'), css_class='col-md-6'),
                Div(Field('tipo', css_class='input-required'), css_class='col-md-6'),
                Div(Field('cantidad', ), css_class='col-md-6'),
                Div(Field('unidad', css_class="input-required"), css_class='col-md-6'),
                Div(Field('costo', css_class="input-required"), css_class='col-md-6'),
                Div(Field('descripcion', ), css_class='col-md-6'),
            ),

            FormActions(
                smtSave(),
                btnCancel(),
                btnReset(),
            ),
        )
