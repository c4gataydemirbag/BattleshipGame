import socket
import random
import time
from colorama import init, Fore, Style
import utils

init(autoreset=True)

# AYARLAR
LISTEN_HOST = '127.0.0.1'
LISTEN_PORT = 12345  # Komutanı buradan dinler
TARGET_HOST = '127.0.0.1'
TARGET_PORT = 12346  # Topçuya (Client 2) buradan yollar


def print_banner():
    print(Fore.RED + Style.BRIGHT + """
    ########################################
       ENEMY JAMMER TERMINAL (INTERCEPTOR)
    ########################################
    """)


# --- HATA ENJEKSİYON YÖNTEMLERİ ---

def inject_bit_flip(text):
    """
     Rastgele bir bitin değerini tersine çevirir.
    """
    if not text: return text

    # 1. Metni binary'e çevir
    binary_list = list(utils.text_to_binary(text))

    # 2. Rastgele bir biti seç ve tersine çevir
    idx = random.randint(0, len(binary_list) - 1)
    original_bit = binary_list[idx]
    binary_list[idx] = '0' if original_bit == '1' else '1'

    print(Fore.YELLOW + f"   -> Bit {idx} değiştirildi: {original_bit} > {binary_list[idx]}")

    # 3. Tekrar metne çevir
    corrupted_binary = "".join(binary_list)
    return utils.binary_to_text(corrupted_binary)


def inject_burst_error(text):
    """
     Belli bir aralıktaki karakterleri bozar.
    """
    if len(text) < 3: return text  # Çok kısaysa dokunma

    # Metni listeye çevir (değiştirebilmek için)
    chars = list(text)
    start = random.randint(0, len(chars) - 2)
    length = random.randint(2, 4)  # 2-4 karakterlik hasar

    for i in range(start, min(start + length, len(chars))):
        chars[i] = random.choice(['#', '?', '!', 'X'])

    print(Fore.YELLOW + f"   -> {start}. karakterden itibaren {length} karakter bozuldu.")
    return "".join(chars)


def process_packet(packet):
    """Gelen paketi parçalar, kullanıcıya sorar ve bozar."""
    try:
        data, method, crc = packet.split('|')
    except ValueError:
        return packet  # Format bozuksa dokunma

    print(Fore.CYAN + f"\n[YAKALANAN MESAJ]: {data}")
    print(Fore.CYAN + f"[KORUMA YÖNTEMİ]: {method}")
    print(Fore.CYAN + f"[KONTROL KODU]: {crc}")

    print(Fore.RED + "\n--- SABOTAJ MENÜSÜ ---")
    print("1. Sızma Yok (Olduğu gibi ilet)")
    print("2. Bit Flip (Tek Bit Hatası) ")
    print("3. Burst Error (Sinyal Kesici) ")

    choice = input(Fore.RED + "SEÇİMİNİZ [1-3]: ")

    corrupted_data = data
    if choice == '2':
        corrupted_data = inject_bit_flip(data)
    elif choice == '3':
        corrupted_data = inject_burst_error(data)
    else:
        print(Fore.GREEN + "-> Müdahale edilmedi.")

    # Paketi yeniden birleştir 
    # Hata tespiti 
    return f"{corrupted_data}|{method}|{crc}"


def start_jammer():
    print_banner()

    # Sunucu soketi (Komutanı dinlemek için)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((LISTEN_HOST, LISTEN_PORT))
    server_socket.listen(1)

    print(Fore.WHITE + f"[*] Ağ dinleniyor... Port: {LISTEN_PORT}")

    while True:
        conn, addr = server_socket.accept()
        print(Fore.YELLOW + f"\n[!] Sinyal Yakalandı: {addr}")

        try:
            packet = conn.recv(1024).decode('utf-8')
            if not packet: continue

            # Veriyi bozma işlemi
            final_packet = process_packet(packet)

            # Topçuya (Client 2) iletme işlemi
            print(Fore.BLUE + "\n[>] Hedefe (Topçu Birliği) yönlendiriliyor...")
            try:
                # Topçuya anlık bağlanıp veriyi atıp çıkacağız
                target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                target_socket.connect((TARGET_HOST, TARGET_PORT))
                target_socket.send(final_packet.encode('utf-8'))
                target_socket.close()
                print(Fore.GREEN + "[+] İletim Başarılı.")
            except ConnectionRefusedError:
                print(Fore.RED + "[X] HATA: Topçu Birliği (Client 2) hatta yok! Paket kayboldu.")

        except Exception as e:
            print(Fore.RED + f"Hata: {e}")

        conn.close()


if __name__ == "__main__":
    start_jammer()