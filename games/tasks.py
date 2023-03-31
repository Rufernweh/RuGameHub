from datetime import date, timedelta
from .models import GameAccount
from django.utils.timezone import now
from celery import shared_task

@shared_task
def update_game_status():
    # Tüm oyunları alın
    games = GameAccount.objects.all()

    # Her oyunu kontrol edin
    for game in games:
        # Oyunun son güncellenme tarihini hesaplayın
        last_updated = game.last_updated or game.created

        # Oyunun durumunu kontrol edin
        if now().date() - last_updated.date() > timedelta(days=30):
            # Oyunun son güncellenme tarihinden 30 günden fazla zaman geçtiyse, aktif olmayan olarak işaretleyin
            game.is_active = False
            game.save()