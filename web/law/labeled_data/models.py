from django.db import models

# Create your models here.


class Data(models.Model):
    STATUS_CHOICE = (
        ('U', 'Unlabeled'),
        ('I', 'Labeling'),
        ('L', 'Labeled'),
        ('A', 'Abandoned')
    )

    data = models.TextField()
    crit = models.IntegerField()
    time = models.IntegerField()
    label = models.TextField(default="")
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default='U')


class User(models.Model):
    name = models.CharField(max_length=128)
    passwd = models.CharField(max_length=128)
    labeling = models.ForeignKey(Data, on_delete=models.SET_NULL, null=True)
    num_labeled = models.IntegerField(default=0)


class LabelId(models.Model):
    crit = models.IntegerField()
    label_id = models.IntegerField()
    name = models.CharField(max_length=128)
