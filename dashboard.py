import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# header
st.set_page_config(page_title="Dashboard Penyewaan Sepeda (2011-2012)", layout="wide")
st.title("Dashboard Analisis Penyewaan Sepeda")
st.markdown("""
Dashboard ini dikembangkan untuk memberikan visualiasi dan insight tentang tren penyewaan sepeda berdasarkan data historis (2011-2012). 
Sehingga dapat melihat langsung : 
1. Pola Peminjaman Harian by Pelanggan Casual dan Registered
2. fluktuasi tren penyewaan terhadap cuaca & musim      
3. Pola/perilaku Pelanggan member (Registered) dan non member (Casual)
4. Proporsi dominasi tipe pelanggan di setiap rentan waktu selama periode 2011-2012.
""")

# load main_data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # urutan musim
    if 'season' in df.columns:
        urutan_musim = ['Spring', 'Summer', 'Fall', 'Winter']
        df['season'] = pd.Categorical(df['season'], categories=urutan_musim, ordered=True)
    return df

df = load_data()

st.divider() 

# chart visualisasi
st.header("1. Pola Peminjaman Harian Berdasarkan Tipe Pelanggan")

jam_rental = df.groupby('hr')[['casual', 'registered']].mean().reset_index()
jam_rental_melted = pd.melt(jam_rental, id_vars=['hr'], value_vars=['casual', 'registered'],
                            var_name='Pelanggan', value_name='Rata-rata Peminjam')

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=jam_rental_melted, x='hr', y='Rata-rata Peminjam', hue='Pelanggan', 
             palette=['#66b3ff', '#ff9999'], marker='o', linewidth=2, ax=ax1)

# highlight area siang-sore untuk Casual, supaya bisa ambil kesimpulan untuk keputusan proosi membership
ax1.axvspan(12, 16, color='#ff9999', alpha=0.1)

ax1.set_title('Pola Peminjaman Rata-rata per Jam (Casual dan Registered)', fontsize=14)
ax1.set_xlabel('Jam (0-23)', fontsize=12)
ax1.set_ylabel('Rata-rata Jumlah Peminjam', fontsize=12)
ax1.set_xticks(range(0, 24))
ax1.grid(True, linestyle='--', alpha=0.5) 
st.pyplot(fig1)

st.info("""
**Insight:** Ternyata para pekerja kantoran dan anak sekolah adalah pelanggan *membership* (Registered) yang menyewa sepeda untuk keperluan berangkat (08:00) dan pulang (17:00) kerja/sekolah. 

**Rekomendasi tindakan bisnis :** Tim marketing dapat menargetkan **promosi membership pada pelanggan casual di rentang siang - sore hari (12:00 - 16:00)**, karena pada jam-jam itulah pelanggan *casual* paling aktif melakukan penyewaan.
""")

st.divider()

# fluktuasi penyewaan terhadap cuaca & musim
st.header("2. Dampak Musim dan Cuaca terhadap Fluktuasi penyewaan")
col1, col2 = st.columns(2)

with col1:
    musim_df = df.groupby('season')['cnt'].sum().reset_index()
    fig2a, ax2a = plt.subplots(figsize=(8, 5))
    sns.barplot(data=musim_df, x='season', y='cnt', palette='viridis', ax=ax2a)
    ax2a.set_title("Total Penyewaan Berdasarkan Musim")
    ax2a.set_xlabel("Musim")
    ax2a.set_ylabel("Total Penyewaan")
    st.pyplot(fig2a)

with col2:
    cuaca_df = df.groupby('weathersit')['cnt'].sum().reset_index()
    fig2b, ax2b = plt.subplots(figsize=(8, 5))
    sns.barplot(data=cuaca_df, x='weathersit', y='cnt', palette='magma', ax=ax2b)
    ax2b.set_title("Total Penyewaan Berdasarkan Kondisi Cuaca")
    ax2b.set_xlabel("Cuaca")
    ax2b.set_ylabel("Total Penyewaan")
    st.pyplot(fig2b)

st.success("""
**Insight:** Grafik menunjukkan puncak keramaian terjadi di musim panas (Summer) dan gugur (Fall). 

**Rekomendasi tindakan bisnis :** Tim operasional dapat melakukan **perawatan (maintenance) sepeda secara keseluruhan pada awal musim semi (Spring) dan dingin (Winter)**. Waktu tersebut adalah momen yang paling pas untuk melakukan perawatan kelayakan agar seluruh armada siap disewa maksimal saat musim panas dan gugur tiba.
""")

st.divider()

# pola penyewaan sepanjang hari (hari kerja dan libur)
st.header(" 3. Pola Penyewaan Sepanjang Hari (Hari Kerja dan Libur)")

hari_kerja_df = df[df['workingday'].isin(['Ya', 1, 'Hari Kerja'])]
hari_libur_df = df[df['workingday'].isin(['Tidak', 0, 'Hari Libur/Weekend'])]

tren_kerja = hari_kerja_df.groupby('hr')['cnt'].mean().reset_index()
tren_libur = hari_libur_df.groupby('hr')['cnt'].mean().reset_index()

col3, col4 = st.columns(2)

with col3:
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=tren_kerja, x='hr', y='cnt', marker='o', color='#d9534f', linewidth=2.5, ax=ax3)
    ax3.set_title("Tren 24 Jam (HARI KERJA)", fontsize=14)
    ax3.set_xlabel("Jam")
    ax3.set_ylabel("Rata-rata Penyewaan")
    ax3.set_xticks(range(0, 24))
    ax3.set_xticklabels([f"{i:02d}:00" for i in range(0, 24)], rotation=45)
    ax3.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig3)

with col4:
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=tren_libur, x='hr', y='cnt', marker='o', color='#5cb85c', linewidth=2.5, ax=ax4)
    ax4.set_title("Tren 24 Jam (HARI LIBUR)", fontsize=14)
    ax4.set_xlabel("Jam")
    ax4.set_ylabel("Rata-rata Penyewaan")
    ax4.set_xticks(range(0, 24))
    ax4.set_xticklabels([f"{i:02d}:00" for i in range(0, 24)], rotation=45)
    ax4.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig4)

st.warning("""
**Insight:** Pola keramaian hari kerja dan hari libur memiliki jam jam ramainya masing masing. Ternyata di hari libur tidak ada lonjakan tajam pelanggan menyewa sepeda.

**Rekomendasi tindakan bisnis:** Karena sudah tahu di jam berapa *peak* dan sepinya permintaan pelanggan, tim operasional dapat mempersiapkan dengan baik ketersediaan kelengkapan dan perapihan pemulangan sepeda di titik kumpul penyewaan *sebelum* jam sibuk tersebut.
""")

st.divider()

# proporsi total pelanggan 
st.header("4. Proporsi Total Pelanggan (Registered dan Casual)")
st.markdown("Gunakan kalender di bawah ini untuk melihat proporsi pelanggan pada rentang waktu tertentu:")

# input tanggal
col_filter1, col_filter2 = st.columns(2)
min_date = df["dteday"].min()
max_date = df["dteday"].max()

with col_filter1:
    start_date = st.date_input(
        label='Tanggal Mulai',
        min_value=min_date,
        max_value=max_date,
        value=min_date
    )

with col_filter2:
    end_date = st.date_input(
        label='Tanggal Akhir',
        min_value=min_date,
        max_value=max_date,
        value=max_date
    )

if start_date > end_date:
    st.error("Harap pastikan Tanggal Akhir tidak mendahului Tanggal Mulai.")
    st.stop()

filtered_df = df[(df["dteday"] >= pd.to_datetime(start_date)) & 
                 (df["dteday"] <= pd.to_datetime(end_date))]

# total pelanggan yang sudah di filter sesuai tanggal
total_casual = filtered_df['casual'].sum()
total_registered = filtered_df['registered'].sum()

# pie chart
fig5, ax5 = plt.subplots(figsize=(8, 6))
labels = ['Casual (Biasa)', 'Registered (Member)']
sizes = [total_casual, total_registered]
colors = ['#B22222', '#728C69']
explode = (0.05, 0) 

if total_casual == 0 and total_registered == 0:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
else:
    ax5.pie(
        sizes, 
        explode=explode, 
        labels=labels, 
        colors=colors, 
        autopct='%1.1f%%', 
        shadow=True, 
        startangle=140,
        textprops={'fontsize': 12}
    )

    ax5.set_title(f"Lebih banyak mana pelanggan saat ini?", fontsize=14, fontweight='bold')
    st.pyplot(fig5)

    st.success(f"Berdasarkan rentang waktu yang dipilih, pelanggan **Registered (Member)** mendominasi dengan total **{total_registered:,}** penyewaan, sedangkan Casual sebanyak **{total_casual:,}**.")

st.caption("Cillano 2026 - Bike Sharing Analisis")
