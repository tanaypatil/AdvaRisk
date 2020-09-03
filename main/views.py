from django.contrib.postgres.search import SearchQuery
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from .models import Review


def home(request):
    term = request.GET.get("search", "")
    if term:
        reviews = Review.objects.filter(search_vector=SearchQuery(term, search_type='raw')). \
            order_by('-score')
    else:
        reviews = Review.objects.all().order_by('-score')
    paginator = Paginator(reviews, 10)
    page = request.GET.get("page", 1)
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    context = {
        "reviews": reviews,
        "term": term
    }
    return render(request, "main/index.html", context=context)


@csrf_exempt
def search(request):
    if request.POST and request.is_ajax():
        term = request.POST['term']
        if not term:
            reviews = Review.objects.all().order_by('-score')
        else:
            reviews = Review.objects.filter(search_vector=SearchQuery(term, search_type='raw')). \
                order_by('-score')
        paginator = Paginator(reviews, 10)
        page = request.GET.get("page", 1)
        try:
            reviews = paginator.page(page)
        except PageNotAnInteger:
            reviews = paginator.page(1)
        except EmptyPage:
            reviews = paginator.page(paginator.num_pages)
        context = {
            "reviews": reviews,
            "term": term
        }
        review_template = render_to_string('main/review_boxes.html', context=context, request=request)
        pages_template = render_to_string('main/pages.html', context=context, request=request)
        return JsonResponse({'reviews': review_template, 'pages': pages_template, 'term': term})
