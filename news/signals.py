from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPortal import settings
from news.models import PostCategory
from .tasks import send_notifications

@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subs = []
        for i in categories:
            subs += i.subscriber.all()

        subs_mail = [sub.email for sub in subs]

        send_notifications.delay(
            preview=instance.preview(),
            pk=instance.pk,
            title=instance.title,
            sub_list=subs_mail,
        )

#@receiver(m2m_changed, sender=PostCategory)
#def notify_new_post(sender, instance, **kwargs):
    #if kwargs['action'] == 'post_add':
       # categories = instance.category.all()
       # subs = []
       # for i in categories:
          #  subs += i.subscriber.all()

     #   subs_mail = [sub.email for sub in subs]

       # send_notifications.delay(
      #      preview=instance.preview(),
      #      pk=instance.pk,
       #     title=instance.title,
       #     sub_list=subs_mail,
      #  )


#def send_notifications(preview, pk, title, subscribers):
   # html_content = render_to_string(
      #  'subscribers/post_created_email.html',
     #   {
         #   'text': preview,
    #        'link': f'{settings.SITE_URL}/news/{pk}'
    #    }

   # )

   # msg = EmailMultiAlternatives(
       # subject=title,
     #   body='',
     #   from_email=settings.DEFAULT_FROM_MAIL,
     #   to=subscribers,
 #   )

  #  msg.attach_alternative(html_content, 'text/html')
   # msg.send()



@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]


        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)


