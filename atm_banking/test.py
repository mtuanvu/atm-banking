import secrets
secret_key = secrets.token_hex(32)  # Tạo ra một chuỗi bí mật ngẫu nhiên 64 ký tự (32 bytes)
print(secret_key)