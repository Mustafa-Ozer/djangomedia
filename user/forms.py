from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label = "Kullanıcı Adı")
    password = forms.CharField(label = "Parola",widget = forms.PasswordInput)


class RegisterForm(forms.Form):
        name = forms.CharField(min_length=3,max_length=20,label="İsim\n")
        surname = forms.CharField(min_length=2,max_length=20,label="Soyisim\n")
        username = forms.CharField(min_length=4,max_length=22,label = "Kullanıcı Adı\n")
        email = forms.CharField(min_length=10,max_length=50,label = "Email\n")
        password = forms.CharField(min_length=5,max_length=25,label="Parola\n",widget=forms.PasswordInput)
        confirm = forms.CharField(max_length=25,widget=forms.PasswordInput,label="Doğrula")
        def clean(self):
            name = self.cleaned_data.get("name")
            surname = self.cleaned_data.get("surname")
            username = self.cleaned_data.get("username")
            email = self.cleaned_data.get("email")
            password = self.cleaned_data.get("password")
            confirm  = self.cleaned_data.get("confirm")
            if password and confirm and password!=confirm:
                raise forms.ValidationError("Parolalar Eşleşmiyor!")
            values = {
                "name" : name,
                "surname":surname,
                "username": username,
                "email" : email,
                "password" : password,
            }
            return values


