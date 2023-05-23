from django import forms
from .models import Profile, BlogPost
from django.core.exceptions import ValidationError
import pytoml

config_filepath = 'config.toml'

MAX_IMAGE_SIZE = 3 * 1024 * 1024 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_no', 'bio', 'facebook', 'instagram', 'linkedin', 'image', )    
   

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'slug', 'content', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title of the Blog'}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Copy the title with no space and a hyphen in between'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Content of the Blog'}),
        }

    def clean_image(self):
        image_file = self.cleaned_data.get('image_data')
        with open(config_filepath, 'rb') as f:            
            data = pytoml.load(f)
            image_size = data.get('image_validation')['image_size']
            image_format = data.get('image_validation')['image_formats']
            image_size_error = data.get('image_validation')['image_size_error']
            image_format_error = data.get('image_validation')['image_format_error']
        if image_file:            
            extension = image_file.name.split(".")[-1]          
            if image_file.size > image_size:
                raise ValidationError(image_size_error)
            if extension not in image_format:
                raise ValidationError(image_format_error)        
            return image_file


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].error_messages['invalid_image'] = 'Please upload a JPG or PNG image.'