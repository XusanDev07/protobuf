# protobuf
Bu loyiha Protocol Buffers (Protobuf) texnologiyasini o'rganish va amalda qo'llash uchun mo'ljallangan. JSON formatdan farqli o'laroq, Protobuf binary format bo'lib, ma'lumotlarni tezroq va samaraliroq uzatish imkonini beradi.

## 📋 Loyiha Haqida

Ushbu loyihada quyidagi amaliy vazifalar amalga oshiriladi:

1. **Protobuf Schema** yaratish va Python kodiga o'tkazish
2. **Webhook Sender** - har 30 sekundda protobuf formatda ma'lumot yuborish
3. **Webhook Receiver** - kelgan protobuf ma'lumotlarini qabul qilish va decode qilish
4. **Django Integration** - web service sifatida ishlatish

## 🛠️ Texnologiyalar

- **Python 3.10+**
- **Django 5.2** - web framework
- **Protocol Buffers** - ma'lumot serializatsiya formati
- **grpcio-tools** - protobuf fayllarini compile qilish uchun
- **requests** - HTTP so'rovlar yuborish uchun

## 📂 Loyiha Tuzilishi

```
protobuf/
├── protos/                          # Protobuf schema fayllari
│   └── platform/v1/
│       ├── data_exchange.proto      # Asosiy data exchange schema
│       ├── entities.proto           # Boshqa entitylar
│       └── events.proto             # Event-lar uchun
├── apps/core/
│   ├── dtos/                        # Generated Python protobuf files
│   └── views.py                     # Django webhook receiver
├── webhook_sender.py                # Django receiver ga yuboruvchi (port 8000)
├── webhook_sender_8002.py          # Sizning loyihangizga yuboruvchi (port 8002)
├── protobuf_decoder.py             # Ma'lumotlarni decode qiluvchi
├── generate_protobuf.py            # Protobuf compiler script
├── test_protobuf.py                # Test va demo script
├── start_project.sh                # Loyihani ishga tushirish script
├── README_UZ.md                    # Ushbu ko'rsatma (o'zbek tilida)
├── DECODE_INSTRUCTIONS.md          # Boshqa loyihada decode qilish ko'rsatmasi
└── requirements.txt                # Python dependencies
```

## 📋 Asosiy Fayllar

### `webhook_sender.py`
- Django receiver ga ma'lumot yuboradi (localhost:8000)
- Test va o'rganish uchun ishlatiladi

### `webhook_sender_8002.py` ⭐
- Sizning asosiy loyihangizga ma'lumot yuboradi (localhost:8002/test-data/)
- Har 30 sekundda protobuf ma'lumot yuboradi
- Bu fayl sizning asosiy vazifangiz uchun

### `DECODE_INSTRUCTIONS.md` ⭐
- Boshqa loyihangizda protobuf ma'lumotlarni qanday decode qilish haqida
- Django va Flask uchun misollar
- Copy-paste uchun tayyor kod

## 🔧 O'rnatish va Sozlash

### 1-qadam: Virtual Environment yaratish

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# yoki Windows da: venv\\Scripts\\activate
```

### 2-qadam: Bog'liqliklarni o'rnatish

```bash
pip install -r requirements.txt
```

### 3-qadam: Protobuf fayllarini compile qilish

```bash
python generate_protobuf.py
```

Bu buyruq `protos/` papkasidagi `.proto` fayllarini Python kodiga o'tkazadi va `apps/core/dtos/` papkasiga joylashtiradi.

### 4-qadam: Django ma'lumotlar bazasini sozlash

```bash
python manage.py migrate
```

## 🚀 Loyihani Ishga Tushirish

### Variant 1: Django Receiver (test uchun)

Bu variant ushbu loyiha ichida webhook qabul qiluvchini ishlatadi:

#### Django Server (1-terminal)
```bash
source venv/bin/activate
python manage.py runserver 8000
```

#### Webhook Sender (2-terminal)
```bash
source venv/bin/activate
python webhook_sender.py
```

### Variant 2: Boshqa loyihangizga yuborish (localhost:8002)

Bu variant sizning asl vazifangiz uchun - boshqa loyihangizga protobuf ma'lumot yuborish:

#### 1-qadam: Boshqa loyihangizni ishga tushiring
```bash
# Sizning boshqa loyihangizni localhost:8002 da ishga tushiring
# Bu loyiha /test-data/ endpoint-iga ega bo'lishi kerak
```

#### 2-qadam: Webhook Sender ishga tushirish
```bash
source venv/bin/activate
python webhook_sender_8002.py
```

#### 3-qadam: Protobuf ma'lumotlarni decode qilish
Boshqa loyihangizda protobuf ma'lumotlarni decode qilish uchun `DECODE_INSTRUCTIONS.md` faylidagi ko'rsatmalarni bajaring.

## 📡 Protobuf Schema Tushunchasi

### Asosiy Message Turlari

#### 1. User Message
```protobuf
message User {
    int64 id = 1;           # Foydalanuvchi ID raqami
    string name = 2;        # Foydalanuvchi ismi
    string email = 3;       # Email manzil
    int32 age = 4;          # Yoshi
    bool is_active = 5;     # Faol yoki yo'q
    google.protobuf.Timestamp created_at = 6;  # Yaratilgan vaqt
}
```

#### 2. Product Message
```protobuf
message Product {
    int64 id = 1;           # Mahsulot ID
    string name = 2;        # Mahsulot nomi
    string description = 3; # Tavsif
    double price = 4;       # Narx
    string category = 5;    # Kategoriya
    int32 quantity = 6;     # Miqdor
    google.protobuf.Timestamp created_at = 7;
}
```

#### 3. Order Message
```protobuf
message Order {
    int64 id = 1;           # Buyurtma ID
    int64 user_id = 2;      # Foydalanuvchi ID
    repeated OrderItem items = 3;  # Buyurtma elementlari ro'yxati
    double total_amount = 4;       # Umumiy summa
    OrderStatus status = 5;        # Buyurtma holati
    google.protobuf.Timestamp created_at = 6;
}
```

#### 4. WebhookData Message (Asosiy)
```protobuf
message WebhookData {
    string event_type = 1;    # Event turi: "user_created", "order_placed", ...
    string event_id = 2;      # Unique event ID
    google.protobuf.Timestamp timestamp = 3;  # Event vaqti
    
    // oneof - faqat bitta field bo'ladi
    oneof data {
        User user_data = 4;
        Product product_data = 5;
        Order order_data = 6;
    }
}
```

## 🔍 Ma'lumotlarni Decode Qilish

### 1. Binary Ma'lumotlarni Qabul Qilish

```python
from apps.core.dtos.platform.v1.data_exchange_pb2 import WebhookData

def receive_protobuf_data(binary_data):
    # Binary datani protobuf obyektiga o'tkazish
    webhook_data = WebhookData()
    webhook_data.ParseFromString(binary_data)
    
    print(f"Event turi: {webhook_data.event_type}")
    print(f"Event ID: {webhook_data.event_id}")
```

### 2. Ma'lumot Turini Tekshirish

```python
# Qaysi turdagi ma'lumot kelganini tekshirish
if webhook_data.HasField("user_data"):
    user = webhook_data.user_data
    print(f"Yangi foydalanuvchi: {user.name} ({user.email})")

elif webhook_data.HasField("product_data"):
    product = webhook_data.product_data
    print(f"Mahsulot yangilanishi: {product.name} - ${product.price}")

elif webhook_data.HasField("order_data"):
    order = webhook_data.order_data
    print(f"Yangi buyurtma: #{order.id} - ${order.total_amount}")
```

### 3. JSON Formatga O'tkazish

```python
from google.protobuf.json_format import MessageToDict
import json

# Protobuf ni JSON ga o'tkazish
data_dict = MessageToDict(webhook_data)
json_string = json.dumps(data_dict, indent=2, ensure_ascii=False)
print(json_string)
```

## 📊 Protobuf vs JSON Taqqoslash

### Afzalliklari:
- **Tezlik**: 3-10 marta tezroq serializatsiya/deserializatsiya
- **O'lcham**: 20-50% kichikroq fayl o'lchami
- **Type Safety**: Strict typing, schema validation
- **Backward Compatibility**: Schema o'zgarishlarida eski versiyalar mos keladi

### Misollar:

#### JSON format (taxminan):
```json
{
  "event_type": "user_created",
  "event_id": "evt_123456",
  "timestamp": "2024-12-18T10:00:00Z",
  "user_data": {
    "id": 1001,
    "name": "Alisher Navoi",
    "email": "user1001@example.uz",
    "age": 35,
    "is_active": true,
    "created_at": "2024-12-18T10:00:00Z"
  }
}
```
**O'lchami**: ~180 bytes

#### Protobuf format:
- Binary format, insonlar o'qiy olmaydi
- **O'lchami**: ~90-120 bytes (50% kichikroq)

## 🧪 Test Qilish

### 1. Django Server Tekshirish

```bash
curl http://localhost:8000/api/protobuf-receiver/
```

Javob:
```json
{
  "status": "ready",
  "message": "Protobuf webhook receiver ishlayapti",
  "content_type": "application/x-protobuf"
}
```

### 2. Manual Protobuf Test

```python
# Test script yaratish
from webhook_sender import ProtobufWebhookSender

sender = ProtobufWebhookSender("http://localhost:8000/api/protobuf-receiver/")
test_data = sender.create_webhook_data("user_created")
sender.send_webhook(test_data)
```

### 3. Log Fayllarini Kuzatish

```bash
# Webhook sender loglarini kuzatish
python webhook_sender.py

# Django server loglarini kuzatish
python manage.py runserver 8000
```

## 🔧 Muammolarni Hal Qilish

### 1. "Module not found" xatosi

```bash
# Virtual environment faol ekanini tekshiring
which python
# /home/user/protobuf/venv/bin/python bo'lishi kerak

# Agar yo'q bo'lsa:
source venv/bin/activate
```

### 2. Protobuf compile xatosi

```bash
# grpcio-tools o'rnatilganini tekshiring
pip list | grep grpcio-tools

# Agar yo'q bo'lsa:
pip install grpcio-tools
```

### 3. Django migration xatosi

```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### 4. Port band bo'lsa

```bash
# Boshqa port ishlatish
python manage.py runserver 8001

# webhook_sender.py da URL o'zgartirish
webhook_url = "http://localhost:8001/api/protobuf-receiver/"
```

## 📈 Keyingi Qadamlar

1. **Ma'lumotlar bazasi**: Kelgan ma'lumotlarni PostgreSQL/MySQL ga saqlash
2. **Celery Integration**: Background tasks bilan ishlov berish
3. **Message Queue**: Redis/RabbitMQ bilan asinxron ishlov berish
4. **Monitoring**: Logging va metrics qo'shish
5. **Authentication**: JWT/API key bilan himoyalash

## 📚 Qo'shimcha Resurslar

- [Protocol Buffers Dokumentatsiya](https://developers.google.com/protocol-buffers)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [gRPC Python Tutorial](https://grpc.io/docs/languages/python/)

## 🤝 Yordam

Agar savollaringiz bo'lsa yoki muammolarga duch kelsangiz, quyidagi ishlarni amalga oshiring:

1. Virtual environment faol ekanini tekshiring
2. Barcha dependencies o'rnatilganini tasdiqlang
3. Django server va webhook sender alohida terminallarda ishga tushiring
4. Log fayllarini diqqat bilan o'qing

**Muvaffaqiyatlar!** 🎉