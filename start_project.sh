#!/bin/bash

# Protobuf loyihasini ishga tushirish scripti

echo "🚀 Protobuf loyihasi ishga tushirilmoqda..."

# Virtual environment faollashtirish
echo "📁 Virtual environment faollashtirilmoqda..."
source venv/bin/activate

# Bog'liqliklarni tekshirish
echo "📦 Bog'liqliklar tekshirilmoqda..."
pip install -r requirements.txt

# Protobuf fayllarni generate qilish
echo "⚙️ Protobuf fayllari generate qilinmoqda..."
python generate_protobuf.py

# Django migratsiyalar
echo "🗄️ Django ma'lumotlar bazasi sozlanmoqda..."
python manage.py migrate

# Test qilish
echo "🧪 Tezkor test..."
python test_protobuf.py demo

echo ""
echo "✅ Tayyor! Endi quyidagi buyruqlarni alohida terminallarda ishga tushiring:"
echo ""
echo "1️⃣ Django server (webhook receiver):"
echo "   source venv/bin/activate && python manage.py runserver 8000"
echo ""
echo "2️⃣ Webhook sender (localhost:8002 ga yuborish uchun):"
echo "   source venv/bin/activate && python webhook_sender_8002.py"
echo ""
echo "3️⃣ Yoki Django receiver ga yuborish uchun:"
echo "   source venv/bin/activate && python webhook_sender.py"
echo ""