import base64

# Nama file yang ingin di-encode
input_file_path = 'C:\Users\Asus\SMT 6\progjar\progjar4a\grandwarden.jpg'  # Ganti dengan path file Anda
output_file_path = 'C:\Users\Asus\SMT 6\progjar\progjar4a\grandwardenb64.jpg'  # Ganti dengan path output yang diinginkan

# Membaca file dalam mode biner
with open(input_file_path, 'rb') as file:
    # Membaca isi file
    file_content = file.read()
    
    # Melakukan encoding ke base64
    encoded_content = base64.b64encode(file_content)

# Jika ingin menyimpan hasil encoding ke file lain
with open(output_file_path, 'wb') as output_file:
    output_file.write(encoded_content)

print(f"File '{input_file_path}' telah di-encode ke base64 dan disimpan sebagai '{output_file_path}'.")

