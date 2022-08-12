from django import forms
from django.utils.safestring import mark_safe

class ListingForm(forms.Form):
    title = forms.CharField(label="Name of Listing", max_length=100, required=True)
    price = forms.IntegerField(label="Starting Bid (USD)", min_value=1, required=True)
    img = forms.ImageField(label="Insert Image", required=True)
    description = forms.CharField(label="Enter a Discription", max_length=500, required=True)
    category = forms.CharField(label="Enter a Category", max_length=50, required=False)

class BidForm(forms.Form):
    bid = forms.IntegerField(label="Place a Bid", min_value=1, required=True)