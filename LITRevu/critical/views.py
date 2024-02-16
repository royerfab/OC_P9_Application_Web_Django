from itertools import chain

from django.shortcuts import render, redirect
from .models import Review, Ticket, UserFollows
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ReviewForm
from django.contrib.auth.models import User
from django.db.models import Q
from django import template
from django.db.models import CharField, Value


'''
Home page, display all tickets and reviews from the user and the followed users.

Parameters:
    request: objet contenant toutes les informations de la requête.

Returns:
    tupple contenant : toutes les informations de la requête, le template de la page html,un dictionnaire de la liste 
    des dictionnaires des informations des critiques et des tickets.

'''
@login_required
def home(request):
    #récupérer tous les user follows et trier pour ceux suivis par ce user
    #UserFollows.objects.filter(user=request.user) Ici il y a les user et les followed_user. Récupérern dedans une liste de followed_user
    #followed = UserFollows.objects.filter(user=request.user)
    #ici on récupère l'enensemble des infos UserFollows de l'utilisateur, la ligne suivante fait la même chose que la précédente
    #l'une en allant chercher le nom du champ et l'autre le name
    followed = request.user.following.all()
    following_list = [userfollow.followed_user for userfollow in followed]
    reviews = Review.objects.filter(
        Q(user__in=following_list) | Q(user=request.user))
    reviews = reviews.annotate(content_type=Value("Review", CharField()))
    print(reviews)
    tickets = Ticket.objects.filter(
        Q(user__in=following_list) | Q(user=request.user))
    tickets = tickets.annotate(content_type=Value("Ticket", CharField()))
    print(tickets)

    reviews_and_tickets = sorted(
        chain(reviews, tickets),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    print(reviews_and_tickets)
    context = {
        'reviews_and_tickets': reviews_and_tickets,
    }
    return render(request, 'critical/home.html', context=context)

'''
Create a new ticket, asking for the creation of a review.

Parameters:
    request: objet contenant toutes les informations de la requête.

Returns:
    tupple contenant : toutes les informations de la requête, le template de la page html,
    le formulaire de création d'un ticket.

'''
@login_required
def add_ticket(request):
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            # créer un nouveau « Ticket » et le sauvegarder dans la db
            #commit false crée l'objet sans l'enregistrer dans la base de données
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')

    return render(request,
            'critical/add_ticket.html',
            {'form': form})

'''
Create a new review, from an existing ticket.

Parameters:
    request: objet contenant toutes les informations de la requête.
    ticket_id : id du ticket à partir duquel une critique va être créé.

Returns:
    tupple contenant : toutes les informations de la requête, le template de la page html,un dictionnaire de la liste 
    des dictionnaires des informations des tickets et le formulaire de création d'une critique.
'''
@login_required
def add_review(request, ticket_id):
    form = ReviewForm()
    ticket = Ticket.objects.get(id=ticket_id)
    if ticket.review_set.exists():
        return redirect('home')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # créer une nouvelle « Review » et la sauvegarder dans la db
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')

    return render(request,
            'critical/add_review.html',
            {'form': form, 'ticket': ticket})

'''
Create a new ticket and at the same time a new review for this ticket.

Parameters:
    request: objet contenant toutes les informations de la requête.

Returns:
    tupple contenant : toutes les informations de la requête, le template de la page html,un dictionnaire de la liste des
     dictionnaires des formulaires pour créer des critiques et des tickets

'''
@login_required
def add_ticket_and_review(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')



    return render(request,
            'critical/add_ticket_and_review.html',
            {'ticket_form': ticket_form, 'review_form': review_form})


'''
Display all tickets and reviews from the user, with the possibility to update or remove them.

Parameters:
    request: objet contenant toutes les informations de la requête.

Returns:
    tupple contenant : toutes les informations de la requête, le template de la page html,un dictionnaire de la liste des
     dictionnaires des informations des critiques et des tickets

'''
@login_required
def ticket_list(request):
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value("Review", CharField()))
    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value("Ticket", CharField()))

    reviews_and_tickets = sorted(
        chain(reviews, tickets),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    return render(request,
                  'critical/posts.html',
                  {'reviews_and_tickets': reviews_and_tickets})

def review_list(request):
    reviews = Review.objects.all()
    return render(request,
                  'critical/posts.html',
                  {'reviews': reviews})

def review_detail(request, review_id):
    review = Review.objects.get(id=review_id)
    return render(request,
                  'critical/posts.html',
                  {'review': review})

'''
Update an already existing ticket.

Parameters:
    request: objet contenant toutes les informations de la requête.
    id : id du ticket à modifier.

Returns:
    tupple contenant toutes les informations de la requête, le template de la page html,un dictionnaire de la liste des
     dictionnaires des informations du formulaire pour modifier un ticket existant.

'''
@login_required
def update_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    form = TicketForm(instance=ticket)

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('posts')

    return render(request,
                'critical/update_ticket.html',
                {'form': form})

'''
Update an already existing review.

Parameters:
    request: objet contenant toutes les informations de la requête.
    id : id de la critique à modifier.

Returns:
    tupple contenant toutes les informations de la requête, le template de la page html,un dictionnaire de la liste des
     dictionnaires des informations des tickets et du formulaire pour modifier une critique existante.

'''
@login_required
def update_review(request, id):
    review = Review.objects.get(id=id)
    form = ReviewForm(instance=review)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('posts')

    return render(request,
                'critical/update_review.html',
                {'form': form, 'review': review})

'''
Delete an already existing ticket.

Parameters:
    request: objet contenant toutes les informations de la requête.
    id : id du ticket à supprimer.

Returns:
    tupple contenant toutes les informations de la requête, le template de la page html,un dictionnaire de la liste des
     dictionnaires des informations des tickets.

'''
@login_required
def delete_ticket(request, id):
    ticket = Ticket.objects.get(id=id)

    if request.method == 'POST':
        ticket.delete()
        return redirect('home')
    return render(request,
                    'critical/delete_ticket.html',
                    {'ticket': ticket})

'''
Update an already existing review.

Parameters:
    request: objet contenant toutes les informations de la requête.
    id : id de la critique à supprimer.

Returns:
    tupple contenant toutes les informations de la requête, le template de la page html,un dictionnaire de la liste des
     dictionnaires des informations des critiques.

'''
@login_required
def delete_review(request, id):
    review = Review.objects.get(id=id)
    #review.delete()
    #return redirect('posts')
    if request.method == 'POST':
        review.delete()
        return redirect('home')

    return render(request,
                    'critical/delete_review.html',
                    {'review': review})

'''
Display all the followed and following users of the user, possibility to subscribe or unsubscribe.

Parameters:
    request: objet contenant toutes les informations de la requête.

Returns:
    tupple contenant toutes les informations de la requête, le template de la page html.

'''
@login_required
def follow(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'follow':
            username = request.POST.get('username')
            #on cherche l'utilisateur avec filter
            user = User.objects.filter(username=username).first()

            if user:
                if user != request.user:
                    #ici user est l'utilisateur qu'on est allé chercher et folloed_user est l'utilisateur actuel donc request
                    userfollow = UserFollows(user=request.user, followed_user=user)
                    userfollow.save()
        elif action == 'unfollow':
            id = request.POST.get('id')
            userfollow = UserFollows.objects.get(id=id)
            userfollow.delete()
    return render(request,
                  'critical/follow.html')

