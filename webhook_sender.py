import json
import time
import random
import requests
import logging
from datetime import datetime
from typing import Dict, Any
from google.protobuf.timestamp_pb2 import Timestamp
from apps.core.dtos.platform.v1.data_exchange_pb2 import (
    WebhookData, User, Product, Order, OrderItem, OrderStatus
)

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProtobufWebhookSender:
    """
    Protobuf format da webhook yuborish uchun klass
    """
    
    def __init__(self, webhook_url: str = "http://localhost:8000/api/protobuf-receiver/"):
        self.webhook_url = webhook_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/x-protobuf',
            'User-Agent': 'ProtobufWebhookSender/1.0'
        })
    
    def create_timestamp(self) -> Timestamp:
        """Hozirgi vaqtdan Timestamp yaratadi"""
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        return timestamp
    
    def create_sample_user(self) -> User:
        """Namuna User yaratadi"""
        user = User()
        user.id = random.randint(1, 10000)
        user.name = random.choice([
            "Alisher Navoi", "Mirza Ulug'bek", "Abu Ali ibn Sino", 
            "Bobur Mirzo", "Amir Temur", "Al-Xorazmi"
        ])
        user.email = f"user{user.id}@example.uz"
        user.age = random.randint(18, 65)
        user.is_active = random.choice([True, False])
        user.created_at.CopyFrom(self.create_timestamp())
        return user
    
    def create_sample_product(self) -> Product:
        """Namuna Product yaratadi"""
        product = Product()
        product.id = random.randint(1, 1000)
        products_data = [
            ("Moshina", "Tez va ishonchli transport", 50000.0, "Transport"),
            ("Telefon", "Zamonaviy smartphone", 1200.0, "Texnologiya"),
            ("Kitob", "Ilmiy adabiyot", 25.0, "Ta'lim"),
            ("Noutbuk", "Professional ish uchun", 1500.0, "Texnologiya"),
            ("Kiyim", "Sifatli kiyim", 80.0, "Moda"),
        ]
        
        name, desc, price, category = random.choice(products_data)
        product.name = name
        product.description = desc
        product.price = price
        product.category = category
        product.quantity = random.randint(1, 100)
        product.created_at.CopyFrom(self.create_timestamp())
        return product
    
    def create_sample_order(self) -> Order:
        """Namuna Order yaratadi"""
        order = Order()
        order.id = random.randint(1, 50000)
        order.user_id = random.randint(1, 10000)
        
        # Order items qo'shish
        items_count = random.randint(1, 5)
        total = 0.0
        
        for i in range(items_count):
            item = order.items.add()  # Repeated field ga element qo'shish
            item.product_id = random.randint(1, 1000)
            item.product_name = f"Product_{item.product_id}"
            item.quantity = random.randint(1, 10)
            item.unit_price = round(random.uniform(10.0, 500.0), 2)
            item.total_price = round(item.quantity * item.unit_price, 2)
            total += item.total_price
        
        order.total_amount = round(total, 2)
        order.status = random.choice([
            OrderStatus.ORDER_STATUS_PENDING,
            OrderStatus.ORDER_STATUS_CONFIRMED,
            OrderStatus.ORDER_STATUS_SHIPPED
        ])
        order.created_at.CopyFrom(self.create_timestamp())
        return order
    
    def create_webhook_data(self, event_type: str) -> WebhookData:
        """Webhook uchun data yaratadi"""
        webhook_data = WebhookData()
        webhook_data.event_type = event_type
        webhook_data.event_id = f"evt_{random.randint(100000, 999999)}"
        webhook_data.timestamp.CopyFrom(self.create_timestamp())
        
        if event_type == "user_created":
            webhook_data.user_data.CopyFrom(self.create_sample_user())
        elif event_type == "product_updated":
            webhook_data.product_data.CopyFrom(self.create_sample_product())
        elif event_type == "order_placed":
            webhook_data.order_data.CopyFrom(self.create_sample_order())
        
        return webhook_data
    
    def send_webhook(self, webhook_data: WebhookData) -> bool:
        """Webhook yuboradi"""
        try:
            # Protobuf ni binary formatga o'tkazish
            binary_data = webhook_data.SerializeToString()
            
            logger.info(f"Webhook yuborilmoqda: {webhook_data.event_type}")
            logger.info(f"Data o'lchami: {len(binary_data)} bytes")
            
            # JSON formatda ham ko'rsatish (o'rganish uchun)
            logger.info(f"JSON format: {self.protobuf_to_dict(webhook_data)}")
            
            response = self.session.post(
                self.webhook_url,
                data=binary_data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ Webhook muvaffaqiyatli yuborildi!")
                return True
            else:
                logger.error(f"❌ Webhook yuborishda xato: {response.status_code} - {response.text}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"❌ Network xatosi: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Kutilmagan xato: {e}")
            return False
    
    def protobuf_to_dict(self, message) -> Dict[str, Any]:
        """Protobuf ni dict ga o'tkazadi (debug uchun)"""
        from google.protobuf.json_format import MessageToDict
        return MessageToDict(message)
    
    def run_continuous_sender(self, interval_seconds: int = 30):
        """Muntazam ravishda webhook yuboradi"""
        logger.info(f"Webhook sender boshlandi. Har {interval_seconds} sekundda yuboriladi.")
        logger.info(f"Maqsad: {self.webhook_url}")
        
        event_types = ["user_created", "product_updated", "order_placed"]
        
        try:
            while True:
                # Random event type tanlash
                event_type = random.choice(event_types)
                
                # Webhook data yaratish va yuborish
                webhook_data = self.create_webhook_data(event_type)
                self.send_webhook(webhook_data)
                
                # Keyingi yuborishgacha kutish
                logger.info(f"⏰ {interval_seconds} sekund kutilmoqda...")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            logger.info("🛑 Webhook sender to'xtatildi (Ctrl+C)")
        except Exception as e:
            logger.error(f"❌ Kutilmagan xato: {e}")


def main():
    """Asosiy funksiya"""
    # Agar siz boshqa servis localhost:8002/test-data/ da ishlayotgan bo'lsa:
    # webhook_url = "http://localhost:8002/test-data/"
    
    # Default Django receiver uchun:
    webhook_url = "http://localhost:8000/api/protobuf-receiver/"
    
    sender = ProtobufWebhookSender(webhook_url)
    
    # Test uchun bir marta yuborish
    logger.info("📤 Test webhook yuborilmoqda...")
    test_data = sender.create_webhook_data("user_created")
    sender.send_webhook(test_data)
    
    # Muntazam yuborish
    sender.run_continuous_sender(interval_seconds=30)


if __name__ == "__main__":
    main()