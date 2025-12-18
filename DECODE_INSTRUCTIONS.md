# 🔧 Manual Decode Instructions - Localhost:8002 uchun

Bu faylda localhost:8002/test-data/ endpoint-iga kelgan protobuf ma'lumotlarini qanday decode qilish haqida batafsil ko'rsatma berilgan.

## 🎯 Vazifa: Boshqa loyihada protobuf ma'lumotlarni qabul qilish

Sizning localhost:8002/test-data/ endpoint-ida protobuf ma'lumotlarni qabul qilish va decode qilish uchun quyidagi amallarni bajaring:

### 1️⃣ Proto fayl nusxasini ko'chirish

Avval bu loyihadagi proto faylni boshqa loyihangizga ko'chiring:

```bash
# Proto faylni ko'chirish
cp protos/platform/v1/data_exchange.proto /path/to/your/other/project/
```

### 2️⃣ Boshqa loyihada protobuf o'rnatish

```bash
pip install protobuf grpcio-tools
```

### 3️⃣ Proto faylni compile qilish

Boshqa loyihangizda:

```bash
# Python uchun protobuf fayllarini generate qilish
python -m grpc_tools.protoc \
    --python_out=. \
    --grpc_python_out=. \
    --proto_path=. \
    data_exchange.proto

# Natijada data_exchange_pb2.py fayli paydo bo'ladi
```

### 4️⃣ Decoder kodni yozish

Boshqa loyihangizda quyidagi kodni qo'shing:

```python
# decode_protobuf.py

from data_exchange_pb2 import WebhookData
from google.protobuf.json_format import MessageToDict
import json

def decode_protobuf_webhook(binary_data):
    """
    Binary protobuf ma'lumotlarini decode qiladi
    
    Args:
        binary_data: POST request.body dan olingan bytes
    
    Returns:
        dict: Decode qilingan ma'lumotlar
    """
    try:
        # Binary datani WebhookData ga o'tkazish
        webhook_data = WebhookData()
        webhook_data.ParseFromString(binary_data)
        
        # Ma'lumotlarni dict formatga o'tkazish
        data_dict = MessageToDict(webhook_data)
        
        print(f"📥 Protobuf ma'lumot qabul qilindi!")
        print(f"📋 Event turi: {webhook_data.event_type}")
        print(f"🆔 Event ID: {webhook_data.event_id}")
        print(f"⏰ Vaqt: {webhook_data.timestamp.ToDatetime()}")
        
        # Ma'lumot turiga qarab ishlov berish
        if webhook_data.HasField("user_data"):
            user = webhook_data.user_data
            print(f"👤 Foydalanuvchi: {user.name} ({user.email})")
            
        elif webhook_data.HasField("product_data"):
            product = webhook_data.product_data
            print(f"🛍️ Mahsulot: {product.name} - ${product.price}")
            
        elif webhook_data.HasField("order_data"):
            order = webhook_data.order_data
            print(f"🛒 Buyurtma: #{order.id} - ${order.total_amount}")
        
        # JSON formatda ham qaytarish
        print(f"📄 JSON format:")
        print(json.dumps(data_dict, indent=2, ensure_ascii=False))
        
        return data_dict
        
    except Exception as e:
        print(f"❌ Decode xatosi: {e}")
        return None

# Test funksiyasi
if __name__ == "__main__":
    print("🔧 Protobuf Decoder tayyor!")
    print("📡 Binary ma'lumotlarni decode qilish uchun decode_protobuf_webhook() funksiyasini chaqiring")
```

### 5️⃣ Django/Flask da ishlatish

#### Django uchun:

```python
# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from .decode_protobuf import decode_protobuf_webhook

logger = logging.getLogger(__name__)

@csrf_exempt
def test_data_endpoint(request):
    if request.method == "POST":
        try:
            # Binary ma'lumotni olish
            binary_data = request.body
            
            logger.info(f"📨 Protobuf ma'lumot keldi: {len(binary_data)} bytes")
            
            # Protobuf ni decode qilish
            decoded_data = decode_protobuf_webhook(binary_data)
            
            if decoded_data:
                # Ma'lumotlarni ma'lumotlar bazasiga saqlash
                # save_to_database(decoded_data)
                
                return JsonResponse({
                    "success": True,
                    "message": "Protobuf ma'lumot muvaffaqiyatli ishlov berildi",
                    "event_type": decoded_data.get("eventType", "unknown"),
                    "data_size": len(binary_data)
                })
            else:
                return JsonResponse({
                    "success": False,
                    "message": "Protobuf decode qila olmadim"
                }, status=400)
                
        except Exception as e:
            logger.error(f"Xato: {e}")
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=500)
    
    # GET request uchun
    return JsonResponse({
        "message": "Protobuf webhook endpoint",
        "status": "ready",
        "instructions": "POST request bilan protobuf binary data yuboring"
    })
```

#### Flask uchun:

```python
# app.py

from flask import Flask, request, jsonify
import logging
from decode_protobuf import decode_protobuf_webhook

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route('/test-data/', methods=['GET', 'POST'])
def test_data_endpoint():
    if request.method == "POST":
        try:
            # Binary ma'lumotni olish
            binary_data = request.get_data()
            
            logger.info(f"📨 Protobuf ma'lumot keldi: {len(binary_data)} bytes")
            
            # Protobuf ni decode qilish
            decoded_data = decode_protobuf_webhook(binary_data)
            
            if decoded_data:
                # Ma'lumotlarni ma'lumotlar bazasiga saqlash
                # save_to_database(decoded_data)
                
                return jsonify({
                    "success": True,
                    "message": "Protobuf ma'lumot muvaffaqiyatli ishlov berildi",
                    "event_type": decoded_data.get("eventType", "unknown"),
                    "data_size": len(binary_data)
                })
            else:
                return jsonify({
                    "success": False,
                    "message": "Protobuf decode qila olmadim"
                }), 400
                
        except Exception as e:
            logger.error(f"Xato: {e}")
            return jsonify({
                "success": False,
                "message": str(e)
            }), 500
    
    # GET request uchun
    return jsonify({
        "message": "Protobuf webhook endpoint",
        "status": "ready",
        "instructions": "POST request bilan protobuf binary data yuboring"
    })

if __name__ == '__main__':
    app.run(host='localhost', port=8002, debug=True)
```

### 6️⃣ URL sozlamalari

#### Django uchun (urls.py):

```python
from django.urls import path
from . import views

urlpatterns = [
    path('test-data/', views.test_data_endpoint, name='test_data'),
]
```

### 7️⃣ Test qilish

Boshqa loyihangizni ishga tushiring:

```bash
# Django uchun
python manage.py runserver 8002

# Flask uchun
python app.py
```

Keyin ushbu loyihadan webhook yuborish:

```bash
cd /path/to/protobuf-learning-project
source venv/bin/activate
python webhook_sender_8002.py
```

### 8️⃣ Ma'lumotlarni saqlash

Decode qilingan ma'lumotlarni ma'lumotlar bazasiga saqlash uchun:

```python
def save_to_database(decoded_data):
    """Decode qilingan protobuf ma'lumotlarini ma'lumotlar bazasiga saqlaydi"""
    
    event_type = decoded_data.get('eventType')
    
    if event_type == 'user_created' and 'userData' in decoded_data:
        user_data = decoded_data['userData']
        # User modelga saqlash
        # User.objects.create(
        #     external_id=user_data['id'],
        #     name=user_data['name'],
        #     email=user_data['email'],
        #     age=user_data.get('age'),
        #     is_active=user_data.get('isActive', True)
        # )
        
    elif event_type == 'product_updated' and 'productData' in decoded_data:
        product_data = decoded_data['productData']
        # Product modelga saqlash yoki yangilash
        
    elif event_type == 'order_placed' and 'orderData' in decoded_data:
        order_data = decoded_data['orderData']
        # Order modelga saqlash
```

### 🔍 Debug va Monitoring

Log fayllarini kuzatish uchun:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('protobuf_receiver.log'),
        logging.StreamHandler()
    ]
)
```

### ✅ Natija

Shundan keyin sizning localhost:8002/test-data/ endpoint-ingiz:

1. ✅ Protobuf binary ma'lumotlarini qabul qiladi
2. ✅ Ularni decode qiladi
3. ✅ Ma'lumotlar turini aniqlaydi (user, product, order)
4. ✅ Ma'lumotlarni JSON formatda ko'rsatadi
5. ✅ Ma'lumotlar bazasiga saqlaydi (ixtiyoriy)
6. ✅ Response qaytaradi

Har 30 sekundda yangi protobuf ma'lumotlar keladi va siz ularni to'liq decode qila olasiz! 🎉