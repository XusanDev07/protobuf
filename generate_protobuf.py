#!/usr/bin/env python3
"""
Protobuf fayllarini Python kodiga o'tkazish uchun script
"""
import os
import subprocess
import sys

def generate_protobuf_files():
    """Proto fayllarini Python kodiga o'tkazadi"""
    
    # Proto fayl yo'li
    proto_dir = "protos"
    output_dir = "apps/core/dtos"
    
    # Output papkasini yaratish
    os.makedirs(output_dir, exist_ok=True)
    
    # __init__.py faylini yaratish
    init_file = os.path.join(output_dir, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write("")
    
    # Proto fayllarini topish
    proto_files = []
    for root, dirs, files in os.walk(proto_dir):
        for file in files:
            if file.endswith('.proto'):
                proto_files.append(os.path.join(root, file))
    
    print(f"Topilgan proto fayllar: {proto_files}")
    
    # Har bir proto faylni compile qilish
    for proto_file in proto_files:
        print(f"Compile qilinmoqda: {proto_file}")
        
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"--python_out={output_dir}",
            f"--grpc_python_out={output_dir}",
            f"--proto_path={proto_dir}",
            proto_file
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✅ Muvaffaqiyatli: {proto_file}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Xato: {proto_file}")
            print(f"Xato matni: {e.stderr}")
            return False
    
    print("🎉 Barcha proto fayllar muvaffaqiyatli compile qilindi!")
    return True

if __name__ == "__main__":
    success = generate_protobuf_files()
    sys.exit(0 if success else 1)