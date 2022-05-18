from django.db import models


class NewPageModel(models.Model):
    """Creates a model class for new pages. Database not actually being used as data stored in files."""
    name = models.CharField(max_length=100)
    contents = models.TextField()
    id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return self.name