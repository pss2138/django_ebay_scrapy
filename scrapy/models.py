from django.db import models


class Results(models.Model):

    class Meta:
        db_table = "results_table"

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    price = models.FloatField()
    shippingcost = models.FloatField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    url = models.CharField(max_length=200)
    duration = models.FloatField()


    def __str__(self):
        return '%s %s %s' % (self.title, self.category, self.url)


class Recommendations(models.Model):

    class Meta:
        db_table = "table_recommendation"

    keyword = models.CharField(max_length=200)
    counts = models.FloatField()

    def __str__(self):
        return self.keyword


class Categories(models.Model):

    class Meta:
        db_table = "table_category"

    category = models.CharField(max_length=200)
    percentage = models.FloatField()

    def __str__(self):
        return self.category


class Price(models.Model):

    class Meta:
        db_table = "table_price"

    percentage = models.FloatField()
    price = models.FloatField()
    

class ShippingCost(models.Model):

    class Meta:
        db_table = "table_shippingcost"
    
    cost = models.FloatField()
    counts = models.FloatField()


class Duration(models.Model):

    class Meta:
        db_table = "table_duration"

    percentage = models.FloatField()
    duration = models.FloatField()   


class Related(models.Model):
    
    class Meta:
        db_table = "related_table"

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    price = models.FloatField()
    shippingcost = models.FloatField()
    url = models.CharField(max_length=200)
    watchcount = models.FloatField()

    def __str__(self):
        return '%s %s %s' % (self.title, self.category, self.url)
