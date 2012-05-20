# coding: utf-8

from django import forms


class PostBackForm(forms.Form):
    token = forms.CharField(max_length=255, required=True)
