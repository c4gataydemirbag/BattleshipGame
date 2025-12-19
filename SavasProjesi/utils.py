import binascii


# --- TEMEL DÖNÜŞÜMLER ---
def text_to_binary(text):
    """Metni binary string'e çevirir (Örn: 'A' -> '01000001')"""
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary_string):
    """Binary string'i tekrar metne çevirir"""
    text = ""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i + 8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text


# --- YÖNTEM 1: PARITY BIT ---
def calculate_parity(text, mode='even'):
    """
    Basit parity hesabı.
    Dönüş: '1' veya '0'
    """
    binary_data = text_to_binary(text)
    ones_count = binary_data.count('1')
    if mode == 'even':
        return '0' if ones_count % 2 == 0 else '1'
    else:
        return '0' if ones_count % 2 != 0 else '1'


# --- YÖNTEM 2: 2D PARITY (MATRIX PARITY) ---
def calculate_2d_parity(text):
    """
    Metni satır ve sütunlara ayırarak 2D parity hesaplar.
    Her karakteri bir satır (8 bit) olarak kabul ediyoruz.
    """
    binary_rows = [format(ord(c), '08b') for c in text]

    # 1. Satır Parityleri (Her karakterin kendi parity'si)
    row_parities = ""
    for row in binary_rows:
        count = row.count('1')
        row_parities += '0' if count % 2 == 0 else '1'

    # 2. Sütun Parityleri (Sütunların dikey taranması)
    col_parities = ""
    if binary_rows:
        num_cols = len(binary_rows[0])  # 8 bit
        for col_idx in range(num_cols):
            col_bits = [row[col_idx] for row in binary_rows]
            count = col_bits.count('1')
            col_parities += '0' if count % 2 == 0 else '1'

    # Sonuç: Satır parityleri + Sütun parityleri birleşimi
    return row_parities + col_parities


# --- YÖNTEM 3: CRC (Cyclic Redundancy Check) ---
def calculate_crc(text):
    """
    Manuel CRC-16 hesaplaması.
    Polinom: 0x8005 (CRC-16-IBM)
    """
    data = text.encode('utf-8')
    crc = 0x0000
    polynomial = 0x8005

    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if (crc & 0x8000):
                crc = (crc << 1) ^ polynomial
            else:
                crc = crc << 1
            crc &= 0xFFFF  # 16 bitte tutmak için

    # Sonucu hex formatında döndür (Örn: 'A1B2')
    return format(crc, '04X')


# --- TEST ALANI ---
if __name__ == "__main__":
    msg = "HELLO"
    print(f"--- TEST: {msg} ---")

    # 1. Parity
    p = calculate_parity(msg)
    print(f"[1] Parity Bit: {p}")

    # 2. 2D Parity
    p2d = calculate_2d_parity(msg)
    print(f"[2] 2D Parity: {p2d}")
    # Açıklama: HELLO 5 harf -> 5 satır parity + 8 sütun parity = 13 bit dönmeli

    # 3. CRC
    crc_val = calculate_crc(msg)
    print(f"[3] CRC-16 Hex: {crc_val}")