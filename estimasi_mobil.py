import pandas as pd
import streamlit as st

try:
    dataset = pd.read_csv('toyota.csv') 
except FileNotFoundError:
    st.error("Dataset 'toyota.csv' tidak ditemukan. Pastikan file tersedia.")
    st.stop()

st.title('Estimasi Harga Mobil Bekas')
st.subheader('Estimasi Berdasarkan Data Historis')

selected_model = st.selectbox('Pilih Model Mobil', sorted(dataset['model'].unique()))


filtered_by_model = dataset[dataset['model'] == selected_model]

selected_year = st.selectbox(
    'Pilih Tahun Mobil', 
    sorted(filtered_by_model['year'].unique())
)
selected_mileage = st.selectbox(
    'Pilih Jarak Tempuh (dalam km)', 
    sorted(filtered_by_model[filtered_by_model['year'] == selected_year]['mileage'].unique())
)
selected_tax = st.selectbox(
    'Pilih Pajak Mobil (dalam £)', 
    sorted(filtered_by_model[(filtered_by_model['year'] == selected_year) & 
                             (filtered_by_model['mileage'] == selected_mileage)]['tax'].unique())
)
selected_mpg = st.selectbox(
    'Pilih Konsumsi BBM (mil per galon)', 
    sorted(filtered_by_model[(filtered_by_model['year'] == selected_year) & 
                             (filtered_by_model['mileage'] == selected_mileage) & 
                             (filtered_by_model['tax'] == selected_tax)]['mpg'].unique())
)
selected_engine_size = st.selectbox(
    'Pilih Ukuran Mesin (dalam liter)', 
    sorted(filtered_by_model[(filtered_by_model['year'] == selected_year) & 
                             (filtered_by_model['mileage'] == selected_mileage) & 
                             (filtered_by_model['tax'] == selected_tax) & 
                             (filtered_by_model['mpg'] == selected_mpg)]['engineSize'].unique())
)

final_filtered_data = filtered_by_model[
    (filtered_by_model['year'] == selected_year) &
    (filtered_by_model['mileage'] == selected_mileage) &
    (filtered_by_model['tax'] == selected_tax) &
    (filtered_by_model['mpg'] == selected_mpg) &
    (filtered_by_model['engineSize'] == selected_engine_size)
]

if st.button('Estimasi Harga'):
    if not final_filtered_data.empty:
        estimated_price = final_filtered_data['price'].mean()  # Rata-rata jika ada beberapa baris
        st.success(f"Harga estimasi mobil bekas: £{estimated_price:,.2f}")
        st.success(f"Konversi ke Rupiah (IDR): Rp{estimated_price * 19000:,.2f}")
    else:
        st.warning("Data tidak ditemukan. Coba kombinasi lain.")
