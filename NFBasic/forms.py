from django import forms


class NotificationForm(forms.Form):
    choices = (('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('All', 'All'))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, label='Title')
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label='Content')
    grade = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class': 'form-control'}), label='Grade')
    file = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}),
                           help_text='not required', label='File')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), max_length=30, label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30, label='Password')