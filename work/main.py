import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import sklearn


# Загрузка модели и кодировщиков
model = joblib.load('model.pkl')
label_encoders = joblib.load('label_encoders.pkl')

# Загрузка словарей
with open('cat_dict.json', 'r', encoding='utf-8') as f:
    cat_dict = json.load(f)

# Функция для кодирования нового ввода
def encode_input(input_data, label_encoders):
    df_input = pd.DataFrame([input_data])
    for col, le in label_encoders.items():
        df_input[col] = le.transform(df_input[col])
    return df_input

# Streamlit приложение
st.title('Цена на квартиры в Москве')

# Ввод категориальных значений
apartment_type = st.selectbox('Выберите значение для типа апартаментов', options=list(cat_dict['Apartment type'].keys()))
metro_station = st.selectbox('Выберите значение для станции метро', options=list(cat_dict['Metro station'].keys()))
renovation = st.selectbox('Выберите значение для ремонта', options=list(cat_dict['Renovation'].keys()))

# Ввод числовых значений
minutes_to_metro = st.number_input('Введите количество минут до метро', min_value=0, step=1)
number_of_rooms = st.number_input('Введите количество комнат', min_value=0, step=1)
area = st.number_input('Введите общую площадь', min_value=0.0, step=0.1)
living_area = st.number_input('Введите жилую площадь', min_value=0.0, step=0.1)
kitchen_area = st.number_input('Введите площадь кухни', min_value=0.0, step=0.1)
floor = st.number_input('Введите этаж', min_value=0, step=1)
number_of_floors = st.number_input('Введите количество этажей', min_value=0, step=1)

# Кодирование введенных данных
input_data = {
    'Apartment type': apartment_type,
    'Metro station': metro_station,
    'Renovation': renovation,
    'Minutes to metro': minutes_to_metro,
    'Number of rooms': number_of_rooms,
    'Area': area,
    'Living area': living_area,
    'Kitchen area': kitchen_area,
    'Floor': floor,
    'Number of floors': number_of_floors
}
encoded_input = encode_input(input_data, label_encoders)

# Упорядочивание признаков в соответствии с обучением
encoded_input = encoded_input[[
    'Apartment type', 'Metro station', 'Minutes to metro', 'Number of rooms',
    'Area', 'Living area', 'Kitchen area', 'Floor', 'Number of floors', 'Renovation'
]]

# Отображение закодированных данных
st.write('Закодированные значения:')
st.write(encoded_input)

# Применение модели
prediction = model.predict(encoded_input)
st.write('Предсказание модели:')
st.write(prediction)
