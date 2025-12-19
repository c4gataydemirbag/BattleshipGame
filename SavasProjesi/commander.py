import socket
import sys
import time
from colorama import init, Fore, Style
import utils  


init(autoreset=True)


HOST = '127.0.0.1'
PORT = 12345


def print_banner():
    print(Fore.CYAN + Style.BRIGHT + """
    ========================================
       COMMANDER TERMINAL (HQ) - CLIENT 1
    ========================================
    """)


def generate_packet(message, method_choice):
    """
    Mesajı ve seçilen yöntemi alır, kontrol bilgisini hesaplar
    ve paket oluşturur.
    """
    control_info = ""
    method_name = ""

    # utils.py içindeki fonksiyonları çağırıyoruz
    if method_choice == '1':
        method_name = "PARITY"
        control_info = utils.calculate_parity(message)
    elif method_choice == '2':
        method_name = "2DPARITY"
        control_info = utils.calculate_2d_parity(message)
    elif method_choice == '3':
        method_name = "CRC"
        control_info = utils.calculate_crc(message)
    else:
        return None

    
    packet = f"{message}|{method_name}|{control_info}"
    return packet


def start_commander():
    print_banner()
    print(Fore.WHITE + "Komuta merkezi aktif. Emir bekleniyor...\n")

    while True:
        try:
            # 1. Mesaj Girişi
            print(Fore.WHITE + "-" * 40)
            command = input(Fore.YELLOW + "KOMUT GİRİN (Çıkış için 'exit'): " + Fore.WHITE).strip()

            if command.lower() == 'exit':
                break
            if not command:
                continue

            # 2. Yöntem Seçimi
            print(Fore.CYAN + "\nGüvenlik Protokolü Seçin:")
            print("1. Parity (Zayıf)")
            print("2. 2D Parity (Orta)")
            print("3. CRC-16 (Güçlü)")

            choice = input(Fore.YELLOW + "SEÇİM [1-3]: " + Fore.WHITE)

            # 3. Paket Oluşturma
            packet = generate_packet(command, choice)

            if packet:
                
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    
                    client_socket.connect((HOST, PORT))

                    print(Fore.BLUE + f"\n[>] Paket Hazırlandı: {packet}")
                    client_socket.send(packet.encode('utf-8'))
                    print(Fore.GREEN + "[+] Paket cepheye gönderildi!")

                except ConnectionRefusedError:
                    print(Fore.RED + "[!] HATA: Sunucu (Jammer) aktif değil! Önce jammer.py'yi çalıştırın.")
                finally:
                    
                    client_socket.close()
            else:
                print(Fore.RED + "[!] Geçersiz seçim!")

        except KeyboardInterrupt:
            print("\nÇıkış yapılıyor...")
            break
        except Exception as e:
            print(Fore.RED + f"Bir hata oluştu: {e}")
            break


if __name__ == "__main__":
    start_commander()