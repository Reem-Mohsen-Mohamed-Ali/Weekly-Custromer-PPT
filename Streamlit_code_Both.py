# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 00:44:04 2025

@author: mreem
"""

import streamlit as st
import tempfile
import os
import base64
import Main_Code_Task
import Delta_code_5G  # backend file

# ---- Page Config ----
st.set_page_config(page_title="Network KPI PowerPoint Updater", page_icon="📊", layout="centered")

# ---- Background Image ----
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            background-attachment: fixed;
        }}
        h1 {{
            text-align: center;
            font-weight: 900;
            color: white;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
        }}
        .subtitle {{
            text-align: center;
            font-size: 1.2rem;
            color: black;
            margin-bottom: 1rem;
        }}
        div.stButton > button:first-child {{
            background-color: #005bb5;
            color: white;
            font-size: 18px;
            border-radius: 12px;
            height: 3rem;
            width: 80%;
            margin-top: 1.5rem;
            border: none;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }}
        div.stButton > button:first-child:hover {{
            background-color: #0073e6;
            transform: scale(1.03);
        }}
        .upload-info {{
            color: #fff;
            font-weight: bold;
            font-size: 1.1rem;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
            background: rgba(0, 0, 0, 0.35);
            padding: 0.7rem 1rem;
            border-radius: 8px;
            display: inline-block;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

add_bg_from_local("Snap6.png")

# ---- Header ----
st.markdown(
    '<h1>📊 Network KPI Weekly Slides Generator</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="subtitle">Select your report type (<b>UE & SI</b> or <b>DE</b>), upload the required Excel and PowerPoint files,<br>then click <b>Run Processing</b> to automatically update your PowerPoint report.</p>',
    unsafe_allow_html=True
)

# ---- Centered Radio Buttons ----
st.markdown('<div style="text-align:center;"><b>Select Report Type:</b></div>', unsafe_allow_html=True)
colr1, colr2, colr3 = st.columns([1, 2, 1])
with colr2:
    report_type = st.radio("", ["UE & SI", "DE"], horizontal=True, label_visibility="collapsed")

# ============================================================
# ---- UE & SI SECTION ----
# ============================================================
if report_type == "UE & SI":
    st.header("📁 UE & SI Input Files")
    excel_file = st.file_uploader("📈 Upload Excel file (.xlsx)", type=["xlsx"])
    ppt_file = st.file_uploader("📊 Upload PowerPoint file (.pptx)", type=["pptx"])

    if not (excel_file and ppt_file):
        st.markdown('<p class="upload-info">⚠️ Please upload both an Excel file and a PowerPoint file to continue.</p>', unsafe_allow_html=True)
    else:
        temp_dir = tempfile.mkdtemp()
        excel_path = os.path.join(temp_dir, excel_file.name)
        pptx_path = os.path.join(temp_dir, ppt_file.name)
        with open(excel_path, "wb") as f: f.write(excel_file.read())
        with open(pptx_path, "wb") as f: f.write(ppt_file.read())

        if st.button("🚀 Run Processing"):
            with st.spinner("Processing UE & SI Report — please wait..."):
                try:
                    Main_Code_Task.main_with_paths(excel_path, pptx_path)
                    if hasattr(Main_Code_Task, 'main'):
                        Main_Code_Task.main()
                    st.success("🎉 UE & SI PowerPoint updated successfully!")
                    with open(pptx_path, "rb") as f:
                        st.download_button("⬇️ Download Updated PowerPoint", f, file_name="Updated_UE_SI_Report.pptx")
                except Exception as e:
                    st.error(f"❌ Processing failed: {e}")
                    st.exception(e)

# ============================================================
# ---- DE SECTION (4 inputs + side-by-side layout) ----
# ============================================================
else:
    st.header("📁 DE Input Files")

    # --- Two uploaders side by side ---
    col1, col2 = st.columns(2)
    with col1:
        excel_file_delta = st.file_uploader("📶 2G/3G/4G Delta Excel (.xlsx)", type=["xlsx"], key="delta")
    with col2:
        excel_file_portsaid = st.file_uploader("🏗️ 2G/3G/4G PortSaid Excel (.xlsx)", type=["xlsx"], key="portsaid")

    # --- Below that: 5G + PPT ---
    excel_file_5G = st.file_uploader("📡 Upload 5G Excel (.xlsx)", type=["xlsx"], key="5g")
    ppt_file = st.file_uploader("📊 Upload PowerPoint file (.pptx)", type=["pptx"], key="ppt")

    if not (excel_file_delta and excel_file_portsaid and excel_file_5G and ppt_file):
        st.markdown('<p class="upload-info">⚠️ Please upload all 4 files (Delta, PortSaid, 5G, PPT) to continue.</p>', unsafe_allow_html=True)
    else:
        temp_dir = tempfile.mkdtemp()
        delta_path = os.path.join(temp_dir, excel_file_delta.name)
        portsaid_path = os.path.join(temp_dir, excel_file_portsaid.name)
        fiveg_path = os.path.join(temp_dir, excel_file_5G.name)
        pptx_path = os.path.join(temp_dir, ppt_file.name)

        for file_obj, path in [
            (excel_file_delta, delta_path),
            (excel_file_portsaid, portsaid_path),
            (excel_file_5G, fiveg_path),
            (ppt_file, pptx_path),
        ]:
            with open(path, "wb") as f: f.write(file_obj.read())

        if st.button("🚀 Run Processing"):
            with st.spinner("Processing DE Report — please wait..."):
                try:
                    if hasattr(Delta_code_5G, 'main_with_paths_DE'):
                        Delta_code_5G.main_with_paths_DE(delta_path, portsaid_path, fiveg_path, pptx_path)
                    elif hasattr(Delta_code_5G, 'main_with_paths'):
                        Delta_code_5G.main_with_paths(delta_path, fiveg_path, pptx_path)
                    if hasattr(Delta_code_5G, 'main'):
                        Delta_code_5G.main()
                    st.success("🎉 DE PowerPoint updated successfully!")
                    with open(pptx_path, "rb") as f:
                        st.download_button("⬇️ Download Updated PowerPoint", f, file_name="Updated_DE_Report.pptx")
                except Exception as e:
                    st.error(f"❌ Processing failed: {e}")
                    st.exception(e)
