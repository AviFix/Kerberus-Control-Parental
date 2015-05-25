from django.db import models

class Anuncio(models.Model):
    descripcion = models.CharField(max_length=200,blank=True)
    url=models.URLField()
    path_imagen=models.CharField(max_length=255)
  #  relevancia=models.IntegerField()

    def __unicode__(self):
        return self.descripcion

#    class Meta:
#        ordering = ['relevancia']
#
