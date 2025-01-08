import os
import yaml

# Fungsi untuk membaca daftar subdomain dari file
def read_subdomain_list(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    return []

# Fungsi untuk menyimpan subdomain yang digunakan ke file YAML
def save_subdomain_to_yaml(subdomain, yaml_file):
    with open(yaml_file, 'w') as file:
        yaml.dump({'subdomain': subdomain}, file)

# Fungsi untuk membaca subdomain terakhir dari file YAML
def read_subdomain_from_yaml(yaml_file):
    if os.path.exists(yaml_file):
        with open(yaml_file, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            return data.get('subdomain', None)
    return None

# Fungsi untuk mengganti subdomain di _worker.js
def replace_subdomain_in_js(js_file, new_subdomain):
    with open(js_file, 'r') as file:
        content = file.read()

    updated_content = content.replace('tp2.bmkg.xyz', f'{new_subdomain}.bmkg.xyz')

    with open(js_file, 'w') as file:
        file.write(updated_content)

def main():
    yaml_file = 'subdomain.yml'
    js_file = '_worker.js'  # Ganti dengan _worker.js
    list_file = 'subdomain_list.txt'  # Pastikan file daftar subdomain ada

    # Baca daftar subdomain dari file
    subdomain_list = read_subdomain_list(list_file)
    if not subdomain_list:
        print("Subdomain list is empty or not found!")
        return

    # Baca subdomain terakhir dari YAML
    last_subdomain = read_subdomain_from_yaml(yaml_file)

    # Cari subdomain berikutnya berdasarkan urutan di daftar
    if last_subdomain and last_subdomain in subdomain_list:
        current_index = subdomain_list.index(last_subdomain)
        next_index = (current_index + 1) % len(subdomain_list)
    else:
        next_index = 0  # Jika belum ada subdomain terakhir, mulai dari yang pertama

    next_subdomain = subdomain_list[next_index]

    # Ganti subdomain di _worker.js
    replace_subdomain_in_js(js_file, next_subdomain)

    # Simpan subdomain yang digunakan ke file YAML
    save_subdomain_to_yaml(next_subdomain, yaml_file)
    print(f"Subdomain updated to: {next_subdomain}")

if __name__ == "__main__":
    main()
