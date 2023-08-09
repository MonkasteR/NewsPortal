from .models import Post


def news_for_header(request):
    return {
        'news_for_header': Post.objects.order_by('-dateCreation')
    }
