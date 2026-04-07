import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# set halaman
st.set_page_config(page_title="Dashboard Penyewaan Sepeda",  layout="wide")
st.title("Dashboard Analisis Penyewaan Sepeda")
st.markdown("""Dashboard ini saya kembangkan untuk memberikan wawasan mendalam tentang tren penyewaan sepeda berdasarkan data historis. Sehingga dapat memahami: 
1. Pola Peminjaman Harian by Pelanggan Casual dan Registered
2. tren penyewaan yang berhubungan dengan cuaca      
3. Pola/perilaku Pelanggan member (Registed) dan non-member (Casual)
4. Lebih banyak mana Pelanggan saat ini (Resgistered) atau (Casual) ? """)

# Load main_data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Mengurutkan kategori musim 
    if 'season' in df.columns:
        urutan_musim = ['Spring', 'Summer', 'Fall', 'Winter']
        df['season'] = pd.Categorical(df['season'], categories=urutan_musim, ordered=True)
    return df

df = load_data()

st.divider() 

# visual pula prminjaman harian berdasarkan berdasarkan tipe pelanggan
st.header("1. Pola Peminjaman Harian berdasarkan berdasarkan tipe pelanggan")

# 'hr'rata-rata 
jam_rental = df.groupby('hr')[['casual', 'registered']].mean().reset_index()

# Meleburkan data (melt) agar Seaborn bisa membedakan dua garis warna
jam_rental_melted = pd.melt(jam_rental, id_vars=['hr'], value_vars=['casual', 'registered'],
                              var_name='Pelanggan', value_name='Rata-rata Peminjam')

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=jam_rental_melted, x='hr', y='Rata-rata Peminjam', hue='Pelanggan', 
             palette=['#66b3ff', '#ff9999'], marker='o', linewidth=2, ax=ax1)

ax1.set_title('Pola Peminjaman Rata-rata per Jam (Casual dan Registered)', fontsize=14)
ax1.set_xlabel('Jam (0-23)', fontsize=12)
ax1.set_ylabel('Rata-rata Jumlah Peminjam', fontsize=12)

ax1.set_xticks(range(0, 24))
ax1.grid(True, linestyle='--', alpha=0.5) 

st.pyplot(fig1)

st.divider()

# Visual bahwa musim dan cuaca berpengaruh terhadap penyewaan sepeda
st.header("2. Dampak Musim dan Cuaca Terhadap Penyewaan")
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

st.divider()

#tren penyewaan sepeda sepanjang hari pada hari kerja dan hari libur
st.header(" 3. Pola Penyewaan Sepeda Sepanjang Hari (00:00 - 23:00)")

# pisahihin hari kerja dan hari libur
hari_kerja_df = df[df['workingday'].isin(['Ya', 1, 'Hari Kerja'])]
hari_libur_df = df[df['workingday'].isin(['Tidak', 0, 'Hari Libur/Weekend'])]

# rata-rata penyewaan per jam
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
    # format 00:00
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

st.divider()

# visualisasi proporsi total pelanggan 
st.header("4. Proporsi Total Pelanggan (Registered dan Casual)")

# total penyewaan masing masing tipe pelanggan
total_casual = df['casual'].sum()
total_registered = df['registered'].sum()

# pie chart
fig5, ax5 = plt.subplots(figsize=(8, 6))
labels = ['Casual (Biasa)', 'Registered (Member)']
sizes = [total_casual, total_registered]
colors = ['#B22222', '#728C69']
explode = (0.05, 0) 

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

ax5.set_title("Lebih banyak mana pelanggan saat ini?", fontsize=14, fontweight='bold')

st.pyplot(fig5)

st.success(f"Pelanggan **Registered** sebagai pelanggan yang paling banyak dengan total **{total_registered:,}** (**Member**), sedangkan Casual **{total_casual:,}**.")

st.caption("Cillano 2026 - Bike Sharing Analisis")