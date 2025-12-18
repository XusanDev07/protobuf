#!/usr/bin/env python3
"""
Protobuf loyihasini test qilish uchun script
"""

import sys
import os
import subprocess
import time
import requests
from pathlib import Path

# Django loyihasini Python path ga qo'shish
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_protobuf_generation():
    """Protobuf fayllar generate qilinganini tekshiradi"""
    print("🔍 Protobuf fayllari tekshirilmoqda...")
    
    generated_files = [
        "apps/core/dtos/platform/v1/data_exchange_pb2.py",
        "apps/core/dtos/platform/v1/data_exchange_pb2_grpc.py",
    ]
    
    for file_path in generated_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - mavjud")
        else:
            print(f"❌ {file_path} - mavjud emas")
            return False
    
    return True

def test_protobuf_import():
    """Protobuf modullarini import qilishni tekshiradi"""
    print("🔍 Protobuf import tekshirilmoqda...")
    
    try:
        from apps.core.dtos.platform.v1.data_exchange_pb2 import WebhookData, User, Product, Order
        print("✅ Protobuf modullari muvaffaqiyatli import qilindi")
        return True
    except ImportError as e:
        print(f"❌ Import xatosi: {e}")
        return False

def test_protobuf_creation():
    """Protobuf obyektlari yaratishni tekshiradi"""
    print("🔍 Protobuf obyektlari yaratilmoqda...")
    
    try:
        from apps.core.dtos.platform.v1.data_exchange_pb2 import WebhookData, User
        from google.protobuf.timestamp_pb2 import Timestamp
        
        # User yaratish
        user = User()
        user.id = 123
        user.name = "Test User"
        user.email = "test@example.com"
        user.age = 25
        user.is_active = True
        user.created_at.GetCurrentTime()
        
        # WebhookData yaratish
        webhook_data = WebhookData()
        webhook_data.event_type = "user_created"
        webhook_data.event_id = "test_123"
        webhook_data.timestamp.GetCurrentTime()
        webhook_data.user_data.CopyFrom(user)
        
        # Serializatsiya test
        binary_data = webhook_data.SerializeToString()
        print(f"✅ Binary data yaratildi: {len(binary_data)} bytes")
        
        # Deserializatsiya test
        new_webhook = WebhookData()
        new_webhook.ParseFromString(binary_data)
        print(f"✅ Deserializatsiya muvaffaqiyatli: {new_webhook.user_data.name}")
        
        return True
    except Exception as e:
        print(f"❌ Protobuf obyekt xatosi: {e}")
        return False

def test_django_server():
    """Django server ishlab turganini tekshiradi"""
    print("🔍 Django server tekshirilmoqda...")
    
    try:
        response = requests.get("http://localhost:8000/api/protobuf-receiver/", timeout=5)
        if response.status_code == 200:
            print("✅ Django server ishlayapti")
            print(f"📄 Response: {response.json()}")
            return True
        else:
            print(f"❌ Django server xatosi: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Django server ulanish xatosi: {e}")
        print("💡 Django serverni ishga tushiring: python manage.py runserver 8000")
        return False

def test_webhook_send():
    """Webhook yuborishni tekshiradi"""
    print("🔍 Webhook yuborish tekshirilmoqda...")
    
    try:
        from webhook_sender import ProtobufWebhookSender
        
        sender = ProtobufWebhookSender("http://localhost:8000/api/protobuf-receiver/")
        test_data = sender.create_webhook_data("user_created")
        success = sender.send_webhook(test_data)
        
        if success:
            print("✅ Webhook muvaffaqiyatli yuborildi")
            return True
        else:
            print("❌ Webhook yuborishda xato")
            return False
            
    except Exception as e:
        print(f"❌ Webhook xatosi: {e}")
        return False

def run_full_test():
    """To'liq test dasturi"""
    print("🚀 Protobuf loyihasi test boshlandi\n")
    
    tests = [
        ("Protobuf generation", test_protobuf_generation),
        ("Protobuf import", test_protobuf_import),
        ("Protobuf creation", test_protobuf_creation),
        ("Django server", test_django_server),
        ("Webhook sending", test_webhook_send),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        print("-" * 40)
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test natijalari: {passed}/{total} muvaffaqiyatli")
    
    if passed == total:
        print("🎉 Barcha testlar muvaffaqiyat!")
        print("\n🚀 Endi webhook_sender.py ni ishga tushirishingiz mumkin:")
        print("   python webhook_sender.py")
    else:
        print("❌ Ba'zi testlar muvaffaqiyatsiz")
        print("\n🔧 Quyidagilarni tekshiring:")
        print("   1. Virtual environment faol ekanini")
        print("   2. pip install -r requirements.txt bajarilganini")
        print("   3. python generate_protobuf.py bajarilganini")
        print("   4. python manage.py runserver 8000 ishlab turganini")

def quick_demo():
    """Tezkor demo"""
    print("🎯 Tezkor Protobuf Demo")
    print("=" * 30)
    
    try:
        from apps.core.dtos.platform.v1.data_exchange_pb2 import WebhookData, User
        from google.protobuf.json_format import MessageToDict
        import json
        
        # Sample data yaratish
        user = User()
        user.id = 12345
        user.name = "Alisher Navoiy"
        user.email = "alisher@example.uz"
        user.age = 35
        user.is_active = True
        user.created_at.GetCurrentTime()
        
        webhook_data = WebhookData()
        webhook_data.event_type = "user_created"
        webhook_data.event_id = "demo_001"
        webhook_data.timestamp.GetCurrentTime()
        webhook_data.user_data.CopyFrom(user)
        
        # JSON formatda ko'rsatish
        data_dict = MessageToDict(webhook_data)
        json_str = json.dumps(data_dict, indent=2, ensure_ascii=False)
        print("📄 JSON format:")
        print(json_str)
        
        # Binary format
        binary_data = webhook_data.SerializeToString()
        print(f"\n💾 Binary format: {len(binary_data)} bytes")
        print(f"🔢 Binary data (hex): {binary_data.hex()[:100]}...")
        
        print("\n✅ Demo tugadi!")
        
    except Exception as e:
        print(f"❌ Demo xatosi: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        quick_demo()
    else:
        run_full_test()