from django.db import models


class Review(models.Model):
    user = models.ForeignKey('User', verbose_name='Автор отзыва',
                             on_delete=models.CASCADE,
                             related_name='reviewer')
    author = models.ForeignKey('User', verbose_name='Автор поста',
                               on_delete=models.CASCADE,
                               related_name='author')
    text = models.TextField()
    score = models.IntegerField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created',)

    def __str__(self):
        return (
            f'Автор поста {self.author.username}, '
            f'Автор отзыва {self.user.username}, '
            f'Текст {self.text[:20]}, '
            f'Дата {self.created}'
        )


class Comment(models.Model):
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='comments'
    )
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return (
            f'Автор: {self.author.username}, '
            f'Название: {self.title}, '
            f'Текст: {self.text[:20]}, '
            f'Дата: {self.created}'
        )
