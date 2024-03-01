from django.db import models

class Quotation(models.Model):
    quote_no = models.CharField(max_length=128)
    logo = models.ImageField(null=True, blank=True)
    from_contact = models.CharField(max_length=128)
    from_email = models.EmailField(max_length=128)
    from_name = models.CharField(max_length=128)
    to_contact = models.CharField(max_length=128)
    to_email = models.EmailField()
    to_name = models.CharField(max_length=128)
    notes = models.CharField(max_length=128)
    
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quote_no}'
    
    class Meta:
        ordering = ['-last_modified']



class LineItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='line_items')
    description = models.CharField(max_length=128)
    rate = models.PositiveIntegerField(default=1)
    quantity = models.PositiveIntegerField(default=1)   
    amount = models.PositiveIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.created_on}'
