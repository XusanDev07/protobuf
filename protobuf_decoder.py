import json
import logging
from typing import Dict, Any, Optional
from google.protobuf.message import Message
from google.protobuf.json_format import MessageToDict
from apps.core.dtos.platform.v1.data_exchange_pb2 import WebhookData, WebhookResponse

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProtobufDecoder:
    """
    Protobuf formatdagi ma'lumotlarni decode qilish uchun klass
    """
    
    @staticmethod
    def decode_webhook_data(binary_data: bytes) -> Optional[WebhookData]:
        """
        Binary formatdagi protobuf ma'lumotlarni WebhookData ga o'tkazadi
        
        Args:
            binary_data: Protobuf binary ma'lumotlari
            
        Returns:
            WebhookData obyekti yoki None (agar decode qila olmasa)
        """
        try:
            webhook_data = WebhookData()
            webhook_data.ParseFromString(binary_data)
            return webhook_data
        except Exception as e:
            logger.error(f"Protobuf decode qilishda xato: {e}")
            return None
    
    @staticmethod
    def protobuf_to_json(message: Message) -> str:
        """
        Protobuf message ni JSON stringga o'tkazadi
        
        Args:
            message: Protobuf message obyekti
            
        Returns:
            JSON format string
        """
        try:
            return json.dumps(MessageToDict(message), indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"JSON ga o'tkazishda xato: {e}")
            return "{}"
    
    @staticmethod
    def protobuf_to_dict(message: Message) -> Dict[str, Any]:
        """
        Protobuf message ni Python dict ga o'tkazadi
        
        Args:
            message: Protobuf message obyekti
            
        Returns:
            Python dictionary
        """
        try:
            return MessageToDict(message)
        except Exception as e:
            logger.error(f"Dict ga o'tkazishda xato: {e}")
            return {}
    
    def process_webhook_data(self, binary_data: bytes) -> Dict[str, Any]:
        """
        Webhook ma'lumotlarini to'liq ishlov beradi
        
        Args:
            binary_data: Protobuf binary ma'lumotlari
            
        Returns:
            Ishlov berilgan ma'lumotlar (dict format)
        """
        logger.info(f"📥 Protobuf ma'lumotlari qabul qilindi: {len(binary_data)} bytes")
        
        # Binary datani decode qilish
        webhook_data = self.decode_webhook_data(binary_data)
        if not webhook_data:
            logger.error("❌ Ma'lumotlarni decode qila olmadim!")
            return {"error": "Decode failed"}
        
        # Ma'lumotlarni dict formatga o'tkazish
        data_dict = self.protobuf_to_dict(webhook_data)
        
        # Event typega qarab boshqacha ishlov berish
        event_type = webhook_data.event_type
        logger.info(f"📋 Event turi: {event_type}")
        logger.info(f"🆔 Event ID: {webhook_data.event_id}")
        
        # Ma'lumotlarni konsolga chiqarish
        if webhook_data.HasField("user_data"):
            self._process_user_data(webhook_data.user_data)
        elif webhook_data.HasField("product_data"):
            self._process_product_data(webhook_data.product_data)
        elif webhook_data.HasField("order_data"):
            self._process_order_data(webhook_data.order_data)
        
        # JSON formatda ham ko'rsatish
        logger.info(f"📄 JSON format:\\n{self.protobuf_to_json(webhook_data)}")
        
        return data_dict
    
    def _process_user_data(self, user):
        """User ma'lumotlarini ishlov beradi"""
        logger.info("👤 Foydalanuvchi ma'lumotlari:")
        logger.info(f"  - ID: {user.id}")
        logger.info(f"  - Ism: {user.name}")
        logger.info(f"  - Email: {user.email}")
        logger.info(f"  - Yosh: {user.age}")
        logger.info(f"  - Faol: {'Ha' if user.is_active else 'Yoq'}")
        logger.info(f"  - Yaratilgan: {user.created_at.ToDatetime()}")
    
    def _process_product_data(self, product):
        """Product ma'lumotlarini ishlov beradi"""
        logger.info("🛍️ Mahsulot ma'lumotlari:")
        logger.info(f"  - ID: {product.id}")
        logger.info(f"  - Nom: {product.name}")
        logger.info(f"  - Tavsif: {product.description}")
        logger.info(f"  - Narx: ${product.price}")
        logger.info(f"  - Kategoriya: {product.category}")
        logger.info(f"  - Miqdor: {product.quantity}")
        logger.info(f"  - Yaratilgan: {product.created_at.ToDatetime()}")
    
    def _process_order_data(self, order):
        """Order ma'lumotlarini ishlov beradi"""
        logger.info("🛒 Buyurtma ma'lumotlari:")
        logger.info(f"  - Buyurtma ID: {order.id}")
        logger.info(f"  - Foydalanuvchi ID: {order.user_id}")
        logger.info(f"  - Umumiy summa: ${order.total_amount}")
        
        # Status ni string formatda ko'rsatish
        status_names = {
            0: "Kutilmoqda",
            1: "Tasdiqlangan",
            2: "Yuborilgan",
            3: "Yetkazilgan",
            4: "Bekor qilingan"
        }
        logger.info(f"  - Status: {status_names.get(order.status, 'Nomalum')}")
        logger.info(f"  - Yaratilgan: {order.created_at.ToDatetime()}")
        
        # Buyurtma elementlarini ko'rsatish
        logger.info(f"  - Elementlar soni: {len(order.items)}")
        for i, item in enumerate(order.items, 1):
            logger.info(f"    {i}. {item.product_name} - {item.quantity} x ${item.unit_price} = ${item.total_price}")
    
    def create_response(self, success: bool, message: str = "") -> bytes:
        """
        Webhook uchun response yaratadi
        
        Args:
            success: Muvaffaqiyatli yoki yo'q
            message: Qo'shimcha xabar
            
        Returns:
            Binary format response
        """
        response = WebhookResponse()
        response.success = success
        response.message = message
        response.processed_at.GetCurrentTime()
        
        return response.SerializeToString()


def demo_decode():
    """
    Decode qilish demo funksiyasi
    Bu funksiya webhook_sender.py dan kelgan ma'lumotlarni qabul qilish uchun ishlatiladi
    """
    decoder = ProtobufDecoder()
    
    # Bu demo - amalda webhook orqali kelgan binary datani decode qiladi
    logger.info("🔧 Protobuf Decoder tayyor!")
    logger.info("📡 Webhook ma'lumotlarini kutmoqda...")
    
    # Django view yoki Flask route da foydalanish mumkin
    # binary_data = request.body  # Django da
    # decoded_data = decoder.process_webhook_data(binary_data)
    
    return decoder


if __name__ == "__main__":
    demo_decode()