from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, ListView, CreateView, DeleteView
from apps.article.forms import ArticleCreateForm, CommentCreateForm
from apps.article.models import Article, Comment


class ArticleCreateView(LoginRequiredMixin, FormView):
    form_class = ArticleCreateForm
    template_name = "article/create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        article = form.save(commit=False)
        breakpoint()
        article.author = self.request.user
        article.status = Article.STATUS.PUBLISHED
        article.save()
        return super().form_valid(form)


class ArticleListView(LoginRequiredMixin, ListView):
    queryset = Article.objects.all()
    template_name = "article/list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return (
            Article.objects.filter(
                status=Article.STATUS.PUBLISHED,
                is_deleted=False
            ).select_related("author")
            .order_by("-published_at")
        )


class ArticleDetailView(LoginRequiredMixin, DetailView):
    template_name = "article/detail.html"
    context_object_name = "article"
    queryset = Article.objects.all()
    slug_field = "slug"
    slug_url_kwarg = "slug"


class CommetCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentCreateForm
    model = Comment

    def form_valid(self, form):
        article_slug = self.kwargs.get("slug")
        article = get_object_or_404(Article, slug=article_slug)
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.article = article

        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment
            except Comment.DoesNotExist:
                pass
        comment.save()
        return redirect(article.get_absolute_url())


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("article_list")

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

