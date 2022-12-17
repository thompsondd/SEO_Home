# pip freeze > requirements.txt
import time
import streamlit as st
import numpy as np
import altair as alt
import pandas as pd
import webbrowser
from PIL import Image
import database as db
import streamlit_nested_layout

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
    page_title="Home Ai Search",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.facebook.com/profile.php?id=100008279142274',
        'Report a bug': "https://www.facebook.com/profile.php?id=100008279142274",
        'About': "# if you have something to report dm https://www.facebook.com/profile.php?id=100008279142274"
    }
)


st.balloons()
col1, col2, col3 = st.columns((2,4,4))
with col1:
    st.image(Image.open('logo.png'), width=250)
with col2:
    st.subheader(' ')
    st.header('Home AI search')
    st.subheader('Your choice, your comfort')

with st.form("first_form"):
    col1, col2, col3 = st.columns((1,1,1))
    with col1:
        quan = st.multiselect(
                'Quận',
                ('Select All','1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 
                'Tân Bình', 'Bình Tân', 'Tân Phú', 'Bình Thạnh', 'Gò Vấp', 'Phú Nhuận',
                'Hóc Môn', 'Bình Chánh', 'Nhà Bè', 'Củ Chi'))
        
        
        
    with col2:
        bottom_money = st.selectbox('Giá thấp nhất (triệu vnd)', ('Giá thấp nhất',20,40,60,80,100))
        if bottom_money == 'Giá thấp nhất':
            bottom_money = 0 
    with col3:
        top_money = st.selectbox('Giá cao nhất (triệu vnd)', ('Giá cao nhất', 120, 140, 160, 180, 200))
        if top_money == 'Giá cao nhất':
            top_money = 200
    
    area = st.slider('Diện tích (m²)', 0, 500, (0, 500))
    
    col1, col2 = st.columns((1,1))
    with col1:
        sleep = st.selectbox('Số phòng ngủ', (1,2,3,4,5))
    with col2:
        vs = st.selectbox('Số phòng vệ sinh', (1,2,3))
    submitted = st.form_submit_button("Search")


if submitted:
    if not quan:
        st.warning("CHỌN QUẬN")
    else:

        user = db.fetch_all_apartments()    
        if "Select All" in quan:
                quan = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 
                'Tân Bình', 'Bình Tân', 'Tân Phú', 'Bình Thạnh', 'Gò Vấp', 'Phú Nhuận',
                'Hóc Môn', 'Bình Chánh', 'Nhà Bè', 'Củ Chi')
        else:
            number = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
            temp1, temp2 = [], []
            list(map(lambda x: temp1.append(x) if x not in number else temp2.append(x),quan))
            temp2 = np.array(temp2).astype(int)
            temp1.sort()
            temp2.sort()
            if len(temp1) != 0 and len(temp2) != 0:
                quan = np.concatenate((temp2,temp1))
            
        huyen = ['Nhà Bè', 'Củ Chi','Hóc Môn', 'Bình Chánh']
        distric_tab = st.tabs(list(map(lambda x: f"Quận {x}" if x not in huyen else f"Huyện {x}",quan)))
        
        for i,tabs in zip(quan,distric_tab):
            dis = []
            for us in user:
                if (us['districts'] == i):
                    if(check1(us,'rates',[bottom_money, top_money])):
                        if(check1(us,'areas',area)):
                            if(check2(us,'wc',vs)):
                                if(check2(us,'bedrooms',sleep)):
                                    dis.append(us)
            with tabs:
                if i not in huyen:
                    st.header('Quận ' + i)
                else:
                    st.header('Huyện  ' + i)
                if (len(dis)==0):
                    st.write("Không tìm thấy dữ liệu phù hợp!")
                else:
                    for d in dis: 
                        width = 500
                        col1, col2 = st.columns((1,1))
                        with col1:
                            st.image(d['links'],width=width)
                        with col2:

                            st.subheader(d['key'])
                            st.info(d['addresses'] + ", Phường " + d['wards'] + (", Quận " + d['districts'] if d['districts'] not in huyen else f", Huyện {d['districts']}")  + ', Tp.HCM', icon="🏢")
                        
                            col1, col2, col3, col4 = st.columns((1.3,1,1,1.7))
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
                        st.write('- - - - - - - - - - - - - - - - - - ')
                            
                    
        
            

url = 'https://youtu.be/'
url_= 'dQw4w9WgXcQ'

if st.button('_do not click_ **this**'):
    webbrowser.open_new_tab(url+url_)
    st.caption('i told ya')

