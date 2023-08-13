from .models import Post


def news_for_header(request):
    return {
        'news_for_header': Post.objects.order_by('-dateCreation')
    }


def news_pk(request):
    return {
        'news_pk': Post.objects.get(pk=request)
        # 'news_pk': Post.objects.get(pk=request.form.get('pk'))
    }
