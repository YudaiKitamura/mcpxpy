from ctypes import Structure, c_char_p, c_uint8


class Prefix:
    X  = 0x9C  # 入力
    Y  = 0x9D  # 出力
    M  = 0x90  # 内部リレー
    L  = 0x92  # ラッチリレー
    F  = 0x93  # アナンシェータ
    V  = 0x94  # エッジリレー
    B  = 0xA0  # リンクリレー
    D  = 0xA8  # データレジスタ
    W  = 0xB4  # リンクレジスタ
    TS = 0xC1  # タイマ接点
    TC = 0xC0  # タイマコイル
    TN = 0xC2  # タイマ現在値
    SS = 0xC7  # 積算タイマ接点
    SC = 0xC6  # 積算タイマコイル
    SN = 0xC8  # 積算タイマ現在値
    CS = 0xC4  # カウンタ接点
    CC = 0xC3  # カウンタコイル
    CN = 0xC5  # カウンタ現在値
    SB = 0xA1  # リンク特殊リレー
    SW = 0xB5  # リンク特殊レジスタ
    S  = 0x98  # ステップリレー
    DX = 0xA2  # ダイレクトアクセス入力
    DY = 0xA3  # ダイレクトアクセス出力
    SM = 0x91  # 特殊リレー
    SD = 0xA9  # 特殊レジスタ
    Z  = 0xCC  # インデックスレジスタ
    R  = 0xAF  # ファイルレジスタ（ブロック）
    ZR = 0xB0  # ファイルレジスタ（連番）

class RequestFrame:
    E3 = 0
    E4 = 1

class Device(Structure):
    _fields_ = [
        ("Prefix", c_uint8),
        ("Address", c_char_p)
    ]
