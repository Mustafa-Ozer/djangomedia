from django.db import models

# Create your models here.
class usersAbout(models.Model):
    user = models.ForeignKey("auth.user",on_delete=models.CASCADE)
    about = models.CharField(max_length=50,verbose_name="Hakkınızda")
    phone = models.CharField(max_length=50,verbose_name="Telefon")
    prof = models.CharField(max_length=50,verbose_name="İş")
    links = models.CharField(max_length=50,verbose_name="Websiteleriniz")
    pphoto = models.FileField(blank=True,null=True,verbose_name="Profil Fotoğrafı Ekle")
    def __str__(self):
        return self.about