import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# header
st.set_page_config(page_title="Dashboard Bike Sharing (2011-2012)", layout="wide")
st.title("Dashboard Analisis Bike Sharing (2011-2012)")
st.markdown("""
Dashboard ini dikembangkan untuk memberikan visualiasi dan insight tentang tren penyewaan sepeda berdasarkan data historis (2011-2012). 
Sehingga dapat melihat langsung: 
1. Fluktuasi tren penyewaan terhadap cuaca & musim per hari (2011-2012).
2. Tren harian peminjaman pelanggan Casual dan Registered (2011-2012).
3. Proporsi dominasi tipe pelanggan di setiap rentang waktu (2011-2012).
""")

# load main data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    if 'season' in df.columns:
        urutan_musim = ['Spring', 'Summer', 'Fall', 'Winter']
        df['season'] = pd.Categorical(df['season'], categories=urutan_musim, ordered=True)
    return df

df = load_data()

# sidebar tempat logo dan filter hari, bulan, tahun
st.sidebar.markdown("Analisis Data Bike Sharing (2011-2012)")

# st.sidebar.image("logo.png", use_column_width=True) 
st.sidebar.image("data:image/jpeg;base64,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", use_container_width=True) # Gambar sementara

st.sidebar.title("Filter rentang waktu")
st.sidebar.markdown("Pilih rentang tanggal (2011-2012):")

min_date = df["dteday"].min()
max_date = df["dteday"].max()

start_date = st.sidebar.date_input(
    label='Tanggal Mulai',
    min_value=min_date,
    max_value=max_date,
    value=min_date
)

end_date = st.sidebar.date_input(
    label='Tanggal Akhir',
    min_value=min_date,
    max_value=max_date,
    value=max_date
)

if start_date > end_date:
    st.sidebar.error("Tanggal Akhir tidak boleh mendahului Tanggal Mulai.")
    st.stop()

# aplikasikan filter pada dataframe
main_df = df[(df["dteday"] >= pd.to_datetime(start_date)) & 
             (df["dteday"] <= pd.to_datetime(end_date))]

st.divider() 

# musim dan cuaca
st.header("1. Dampak Musim dan Cuaca Terhadap Fluktuasi Penyewaan")
col1, col2 = st.columns(2)

with col1:
    musim_df = main_df.groupby('season')['cnt'].sum().reset_index()
    fig1a, ax1a = plt.subplots(figsize=(8, 5))
    sns.barplot(data=musim_df, x='season', y='cnt', palette='viridis', ax=ax1a)
    ax1a.set_title("Total Penyewaan Berdasarkan Musim", fontsize=14)
    ax1a.set_xlabel("Musim")
    ax1a.set_ylabel("Total Penyewaan")
    st.pyplot(fig1a)

with col2:
    cuaca_df = main_df.groupby('weathersit')['cnt'].sum().reset_index()
    fig1b, ax1b = plt.subplots(figsize=(8, 5))
    sns.barplot(data=cuaca_df, x='weathersit', y='cnt', palette='magma', ax=ax1b)
    ax1b.set_title("Total Penyewaan Berdasarkan Kondisi Cuaca", fontsize=14)
    ax1b.set_xlabel("Cuaca")
    ax1b.set_ylabel("Total Penyewaan")
    st.pyplot(fig1b)

st.success("""
**Insight :** Berdasarkan rentang waktu yang dipilih, terlihat jelas fluktuasi penyewaan di setiap musim dan cuaca. 
**Rekomendasi:** Tim operasional dapat memanfaatkan waktu saat musim sepi (seperti Winter/Spring) atau saat cuaca memburuk untuk melakukan **perawatan sepeda (maintenance) secara keseluruhan**, agar sepeda siap dipakai maksimal saat musim panas dan gugur.
""")

st.divider()

# tren harian casual dan registered
st.header("2. Tren Harian Pelanggan (Casual dan Registered)")


tren_harian = main_df.groupby('dteday')[['casual', 'registered']].sum().reset_index()
tren_harian_melted = pd.melt(tren_harian, id_vars=['dteday'], value_vars=['casual', 'registered'],
                             var_name='Tipe Pelanggan', value_name='Total Penyewaan')

fig2, ax2 = plt.subplots(figsize=(14, 6))
sns.lineplot(data=tren_harian_melted, x='dteday', y='Total Penyewaan', hue='Tipe Pelanggan', 
             palette=['#66b3ff', '#ff9999'], marker='o', linewidth=2, ax=ax2)

ax2.set_title('Tren Harian Penyewaan Sepeda (Casual vs Registered)', fontsize=16)
ax2.set_xlabel('Tanggal', fontsize=12)
ax2.set_ylabel('Total Sepeda Disewa', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.5) 
st.pyplot(fig2)

st.info("""
**Insight :** Pola tren harian di atas menunjukkan perbedaan pola penyewaan antara pelanggan Casual dan Registered setiap harinya.
**Rekomendasi:** Jika garis warna Casual terlihat meningkat di hari-hari tertentu (seperti akhir pekan), tim marketing dapat meluncurkan **promo membership spesial (diskon pendaftaran)** tepat di hari-hari tersebut untuk menarik mereka menjadi pelanggan membership (Registered).
""")

st.divider()

# proporsi total pelanggan
st.header("3. Proporsi Total Pelanggan (Registered dan Casual)")

total_casual = main_df['casual'].sum()
total_registered = main_df['registered'].sum()

fig3, ax3 = plt.subplots(figsize=(8, 6))
labels = ['Casual (Biasa)', 'Registered (Member)']
sizes = [total_casual, total_registered]
colors = ['#B22222', '#728C69']
explode = (0.05, 0) 

if total_casual == 0 and total_registered == 0:
    st.warning("Tidak ada penyewaan pada rentang tanggal yang dipilih.")
else:
    ax3.pie(
        sizes, 
        explode=explode, 
        labels=labels, 
        colors=colors, 
        autopct='%1.1f%%', 
        shadow=True, 
        startangle=140,
        textprops={'fontsize': 12}
    )
    ax3.set_title("Dominasi Tipe Pelanggan Saat Ini", fontsize=14, fontweight='bold')
    st.pyplot(fig3)

    st.success(f"Berdasarkan rentang waktu yang difilter, jumlah penyewaan oleh pelanggan **Registered (Member)** sebanyak **{total_registered:,}**, sedangkan Casual sebanyak **{total_casual:,}**.")

st.caption("Copyright © 2026 - Bike Sharing Analytics - cillano")
