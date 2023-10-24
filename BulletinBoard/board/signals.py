from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Comment, Mailing, User

from django.conf import settings

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

# возможность пользователя узнать об отклике на объявление от других пользователей
@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created and instance.author != instance.advertisement.author:
        send_mail(
            subject=f'Пользователь {instance.author.username} Оставил отклик на ваше объявление!',
            message=f'Проверьте страничку с откликами, чтобы принять или удалить это сообщение!\n\n{instance.content}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[instance.advertisement.author.email]
        )

#  возможность отправлять пользователям новостные рассылки
@receiver(post_save, sender=Mailing)
def send_mailing_notification(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject=f'{instance.title}',
            message=f'{instance.content}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=User.objects.values_list('email', flat=True),
        )
# уведомления о принятии/отклонении отклика
@receiver(post_save, sender=Comment)
def comment_approved(sender, instance, created, **kwargs):
    if instance.approve and instance.author != instance.advertisement.author:
        send_mail(
            subject=f'Ваш отклик был принят!',
            message=f'Пользователь {instance.advertisement.author.username} принял ваш отклик!'
                    f' Теперь вы его можете увидеть на странице объявления!',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[instance.author.email],
        )

@receiver(pre_delete, sender=Comment)
def comment_rejected(sender, instance, **kwargs):
    if instance.author != instance.advertisement.author:
        send_mail(
            subject=f'Ваш отклик был отклонён!',
            message=f'Пользователь {instance.advertisement.author.username} отклонил ваш отлик ваш отклик!',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[instance.author.email],
        )
