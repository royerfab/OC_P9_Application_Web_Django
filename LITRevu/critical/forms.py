from django import forms
from critical.models import Ticket, Review, UserFollows

class TicketForm(forms.ModelForm):
   class Meta:
     model = Ticket
     exclude = ('user',)

class ReviewForm(forms.ModelForm):
   class Meta:
     model = Review
     exclude = ('user', 'ticket')
