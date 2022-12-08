# pip freeze > requirements.txt
import time
import streamlit as st
import numpy as np
import altair as alt
import pandas as pd
import webbrowser
from PIL import Image
import database as db

def check1(us, col, c):
    temp1 = np.array(us[col].split("-")).astype(float)
    temp1 = np.ceil(temp1).astype(int)
    if(len(temp1) > 1):
        if temp1[0] in range(c[0],c[1]+1) and temp1[1] in range(c[0],c[1]+1):
            return True
    else:
        if temp1 in range(c[0],c[1]+1) and temp1 in range(c[0],c[1]+1):
            return True
    
    return False

def check2(us, col, c):
    temp1 = np.array(us[col].split("-")).astype(int)
    if c in range(temp1[0],temp1[1]+1):
        return True
    
    return False

st.set_page_config(
    page_title="Datvilla",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.facebook.com/profile.php?id=100008279142274',
        'Report a bug': "https://www.facebook.com/profile.php?id=100008279142274",
        'About': "# if you have something to report dm https://www.facebook.com/profile.php?id=100008279142274"
    }
)


col1, col2, col3 = st.columns((2,4,1))
with col1:
    st.image(Image.open('dark_logo.png'))
with col2:
    st.header(' ')
    st.header('Knowledge Represent')
    st.markdown('Your choice, your comfort')

with st.form("my_form"):
    quan = st.multiselect(
        'Quận',
        ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 
        'Tân Bình', 'Bình Tân', 'Tân Phú', 'Bình Thạnh', 'Gò Vấp', 'Phú Nhuận',
        'Hóc Môn', 'Bình Chánh', 'Nhà Bè', 'Củ Chi'))

    submitted = st.form_submit_button("Next")

if not quan and submitted==True:
    st.warning("Hãy chọn quận!!",icon="⚠️")

if len(quan)!=0:
    with st.expander('Bộ lọc'):
        money = st.slider('Giá tiền (triệu/m²)',0, 200, (0, 50))
        area = st.slider('Diện tích m²', 0, 500, (0, 70))
        col1, col2 = st.columns((1,1))
        with col1:
            sleep = st.selectbox('Số phòng ngủ', (1,2,3,4,5))
        with col2:
            vs = st.selectbox('Số phòng vệ sinh', (1,2,3))
        search = st.button("Search")
    if search:
        user = db.fetch_all_apartments()    
        dis = []
        for us in user:
            for i in quan:
                if (us['districts'] == i):
                    if(check1(us,'rates',money)):
                        if(check1(us,'areas',area)):
                            if(check2(us,'wc',vs)):
                                if(check2(us,'bedrooms',sleep)):
                                    dis.append(us)

        for q in quan:
            st.header('Quận ' + q)
            if (len(dis)==0):
                st.write("Không tìm thấy dữ liệu phù hợp!")
            else:
                for d in dis: 
                    # st.write(d)
                    st.subheader(d['key'])
                    st.info(d['addresses'] + ", phường " + d['wards'] + ", quận " + d['districts'] + ', Tp.HCM', icon="🏢")
                    col1, col2, col3, col4 = st.columns((1.3,1,1,1.5))
                    with col1:
                        st.info(d['areas'] + ' m²',icon='🛋')
                    with col2:
                        st.success(d['bedrooms'],icon='🛏️')
                    with col3:
                        st.warning(d['wc'],icon='🛁')
                    with col4:
                        st.error(d['rates'] + " triệu/m²",icon='💲')
                    with st.expander('Những tiện ích xung quanh'):
                        col1, col2, col3, col4 = st.columns((3,1,3,1))
                        with col1:
                            st.markdown('Số trường học: ')
                            st.write('- - - - - - - - - - - - - - - - - - ')
                        with col2:
                            a=d['schools']
                            st.write(a)
                        with col3:
                            st.markdown('Số trạm xe bus: ')
                            st.write('- - - - - - - - - - - - - - - - - - ')
                        with col4:
                            a=d['buses']
                            st.write(a)
                        col1, col2, col3, col4 = st.columns((3,1,3,1))
                        with col1:
                            st.markdown('Số siêu thị: ')
                            st.write('- - - - - - - - - - - - - - - - - - ')
                        with col2:
                            a=d['markets']
                            st.write(a)
                        with col3:
                            st.markdown('Số trạm nhà hàng: ')
                            st.write('- - - - - - - - - - - - - - - - - - ')
                        with col4:
                            a=d['restaurants']
                            st.write(a)
                        col1, col2, col3, col4 = st.columns((3,1,3,1))
                        with col1:
                            st.markdown('Số cây ATM: ')
                        with col2:
                            a=d['atm']
                            st.write(a)
                        with col3:
                            st.markdown('Số cơ sở y tế: ')
                        with col4:
                            a=d['hospitals']
                            st.write(a) 

url = 'https://youtu.be/'
url_= 'dQw4w9WgXcQ'

if st.button('_do not click_ **this**'):
    webbrowser.open_new_tab(url+url_)
    st.caption('i told ya')



