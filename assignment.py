import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objects as go 
from datetime import datetime, timedelta


#konfigurasi halaman
st.set_page_config(
    page_title = "Dashboard Analisis Penjualan",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("Data/employee_survey.csv")

df = load_data()
df.columns = df.columns.str.lower().str.replace(' ', '_')

#Judul Dashboard
st.title("People Analytics Dashboard")
st.markdown(
    "Dashboard ini dirancang untuk membantu HR & manajemen memahami profil karyawan, "
    "faktor yang memengaruhi kepuasan kerja, serta area prioritas intervensi."
)

# ================== SIDEBAR FILTER GLOBAL ==================
st.sidebar.header("Filter Data")

# opsi filter (sesuai kolom: dept, joblevel)
dept_opt = sorted(df["dept"].dropna().unique()) if "dept" in df.columns else []
job_opt = sorted(df["joblevel"].dropna().unique()) if "joblevel" in df.columns else []

selected_dept = st.sidebar.multiselect(
    "Pilih Department:",
    options=dept_opt,
    default=dept_opt
)

selected_job = st.sidebar.multiselect(
    "Pilih Job Level:",
    options=job_opt,
    default=job_opt
)

# terapkan filter
filtered = df.copy()

if selected_dept:
    filtered = filtered[filtered["dept"].isin(selected_dept)]

if selected_job:
    filtered = filtered[filtered["joblevel"].isin(selected_job)]


# ================== NAVIGASI HALAMAN ==================
page = st.sidebar.radio(
    "Pilih Halaman:",
    ("Executive Overview", "Wellbeing & Workload", "Risk & Segmentation", "Actions & Playbook")
)

# ================== HALAMAN 1: EXECUTIVE OVERVIEW ==================
if page == "Executive Overview":
    st.subheader("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    # Total karyawan
    with col1:
        st.metric("Total Karyawan", len(filtered))

    # Rata-rata Job Satisfaction
    if "jobsatisfaction" in filtered.columns:
        with col2:
            st.metric(
                "Rata-rata Job Satisfaction",
                f"{filtered['jobsatisfaction'].mean():.2f} / 5"
            )

    # Rata-rata Stress
    if "stress" in filtered.columns:
        with col3:
            st.metric(
                "Rata-rata Stress",
                f"{filtered['stress'].mean():.2f} / 5"
            )

    # Rata-rata Work-Life Balance
    if "wlb" in filtered.columns:
        with col4:
            st.metric(
                "Rata-rata Work-Life Balance",
                f"{filtered['wlb'].mean():.2f} / 5"
            )

    st.markdown("### Komposisi Karyawan")

    col5, col6 = st.columns(2)

    # Pie komposisi gender
    if "gender" in filtered.columns:
        with col5:
            gender_count = (
                filtered["gender"]
                .value_counts()
                .reset_index(name="jumlah")
                .rename(columns={"index": "gender"})
            )
            fig_gender = px.pie(
                gender_count,
                names="gender",
                values="jumlah",
                title="Komposisi Gender"
            )
            st.plotly_chart(fig_gender, use_container_width=True)

    # Bar jumlah karyawan per department
    if "dept" in filtered.columns:
        with col6:
            dept_count = (
                filtered["dept"]
                .value_counts()
                .reset_index(name="jumlah")
                .rename(columns={"index": "dept"})
            )
            fig_dept = px.bar(
                dept_count,
                x="dept",
                y="jumlah",
                title="Jumlah Karyawan per Department"
            )
            st.plotly_chart(fig_dept, use_container_width=True)

    # Rata-rata job satisfaction per department
    if "jobsatisfaction" in filtered.columns and "dept" in filtered.columns:
        st.markdown("### Rata-rata Job Satisfaction per Department")
        js_dept = (
            filtered.groupby("dept")["jobsatisfaction"]
            .mean()
            .reset_index()
            .sort_values("jobsatisfaction", ascending=False)
        )
        fig_js_dept = px.bar(
            js_dept,
            x="dept",
            y="jobsatisfaction",
            title="Rata-rata Job Satisfaction per Department",
            labels={"jobsatisfaction": "Rata-rata Job Satisfaction"}
        )
        st.plotly_chart(fig_js_dept, use_container_width=True)

# ================== HALAMAN 2: WELLBEING & WORKLOAD ==================
elif page == "Wellbeing & Workload":
    st.subheader("Wellbeing & Workload Analysis")

    col1, col2, col3 = st.columns(3)

    # Rata-rata jam tidur
    if "sleephours" in filtered.columns:
        col1.metric("Rata-rata Jam Tidur", f"{filtered['sleephours'].mean():.1f} jam")

    # Rata-rata workload
    if "workload" in filtered.columns:
        col2.metric("Rata-rata Workload", f"{filtered['workload'].mean():.2f} / 5")

    # Rata-rata aktivitas fisik
    if "physicalactivityhours" in filtered.columns:
        col3.metric(
            "Rata-rata Aktivitas Fisik",
            f"{filtered['physicalactivityhours'].mean():.1f} jam/minggu"
        )

    if "haveot" in filtered.columns and "jobsatisfaction" in filtered.columns:
        js_ot = (
            filtered
            .groupby("haveot")["jobsatisfaction"]
            .mean()
            .reset_index()
            .sort_values("jobsatisfaction", ascending=False)
        )
        js_ot["haveot"] = js_ot["haveot"].map({False: "Tidak Lembur", True: "Lembur"})
        fig_ot = px.bar(
            js_ot,
            x="haveot",
            y="jobsatisfaction",
            title="Rata-rata Job Satisfaction: Lembur vs Tidak Lembur",
            labels={"haveot": "Status Lembur", "jobsatisfaction": "Rata-rata Job Satisfaction"}
        )
        st.plotly_chart(fig_ot, use_container_width=True)
    
    # Persentase Lembur per Department
    if "haveot" in filtered.columns and "dept" in filtered.columns:
        # True = 1, False = 0, jadi mean() langsung = proporsi lembur
        ot_dept = (
            filtered.groupby("dept")["haveot"]
            .mean()
            .reset_index()
            .rename(columns={"haveot": "ot_rate"})
            .sort_values("ot_rate", ascending=False)
        )
        ot_dept["ot_rate"] = ot_dept["ot_rate"] * 100

        fig_ot_dept = px.bar(
            ot_dept,
            x="dept",
            y="ot_rate",
            title="Persentase Karyawan Lembur per Department",
            labels={"dept": "Department", "ot_rate": "% Karyawan Lembur"}
        )
        st.plotly_chart(fig_ot_dept, use_container_width=True)

    # Boxplot Stress vs Job Satisfaction
    if "stress" in filtered.columns and "jobsatisfaction" in filtered.columns:
        fig_stress = px.box(
            filtered,
            x="stress",
            y="jobsatisfaction",
            points="all",
            title="Job Satisfaction vs Stress Level"
        )
        st.plotly_chart(fig_stress, use_container_width=True)

    # Boxplot WLB vs Job Satisfaction
    if "wlb" in filtered.columns and "jobsatisfaction" in filtered.columns:
        fig_wlb = px.box(
            filtered,
            x="wlb",
            y="jobsatisfaction",
            points="all",
            title="Job Satisfaction vs Work-Life Balance"
        )
        st.plotly_chart(fig_wlb, use_container_width=True)

# ================== HALAMAN 3: RISK & SEGMENTATION ==================
elif page == "Risk & Segmentation":
    st.subheader("Risk & Segmentation")

    if "jobsatisfaction" in filtered.columns:
        tmp = filtered.copy()
        tmp["low_sat"] = tmp["jobsatisfaction"] <= 3

        low_sat_rate = tmp["low_sat"].mean() * 100
        st.metric(
            "Persentase Karyawan Low Satisfaction (≤3)",
            f"{low_sat_rate:.1f}%"
        )

        # Risiko per department
        if "dept" in tmp.columns:
            seg = (
                tmp.groupby("dept")["low_sat"]
                .mean()
                .reset_index()
                .sort_values("low_sat", ascending=False)
            )
            seg["low_sat_pct"] = seg["low_sat"] * 100

            fig_seg = px.bar(
                seg,
                x="dept",
                y="low_sat_pct",
                title="Persentase Low Satisfaction per Department",
                labels={"low_sat_pct": "% Low Satisfaction"}
            )
            st.plotly_chart(fig_seg, use_container_width=True)

        # Risiko per job level
        if "joblevel" in tmp.columns:
            seg_j = (
                tmp.groupby("joblevel")["low_sat"]
                .mean()
                .reset_index()
                .sort_values("low_sat", ascending=False)
            )
            seg_j["low_sat_pct"] = seg_j["low_sat"] * 100

            fig_seg_j = px.bar(
                seg_j,
                x="joblevel",
                y="low_sat_pct",
                title="Persentase Low Satisfaction per Job Level",
                labels={"low_sat_pct": "% Low Satisfaction"}
            )
            st.plotly_chart(fig_seg_j, use_container_width=True)
        
        # Risiko per education level
        if "edulevel" in tmp.columns:
            seg_j = (
                tmp.groupby("edulevel")["low_sat"]
                .mean()
                .reset_index()
                .sort_values("low_sat", ascending=False)
            )
            seg_j["low_sat_pct"] = seg_j["low_sat"] * 100

            fig_seg_j = px.bar(
                seg_j,
                x="edulevel",
                y="low_sat_pct",
                title="Persentase Low Satisfaction per Education Level",
                labels={"low_sat_pct": "% Low Satisfaction"}
            )
            st.plotly_chart(fig_seg_j, use_container_width=True)

    st.markdown(
        "Visualisasi ini membantu mengidentifikasi segmen dengan risiko kepuasan rendah "
        "sebagai prioritas program HR."
    )

# ================== HALAMAN 4: ACTIONS & PLAYBOOK ==================
else:
    st.subheader("Actions & Playbook")
    st.markdown("""
**Ringkasan Insight (berbasis pola umum people analytics):**

1. Segmen dengan stres tinggi dan work-life balance rendah cenderung memiliki job satisfaction lebih rendah.  
2. Kebiasaan lembur yang berulang berpotensi berkaitan dengan kelelahan dan penurunan kepuasan.  
3. Perbedaan antar department dan job level menunjukkan perlunya intervensi spesifik, bukan kebijakan seragam.  

**Rekomendasi Strategis:**

- Evaluasi dan batasi lembur pada department dengan persentase low satisfaction tinggi.  
- Perkuat program work-life balance dan dukungan kesehatan mental.  
- Sediakan jalur karier dan peluang pengembangan yang jelas terutama bagi Level pendidikan yanggit tinggi.  
- Jadikan dashboard ini alat monitoring rutin untuk mendeteksi risiko lebih awal.
    """)