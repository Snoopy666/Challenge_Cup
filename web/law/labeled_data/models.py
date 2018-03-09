from django.db import models

# Create your models here.


class Data(models.Model):
    data = models.TextField()
    crit = models.IntegerField()
    time = models.IntegerField()
    num_labeled = models.IntegerField(default=0)
    num_labeling = models.IntegerField(default=0)

    def __str__(self):
        return 'Data: ' + str(self.pk)


class User(models.Model):
    name = models.CharField(max_length=128)
    passwd = models.CharField(max_length=128)
    labeling = models.ForeignKey(Data, on_delete=models.SET_NULL, null=True)
    num_labeled = models.IntegerField(default=0)
    allowed_crit = models.IntegerField(default=-1)

    def __str__(self):
        return 'User: ' + self.name


class Label(models.Model):
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    label = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'User: %s => Data: %d' % (self.author.name, self.data.pk)


class LabelId(models.Model):
    crit = models.IntegerField()
    label_id = models.IntegerField()
    name = models.CharField(max_length=128)