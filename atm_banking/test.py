from werkzeug.security import generate_password_hash, check_password_hash

# Đặt mật khẩu thực tế
actual_password = "12345"  # Mật khẩu thực tế mà bạn muốn kiểm tra

# Mã hóa mật khẩu
hashed_password = generate_password_hash(actual_password)

# Kiểm tra xem mật khẩu đã mã hóa có khớp với mật khẩu thực tế không
password_to_check = "scrypt:32768:8:1$PCRfK8guyZlSYnAY$e009a3df85a79d5316f3d057571196380beed087276e699e39eee4cd8b3a35eaba"  # Thay thế bằng mật khẩu bạn muốn kiểm tra
is_valid = check_password_hash(hashed_password, password_to_check)

print(f"Hashed Password: {hashed_password}")
print(f"Password Valid: {is_valid}")
