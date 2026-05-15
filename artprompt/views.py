from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q, F, Value, Count, Avg, Max, Min
from django.db.models.functions import Length

from .models import ArtPrompt, Category, TagPrompt


def index(request):
    posts = (
        ArtPrompt.published
        .select_related("cat", "meta")
        .prefetch_related("tags")
    )

    data = {
        "title": "ArtPrompt — сайт для художников",
        "description": "Главная страница проекта с арт-промптами из базы данных.",
        "posts": posts,
        "db_categories": Category.objects.all(),
        "cat_selected": 0,
        "tags": TagPrompt.objects.all(),
    }

    return render(request, "artprompt/index.html", data)


def about(request):
    data = {
        "title": "О сайте ArtPrompt",
        "content": (
            "ArtPrompt — учебный Django-проект для художников. "
            "На сайте демонстрируется работа шаблонов, маршрутов, "
            "базы данных, связей между таблицами и ORM-запросов."
        ),
    }

    return render(request, "artprompt/about.html", data)


def categories(request):
    data = {
        "title": "Категории идей",
        "categories": [
            "Пейзаж",
            "Портрет",
            "Абстракция",
            "Акварель",
            "Цифровой арт",
            "Натюрморт",
        ],
        "db_categories": Category.objects.all(),
    }

    return render(request, "artprompt/categories.html", data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)

    posts = (
        ArtPrompt.published
        .filter(cat=category)
        .select_related("cat", "meta")
        .prefetch_related("tags")
    )

    data = {
        "title": f"Категория: {category.name}",
        "description": "Арт-промпты выбранной категории.",
        "posts": posts,
        "db_categories": Category.objects.all(),
        "cat_selected": category.id,
        "tags": TagPrompt.objects.all(),
    }

    return render(request, "artprompt/index.html", data)


def show_tag(request, tag_slug):
    tag = get_object_or_404(TagPrompt, slug=tag_slug)

    posts = (
        tag.prompts
        .filter(status=ArtPrompt.Status.PUBLISHED)
        .select_related("cat", "meta")
        .prefetch_related("tags")
    )

    data = {
        "title": f"Тег: {tag.tag}",
        "description": "Арт-промпты с выбранным тегом.",
        "posts": posts,
        "db_categories": Category.objects.all(),
        "cat_selected": None,
        "tags": TagPrompt.objects.all(),
        "selected_tag": tag.id,
    }

    return render(request, "artprompt/index.html", data)


def idea_by_id(request, idea_id):
    idea = get_object_or_404(
        ArtPrompt.objects
        .select_related("cat", "meta")
        .prefetch_related("tags"),
        pk=idea_id,
    )

    return render(request, "artprompt/idea_id.html", {"idea": idea})


def idea_by_slug(request, idea_slug):
    idea = get_object_or_404(
        ArtPrompt.objects
        .select_related("cat", "meta")
        .prefetch_related("tags"),
        slug=idea_slug,
    )

    return render(
        request,
        "artprompt/idea_slug.html",
        {
            "idea": idea,
            "get_params": request.GET.dict(),
        },
    )


def orm_examples(request):
    q_examples = ArtPrompt.objects.filter(
        Q(style__icontains="sci") | Q(title__icontains="лес")
    )

    f_examples = ArtPrompt.objects.filter(
        id__gt=F("cat_id")
    )

    value_examples = ArtPrompt.objects.annotate(
        source=Value("ArtPrompt project")
    ).values("title", "style", "source")

    length_examples = ArtPrompt.objects.annotate(
        title_length=Length("title")
    ).values("title", "title_length")

    aggregate_examples = ArtPrompt.objects.aggregate(
        total=Count("id"),
        avg_id=Avg("id"),
        max_id=Max("id"),
        min_id=Min("id"),
    )

    grouped_examples = Category.objects.annotate(
        total_prompts=Count("prompts")
    ).filter(total_prompts__gt=0)

    data = {
        "title": "Примеры ORM-запросов",
        "q_examples": q_examples,
        "f_examples": f_examples,
        "value_examples": value_examples,
        "length_examples": length_examples,
        "aggregate_examples": aggregate_examples,
        "grouped_examples": grouped_examples,
    }

    return render(request, "artprompt/orm_examples.html", data)


def archive(request, year):
    if year > 2023:
        raise Http404("Архив недоступен")

    return render(request, "artprompt/archive.html", {"year": year})


def search(request):
    style = request.GET.get("style", "")
    idea_type = request.GET.get("type", "")

    return render(
        request,
        "artprompt/search.html",
        {
            "style": style,
            "type": idea_type,
        },
    )


def generate(request):
    if request.method == "POST":
        return render(request, "artprompt/generate.html", {"generated": True})

    return render(request, "artprompt/generate.html", {"generated": False})


def go_home(request):
    return redirect("home")