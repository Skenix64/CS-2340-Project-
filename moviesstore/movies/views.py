from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required

#movies = [
 #   {
  #      'id': 1, 'name': 'Back to the Future', 'price': 8.25,
   #     'description': 'A 1980s classic time travelling story where a California teen Marty Mcfly (Michael J. Fox) '
    #                   'travels back in time when an experiment conducted by his friend Doc Brown (Christopher Lloyd) '
     #                  'goes aray. Traveling through time in a DeLorean, Marty encounters his parents in 1955. He must '
      #                'present to prevent Doc Browns death. (Rated PG)'
#    },
#    {
#        'id': 2, 'name': '21 Jump Street', 'price': 10.99,
#        'description': 'Failed cops Schmidt (Jonah Hill) and Jenko (Channing Tatum) are forced to work at the '
#                       '21 Jump Street precinct. They use their youthful appearances to crack down on a dangerous drug '
#                       'ring operating at their old high school. The learn their high school is much different than '
#                       'before and suspect Eric (Dave Franco) to be the primary dealer'
#    },
#    {
#        'id': 3, 'name': 'The Interview', 'price': 14.99,
#        'description': 'Classic Seth Rogen and James Franco comedy that follows two reporters '
#                       'Aaron Rappaport (Seth Rogen) and David Skylark (James Franco) that were invited to '
#                       'interview North Korean dictator Kim Jong-un (Randall Park). They accept in the hopes to '
#                       'legitimize themselves as actual journalists. However as they prepare to embark to North Korea,'
#                       'the CIA recruits them to assassinate the dictator.'
#    },
#    {
#        'id': 4, 'name': 'Avengers Endgame', 'price': 25.99,
#        'description': 'Possibly the biggest movie of the 21st Century and the completion to the Infinity Saga. This'
#                       'movie is a continuation of the previous installment Avengers: Infinity War. '
##                       'Thanos the Mad Titan, collected all 6 Infinity Stones and erased half the universe. '
 #                      'The remaining Avengers Iron Man (Robert Downey Jr.), Captain America (Chris Evans)'
#                       'Thor (Chris Hemsworth), Hulk (Mark Ruffalo), Black Widow (Scarlet Johansson), '
#                       'Hawkeye (Jeremy Renner), Ant Man (Paul Rudd), War Machine (Don Cheadle), '
#                       'Rocket Racoon (Bradley Cooper), Nebula (Karen Gillan) band together and travel back in time to '
#                       'find the stones and reverse the "Blip." However, a Thanos from another timeline catches on to '
#                       'the Avengers plot.'
#    },
#]
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)


@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)