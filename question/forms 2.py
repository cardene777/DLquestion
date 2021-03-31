from django import forms
from .models import Question, QuestionTitle


class QuestionTitleForm(forms.ModelForm):
    class Meta:
        model = QuestionTitle
        fields = ('title', 'about', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control title'
        self.fields['title'].widget.attrs['placeholder'] = '問題タイトル(必須)'
        self.fields['title'].widget.attrs['maxlength'] = '200'
        self.fields['about'].widget.attrs['class'] = 'form-control about'
        self.fields['about'].widget.attrs['placeholder'] = '概要(必須)'
        self.fields['image'].widget.attrs['class'] = 'image'
        self.fields['image'].widget.attrs['placeholder'] = '画像(任意)'