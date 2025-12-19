import socket
import time
from colorama import init, Fore, Style
import utils

init(autoreset=True)


HOST = '127.0.0.1'
PORT = 12346  


def print_banner():
    print(Fore.GREEN + Style.BRIGHT + """
    ========================================
       ARTILLERY UNIT (RECEIVER) - CLIENT 2
    ========================================
    """)


def check_integrity(data, method, received_control):
    
    calculated_control = ""

    print(Fore.CYAN + f"\n[ANALİZ BAŞLIYOR] Yöntem: {method}")
    print(f"Gelen Veri: {data}")
    print(f"Gelen Kontrol Kodu: {received_control}")

    # Yeniden Hesaplama
    if method == "PARITY":
        calculated_control = utils.calculate_parity(data)
    elif method == "2DPARITY":
        calculated_control = utils.calculate_2d_parity(data)
    elif method == "CRC":
        calculated_control = utils.calculate_crc(data)
    else:
        print(Fore.RED + "Bilinmeyen Yöntem!")
        return False

    print(Fore.YELLOW + f"Hesaplanan Kod    : {calculated_control}")

    # Karşılaştırma
    if calculated_control == received_control:
        return True
    else:
        return False


def start_artillery():
    print_banner()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(Fore.WHITE + f"[*] Atış koordinatları bekleniyor... Port: {PORT}")

    while True:
        conn, addr = server_socket.accept()

        try:
            packet = conn.recv(1024).decode('utf-8')
            if not packet: continue

            # Paketi Parçala
            parts = packet.split('|')
            if len(parts) < 3:
                print(Fore.RED + "Hatalı Paket Formatı!")
                conn.close()
                continue

            data = parts[0]
            method = parts[1]
            received_control = parts[2]

            # Doğrulama Yap
            is_valid = check_integrity(data, method, received_control)

            print("-" * 40)
            if is_valid:
                print(Fore.GREEN + Style.BRIGHT + """
      _.-^^---....,,--
  _--                  --_
 <      HEDEF VURULDU!    >)
  \._                   _./
     ```--. . , ; .--'''
           | |   |
        .-=||  | |=-.
        `-=#$%&%$#=-'
                """)
                print(Fore.GREEN + f"DURUM: VERİ SAĞLAM. EMİR UYGULANIYOR: {data}")
            else:
                print(Fore.RED + Style.BRIGHT + """
        XXXXXXXXXXXXX
      XX  SİNYAL   XX
    XX   BOZUK!    XX
      XX  İPTAL    XX
        XXXXXXXXXXXXX
                """)
                print(Fore.RED + f"DURUM: VERİ BOZULMUŞ! (Gelen: {received_control} != Hesaplanan)")
            print("-" * 40)

        except Exception as e:
            print(Fore.RED + f"Hata: {e}")

        conn.close()


if __name__ == "__main__":
    start_artillery()