# scripts/app/pages/6_Profil.py
import io
import base64
from pathlib import Path
from PIL import Image, ExifTags
import streamlit as st
from app.utils.ui_style import apply_greentech_style

st.set_page_config(page_title="👥 Profils", layout="wide")
apply_greentech_style()

# --- Correction EXIF images ---
def fix_exif_orientation(img: Image.Image) -> Image.Image:
    try:
        exif = img._getexif()
        if not exif:
            return img
        orientation_key = next((k for k, v in ExifTags.TAGS.items() if v == "Orientation"), None)
        val = exif.get(orientation_key)
        if val == 3:
            img = img.rotate(180, expand=True)
        elif val == 6:
            img = img.rotate(270, expand=True)
        elif val == 8:
            img = img.rotate(90, expand=True)
    except Exception:
        pass
    return img

def load_local_img(path: Path):
    try:
        img = Image.open(path)
        return fix_exif_orientation(img).convert("RGBA")
    except Exception:
        return None

def to_b64(img: Image.Image | None):
    if img is None:
        return None
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

# --- Données ---
ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
TEAM = [
    {"fullname": "Mohamed Habib", "role": "Data Scientist", "linkedin": "https://www.linkedin.com/in/mohamed-bah-270b6a1a9/", "photo_file": "pp.jpg"},
    {"fullname": "Yassine Cheniour", "role": "Data Scientist", "linkedin": "https://www.linkedin.com/in/yassine-cheniour-01yc/", "photo_file": "ya.jpeg"},
    {"fullname": "Perrine Ibouroi", "role": "Data Scientist", "linkedin": "https://www.linkedin.com/in/perrine-i/", "photo_file": "pe.JPG"},
]

# --- Affichage ---
st.markdown("<h2 style='color:#097536; font-weight:700;'>👥 Notre équipe</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#14532d; opacity:0.85;'><em>Trois profils complémentaires unis autour du même objectif : excellence, innovation et collaboration.</em></p>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid rgba(9,117,54,0.2);'>", unsafe_allow_html=True)

cols = st.columns(len(TEAM), gap="large")
for i, member in enumerate(TEAM):
    img = load_local_img(ASSETS_DIR / member["photo_file"])
    img_b64 = to_b64(img)
    with cols[i]:
        st.markdown(f"""
        <div style="text-align:center;background-color:white;padding:25px;border-radius:20px;
        box-shadow:0 8px 24px rgba(9,117,54,0.1);transition:all .2s ease-in-out;">
            <img src="data:image/png;base64,{img_b64}" style="width:160px;height:160px;object-fit:cover;
            border-radius:18px;border:3px solid #097536;margin-bottom:10px;"/>
            <h3 style="color:#065f46;margin-bottom:4px;">{member['fullname']}</h3>
            <p style="color:#166534;margin-bottom:14px;">{member['role']}</p>
            <a href="{member['linkedin']}" target="_blank"
            style="background-color:#097536;color:white;padding:8px 16px;
            border-radius:10px;text-decoration:none;font-weight:600;">LinkedIn</a>
        </div>
        """, unsafe_allow_html=True)
