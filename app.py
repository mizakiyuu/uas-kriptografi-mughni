import streamlit as st
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import qrcode
import json
import cv2
import numpy as np

# =================================================
# RSA KEY (TIDAK RESET)
# =================================================
def npm_20221310123_load_or_generate_key():
    try:
        with open("private.pem", "rb") as f:
            priv = f.read()
        with open("public.pem", "rb") as f:
            pub = f.read()
    except:
        key = RSA.generate(2048)
        priv = key.export_key()
        pub = key.publickey().export_key()
        with open("private.pem", "wb") as f:
            f.write(priv)
        with open("public.pem", "wb") as f:
            f.write(pub)
    return priv, pub

# =================================================
# FUNGSI KRIPTOGRAFI
# =================================================
def npm_20221310123_hash_pesan(pesan):
    return SHA256.new(pesan.encode())

def npm_20221310123_tanda_tangan(private_key, hash_obj):
    return pkcs1_15.new(RSA.import_key(private_key)).sign(hash_obj)

def npm_20221310123_encode_base64(data):
    return base64.b64encode(data).decode()

def npm_20221310123_verifikasi(public_key, pesan, signature_b64):
    hash_obj = SHA256.new(pesan.encode())
    pkcs1_15.new(RSA.import_key(public_key)).verify(
        hash_obj,
        base64.b64decode(signature_b64)
    )

# =================================================
# QR (ISI PESAN + SIGNATURE)
# =================================================
def npm_20221310123_buat_qr(pesan, signature_b64):
    data = {"pesan": pesan, "signature": signature_b64}
    img = qrcode.make(json.dumps(data))
    img.save("signature_qr.png")

def npm_20221310123_baca_qr(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    if data:
        return json.loads(data)
    return None

# =================================================
# KONFIGURASI HALAMAN
# =================================================
st.set_page_config(page_title="Verifikasi Dokumen Digital", layout="wide")

# =================================================
# STYLE UI (ASLI)
# =================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Inter:wght@300;400;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
body { background: radial-gradient(circle at top, #7b2cff, #12002b); }
.hero {
    background: linear-gradient(180deg, rgba(123,44,255,0.9), rgba(18,0,43,0.95));
    padding: 60px;
    border-radius: 35px;
    color: white;
    text-align: center;
    box-shadow: 0 0 50px rgba(160,100,255,0.45);
    margin-bottom: 40px;
}
.hero h1 { font-family: 'Fredoka', cursive; font-size: 3rem; }
.card {
    background: rgba(22, 8, 52, 0.95);
    padding: 25px;
    border-radius: 25px;
    box-shadow: 0 0 30px rgba(123,44,255,0.35);
    margin-bottom: 25px;
    color: white;
}
.stat {
    background: rgba(22, 8, 52, 0.95);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 0 25px rgba(123,44,255,0.35);
    color: white;
}
textarea, input {
    background-color: #12002b !important;
    color: white !important;
    border-radius: 15px !important;
}
button {
    border-radius: 999px !important;
    background: linear-gradient(135deg, #ff4fd8, #7b2cff) !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 0.6rem 1.6rem !important;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# HERO
# =================================================
st.markdown("""
<div class="hero">
<h1>🔐 Verifikasi Dokumen Digital</h1>
<p>Sistem tanda tangan digital menggunakan <b>RSA</b>, <b>SHA-256</b>, dan <b>QR Code</b></p>
</div>
""", unsafe_allow_html=True)

# =================================================
# STATISTIK (BALIK – UI ASLI)
# =================================================
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="stat"><h2>2048</h2><p>Kunci RSA</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="stat"><h2>SHA-256</h2><p>Hash</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="stat"><h2>QR</h2><p>Signature</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="stat"><h2>VALID</h2><p>Verifikasi</p></div>', unsafe_allow_html=True)

# =================================================
# LOAD KEY
# =================================================
if "private_key" not in st.session_state:
    priv, pub = npm_20221310123_load_or_generate_key()
    st.session_state.private_key = priv
    st.session_state.public_key = pub

tab1, tab2 = st.tabs(["📤 Pengirim Pesan", "📥 Penerima Pesan"])

# =================================================
# TAB PENGIRIM (ASLI)
# =================================================
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    pesan = st.text_area("✉️ Pesan Asli")

    if st.button("Proses Digital Signature"):
        hash_obj = npm_20221310123_hash_pesan(pesan)
        signature = npm_20221310123_tanda_tangan(
            st.session_state.private_key, hash_obj
        )
        signature_b64 = npm_20221310123_encode_base64(signature)
        npm_20221310123_buat_qr(pesan, signature_b64)

        st.success("Signature berhasil dibuat")
        st.image("signature_qr.png", width=220)
        st.text_area("Digital Signature (Base64)", signature_b64, height=120)
    st.markdown('</div>', unsafe_allow_html=True)

# =================================================
# TAB PENERIMA
# (TEXTAREA KOSONG DI ATAS SUDAH DIHAPUS)
# =================================================
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    uploaded_qr = st.file_uploader(
        "📷 Upload Gambar QR Code Digital Signature",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_qr and st.button("Verifikasi"):
        hasil = npm_20221310123_baca_qr(uploaded_qr)

        if hasil:
            pesan_terima = hasil["pesan"]
            signature_terima = hasil["signature"]

            st.text_area("✉️ Pesan yang Diterima", pesan_terima)
            st.text_area("Digital Signature (Base64)", signature_terima, height=120)

            try:
                npm_20221310123_verifikasi(
                    st.session_state.public_key,
                    pesan_terima,
                    signature_terima
                )
                st.success("✅ Signature VALID — Pesan Asli & Tidak Diubah")
            except:
                st.error("❌ Signature TIDAK VALID")
        else:
            st.error("QR Code tidak valid")

    st.markdown('</div>', unsafe_allow_html=True)