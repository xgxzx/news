from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_title',
            'category',
            'post_text',
            'author',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("post_text")
        if text is not None and len(text) < 20:
            raise ValidationError(
                "Пост слишком мал. Необходимо более 20 символов."
            )
        return cleaned_data
