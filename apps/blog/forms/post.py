from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab, \
    PrependedAppendedText, PrependedText

from ..models.post import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields['title'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')
        self.fields['body'].help_text = u'<small class="help-error"></small> %s' % (
            u' ')

        self.fields['body'].widget.attrs = {'rows': 3, }
        self.fields['body'].label = 'Cuerpo'

        self.helper = FormHelper()
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.form_id = 'form'

        self.helper.layout = Layout(

            Row(
                Div(Field('title', css_class='input-required'),
                    css_class='col-md-6'),
                Div(Field('body', css_class="input-required"),
                    css_class='col-md-6'),

            ),
            Row(
                Div(Field('asd', css_class='input-required'),
                    css_class='col-md-6'),
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )
