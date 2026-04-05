from django import forms

class DirectoryImportForm(forms.Form):
    directory_path = forms.CharField(
        label="path to data directory",
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '/home/user/data/'})
    )