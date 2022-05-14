#import matplotlib
import streamlit as st
import numpy as np
#import math
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point


with st.echo(code_location='below'):

    def go():
        df = pd.read_csv('addresses moscow.csv', sep = ',')
        df2 = df[df['repressed'] > 1]
        ratio = df2['longitude'].count()/df['longitude'].count()
        st.title("Hello, repressions!")
        st.header('Изучаем историю Москвы на открытых данных')
        st.write('Я взял базу данных о расстрелянных москвичах отсюда: https://www.memo.ru/ru-ru/projects/hackathon '
                 '(Спаибо Мемориалу, признанному иностранным агентом) '
                 'и изучил места последнего проживания людей, которых расстреляли в ходе репрессий. '
                 'Всего в базе данных было **%d** строк. Каждая соответствует адресу, по которому проживал хотя бы один репрессированный. ' %(df['longitude'].count()))
        st.write('Из этого списка у **%.1f** процентов домов репрессировано более 1 человека.'
                 ' На графике ниже вы можете найти расположенные в алфавитном порядке районы и, наведя мышь на бар, посмотреть сколько человек '
                 '(не домов, а именно людей!) было расстреляно в этом дистрикте.' %(ratio*100))

        adm_moscow = gpd.read_file('http://gis-lab.info/data/mos-adm/mo.geojson')

        houses = [Point(row['longitude'], row['latitude']) for _, row in df.iterrows()]
        houseswitha = gpd.GeoDataFrame(df, geometry = houses, crs = "EPSG:4326")

        kart = adm_moscow.sjoin(houseswitha)
        print(kart[['NAME', 'street', 'house', 'repressed']])
        repression_counts = kart.groupby('NAME')['repressed'].sum()
        st.bar_chart(repression_counts, use_container_width=True)
        fig, ax = plt.subplots()

        st.write('На графике ниже по-другому изображаются те же данные. '
                 ' Видно явное увеличение количества репрессированных при приближении к центру.')
        st.pyplot(adm_moscow.set_index('NAME').assign(repression_counts = repression_counts)
                  .plot(column = 'repression_counts', ax = ax, legend = True, cmap = 'Reds').figure)
        dfmap = df[['longitude', 'latitude']].dropna(inplace = False)
        st.write('Ниже интерактивная карта с нанесенными на неё адресами расстрелянных. (Можете приблизить её и рассмотреть лучше).'
                 ' Заметно, что есть и те люди, которые даже по нынешним меркам жили не в Москве, а рядом (см. Королёв, Дзержинск и тд)')
    #    st.write(dfmap)
        st.map(dfmap)
        st.markdown("<h1 style='text-align: center; color: red;'>242</h1>", unsafe_allow_html=True)
        st.subheader('Это наибольшее количество человек, которые жили по одному адресу, и были расстреляны. '
                 'Этот адрес – улица Сирафимовича, дом 2. Дом на набережной, который видел каждый.'
                 ' Об этом жилом комплексе можно почитать '
                 '[здесь](https://ru.wikipedia.org/wiki/%D0%94%D0%BE%D0%BC_%D0%BD%D0%B0_%D0%BD%D0%B0%D0%B1%D0%B5%D1%80%D0%B5%D0%B6%D0%BD%D0%BE%D0%B9) '
                 'и [здесь](https://www.corpus.ru/products/urij-slezkin-dom-pravitelstva.htm) ')

        source = df['repressed'].value_counts(normalize = False).sort_index()
        source = source.reset_index()
    #    st.write(source)
        number = st.number_input('Введите количество людей, которые были соседями и подверглись расстрелу,'
                 ' и вы увидете, сколько было домов с таким или большим количеством сожителей ')
        res = source[source['index'] >= number]
        res = res['repressed'].sum()
        st.subheader(res)
        st.header('Подводя итоги, живите без расстрелов.')


    go()
