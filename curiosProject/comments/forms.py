from django import forms
class CommentForm(forms.Form):
    #content_type = forms.CharField(widget=forms.HiddenInput)
    #object_id = forms.IntegerField(widget=forms.HiddenInput)
    #parent_id=forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(max_length=400,widget=forms.TextInput(attrs={'placeholder': 'Make a comment'}))