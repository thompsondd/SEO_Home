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
import backend

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


#st.balloons()
col1, col2, col3 = st.columns((2,4,4))

    #st.session_state.disabled = False
def get_and_set_time(time_now):
    if "time_searching" not in st.session_state:
        st.session_state["time_searching"] = time_now
    temp = st.session_state["time_searching"]
    st.session_state["time_searching"] = time_now
    return temp
with col1:
    st.image(Image.open('logo.png'), width=250)
with col2:
    st.subheader(' ')
    st.header('Home AI search')
    st.subheader('Your choice, your comfort')

with st.form("first_form"):
    priority = {"main":{},"sub":{}}
    with st.sidebar:
        st.title("Đánh giá mức độ quan trọng của các tiêu chí")
        st.subheader("1(Không quan trọng) - 10(Rất quan trọng)")

        priority["main"]["location_p"] = st.slider("Vị trí",1,10, step=1, key="location", value=10)
        priority["main"]["price_p"] = st.slider("Giá nhà",1,10, step=1, key="price", value=10)
        priority["main"]["area_p"] = st.slider("Diện tích",1,10, step=1, key="area")
        with st.expander("Tiêu chí về số lượng phòng"):
            priority["main"]["area_ele_p"] = st.slider("",1,10, step=1, key="area_p", value=7)
            c1,c2 = st.columns(2)
            priority["sub"]["area_ele_p"]={}
            with c1:
                priority["sub"]["area_ele_p"]["sleep_p"] = st.slider("Số lượng phòng ngủ",1,10, step=1, key="sleep", value=8)
            with c2:
                priority["sub"]["area_ele_p"]["wc_p"] = st.slider("Số lượng nhà vệ sinh",1,10, step=1, key="wc", value=8)

        with st.expander("Môi trường"):
            priority["main"]["env_p"] = st.slider("",1,10, step=1, key="env", value=6)
            c3,c4,c5 = st.columns(3)
            priority["sub"]["env_p"]={}
            with c3:
                priority["sub"]["env_p"]["school_p"] = st.slider("Số lượng trường trong khu vực",1,10, step=1, key="school",value=8)
            with c4:
                priority["sub"]["env_p"]["market_p"] = st.slider("Số lượng nơi mua sách trong khu vực",1,10, step=1, key="market",value=8)
            with c5:
                priority["sub"]["env_p"]["entertainment_p"] = st.slider("Số lượng nơi mua sắm trong khu vực",1,10, step=1, key="entertainment",value=8)
    
    col1, col2, col3 = st.columns((1,1,1))
    with col1:
        quan = st.multiselect(
                'Quận',
                ('Select All','1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 
                'Tân Bình', 'Bình Tân', 'Tân Phú', 'Bình Thạnh', 'Gò Vấp', 'Phú Nhuận',
                'Hóc Môn', 'Bình Chánh', 'Nhà Bè', 'Củ Chi'))
    with col2:
        bottom_money = st.selectbox('Giá thấp nhất (triệu/m²)', ('Giá thấp nhất',20,40,60,80,100))
        if bottom_money == 'Giá thấp nhất':
            bottom_money = 0 
    with col3:
        top_money = st.selectbox('Giá cao nhất (triệu/m²)', ('Giá cao nhất', 120, 140, 160, 180, 200))
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
        seo = backend.Manager    
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
            #quan.sort()
                #print(quan)

        requirments = {"quan":quan, "top_money":top_money,"bottom_money":bottom_money,
                       "area":area, "sleep":sleep, "vs":vs, "priority":priority}
        huyen = ['Nhà Bè', 'Củ Chi','Hóc Môn', 'Bình Chánh']
        start = time.time()
        search_result, recommendList = seo.search(requirments)
        end = time.time()
        #t1,t2 = st.tabs(["Tìm Kiếm","Gợi ý"])
        timeSearch = end-start
        st.metric("Search Time", str(timeSearch)+"s", str(get_and_set_time(timeSearch)-timeSearch)+"s")
        with st.expander("Danh sách căn hộ tìm được theo yêu cầu"):
            #with t1:
                distric_tab = st.tabs(list(map(lambda x: f"Quận {x}" if x not in huyen else f"Huyện {x}",quan)))
                for i,tabs in zip(quan,distric_tab):
                    #Search
                    dis =  search_result.get(i,None)
                    if dis==None:
                        continue                         
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
        
        with st.expander("Danh sách căn hộ gợi ý theo yêu cầu"):
            #with t2:
                for d in recommendList: 
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

#url = 'https://youtu.be/'
#url_= 'dQw4w9WgXcQ'
#
#if st.button('_do not click_ **this**'):
#    webbrowser.open_new_tab(url+url_)
#    st.caption('i told ya')

