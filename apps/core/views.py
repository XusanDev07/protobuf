import json
import logging
import sys
import os
from pathlib import Path
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View

# Add project root to Python path for imports
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from protobuf_decoder import ProtobufDecoder
except ImportError as e:
    # Fallback if protobuf_decoder can't be imported
    print(f"Warning: Could not import protobuf_decoder: {e}")
    ProtobufDecoder = None

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class ProtobufWebhookView(View):
    """
    Protobuf formatdagi webhook ma'lumotlarini qabul qiluvchi view
    """
    
    def __init__(self):
        super().__init__()
        if ProtobufDecoder:
            self.decoder = ProtobufDecoder()
        else:
            self.decoder = None
    
    def post(self, request):
        """
        POST request orqali Protobuf ma'lumotlarini qabul qiladi
        """
        try:
            # Binary datani olish
            binary_data = request.body
            
            if not binary_data:
                logger.error("Bo'sh ma'lumot keldi!")
                return JsonResponse({"error": "Bo'sh ma'lumot"}, status=400)
            
            logger.info(f"📥 Webhook qabul qilindi: {len(binary_data)} bytes")
            
            if not self.decoder:
                # Simple fallback processing
                return JsonResponse({
                    "success": True,
                    "message": "Ma'lumot qabul qilindi (basic processing)",
                    "data_size": len(binary_data)
                })
            
            # Ma'lumotlarni decode qilish
            decoded_data = self.decoder.process_webhook_data(binary_data)
            
            if "error" in decoded_data:
                return JsonResponse({"error": "Decode qila olmadim"}, status=400)
            
            # Muvaffaqiyatli response qaytarish
            response_data = self.decoder.create_response(True, "Muvaffaqiyatli qabul qilindi")
            
            return HttpResponse(
                response_data,
                content_type='application/x-protobuf',
                status=200
            )
            
        except Exception as e:
            logger.error(f"Webhook ishlov berishda xato: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    
    def get(self, request):
        """
        GET request - test uchun
        """
        return JsonResponse({
            "message": "Protobuf Webhook Receiver tayyor!",
            "instructions": "POST request bilan protobuf binary data yuboring"
        })


# Function-based view alternative
@csrf_exempt
@require_http_methods(["GET", "POST"])
def protobuf_webhook_receiver(request):
    """
    Function-based webhook receiver
    """
    if request.method == "GET":
        return JsonResponse({
            "status": "ready",
            "message": "Protobuf webhook receiver ishlayapti",
            "content_type": "application/x-protobuf"
        })
    
    elif request.method == "POST":
        try:
            binary_data = request.body
            
            logger.info(f"📨 Protobuf webhook keldi: {len(binary_data)} bytes")
            
            if ProtobufDecoder:
                decoder = ProtobufDecoder()
                # Decode qilish
                decoded_data = decoder.process_webhook_data(binary_data)
                event_type = decoded_data.get("eventType", "unknown")
            else:
                # Simple processing without decoder
                decoded_data = {"message": "Basic processing completed"}
                event_type = "unknown"
            
            # Simple JSON response qaytarish
            return JsonResponse({
                "success": True,
                "message": "Ma'lumot muvaffaqiyatli ishlov berildi",
                "data_size": len(binary_data),
                "event_type": event_type
            })
            
        except Exception as e:
            logger.error(f"Xato: {e}")
            return JsonResponse({"error": str(e)}, status=500)
