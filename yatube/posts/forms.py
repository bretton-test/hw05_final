from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Форма публикации"""

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = 'текст поста'


class CommentForm(forms.ModelForm):
    """Форма комментария"""

    class Meta:
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs[
            'placeholder'
        ] = 'текст вашего комментария'
