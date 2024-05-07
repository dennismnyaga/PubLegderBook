# inventory/tasks.py
from celery import shared_task
from datetime import datetime, timedelta
from .models import Stock

@shared_task
def calculate_opening_closing_stock():
    # Calculate opening and closing stock for each item
    items = Stock.objects.values('item').distinct()
    for item in items:
        try:
            latest_stock = Stock.objects.filter(item=item['item']).latest('id')
            opening_stock = latest_stock.closing_stock
        except Stock.DoesNotExist:
            opening_stock = 0

        # Create a new stock entry for the current day
        Stock.objects.create(
            item_id=item['item'],
            opening_stock=opening_stock,
            received_stock=0,
            sold_stock=0,
            closing_stock=opening_stock,
        )
