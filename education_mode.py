# education_mode.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_basic_concepts():
    """Temel trading kavramlarını göster"""
    st.header("Temel Borsa Kavramları")
    
    concept = st.selectbox(
        "Hangi kavramı öğrenmek istiyorsunuz?",
        ["Trend Analizi", "Momentum", "Destek ve Direnç", "İşlem Hacimleri"]
    )
    
    if concept == "Trend Analizi":
        st.subheader("📈 Trend Nedir?")
        st.markdown("""
        Trend, finansal piyasalarda bir varlığın fiyat hareketinin genel yönünü ve karakterini gösteren temel bir kavramdır. 
        Üç tür trend vardır:

        - 📈 **Yükselen Trend (Uptrend)**: 
          Fiyatların sürekli olarak daha yüksek tepeler ve daha yüksek dipler oluşturduğu durumdur.
          Bu, piyasada alıcıların satıcılardan daha güçlü olduğunu gösterir.

        - 📉 **Düşen Trend (Downtrend)**: 
          Fiyatların sürekli olarak daha düşük tepeler ve daha düşük dipler oluşturduğu durumdur.
          Satıcıların baskın olduğu ve fiyatların düşüş eğiliminde olduğu bir piyasayı işaret eder.

        - ↔️ **Yatay Trend (Sideways)**: 
          Fiyatların belirli bir aralıkta dalgalandığı, net bir yön göstermediği durumdur.
          Alıcılar ve satıcılar arasında bir denge olduğunu gösterir.
        """)
        
        # İnteraktif trend gösterimi
        st.subheader("İnteraktif Trend Grafiği")
        trend_type = st.radio(
            "Trend tipini seçin:",
            ["Yükselen", "Düşen", "Yatay"]
        )
        
        # Örnek veri oluştur
        dates = pd.date_range(start='2024-01-01', periods=100)
        if trend_type == "Yükselen":
            price = np.linspace(100, 200, 100) + np.random.normal(0, 5, 100)
        elif trend_type == "Düşen":
            price = np.linspace(200, 100, 100) + np.random.normal(0, 5, 100)
        else:  # Yatay
            price = np.ones(100) * 150 + np.random.normal(0, 10, 100)
        
        df = pd.DataFrame({
            'Close': price,
            'signal': np.zeros(100)
        }, index=dates)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Fiyat'))
        fig.update_layout(title='Trend Analizi', xaxis_title='Tarih', yaxis_title='Fiyat')
        st.plotly_chart(fig, use_container_width=True)

    elif concept == "Momentum":
        st.subheader("🔄 Momentum")
        st.markdown("""
        Momentum, finansal piyasalarda fiyat hareketinin gücünü ve hızını gösteren önemli bir göstergedir:

        - 🚀 **Yüksek Momentum**: 
          Finansal piyasada yüksek momentum, bir varlığın fiyatının belirli bir süre boyunca güçlü ve istikrarlı bir şekilde yükselmesi (veya düşmesi) durumudur.
          - Yukarı yönlü: Varlık hızla ve kararlılıkla yükseliyor
          - Aşağı yönlü: Varlık hızla ve sürekli düşüyor

        - 🐌 **Düşük Momentum**: 
          Fiyat hareketinin zayıf ve yavaş olduğu durumu ifade eder.
          Piyasada belirgin bir yön eksikliği ve düşük volatilite görülür.

        - 🔄 **Momentum Değişimi**: 
          Mevcut trendin gücünün azaldığını ve olası bir trend değişimini işaret eder.
          Fiyat hareketindeki ivmenin yön değiştirmesi yakın olabilir.
        """)
        
        # Örnek momentum verisi oluştur
        dates = pd.date_range(start='2024-01-01', periods=100)
        price = np.cumsum(np.random.normal(0, 1, 100)) + 100
        momentum = np.gradient(price)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=price, name='Fiyat'))
        fig.add_trace(go.Scatter(x=dates, y=momentum*10+100, name='Momentum'))
        fig.update_layout(title='Momentum Göstergesi', xaxis_title='Tarih', yaxis_title='Değer')
        st.plotly_chart(fig, use_container_width=True)
        
    elif concept == "Destek ve Direnç":
        st.subheader("🎯 Destek ve Direnç Seviyeleri")
        st.markdown("""
        Destek ve direnç seviyeleri, fiyatın sıklıkla geri döndüğü psikolojik ve teknik öneme sahip fiyat seviyelerini temsil eder:

        - 💪 **Destek Seviyesi**: 
          Fiyatın düşüş trendinde zorlandığı ve genellikle yukarı döndüğü seviyedir.
          Alıcıların aktif olarak devreye girdiği ve düşüşün durduğu noktalardır.
          Kırılması durumunda önemli düşüşler görülebilir.

        - 🛑 **Direnç Seviyesi**: 
          Fiyatın yükseliş trendinde zorlandığı ve genellikle aşağı döndüğü seviyedir.
          Satıcıların yoğunlaştığı ve yükselişin durduğu noktalardır.
          Kırılması durumunda sert yükselişler yaşanabilir.
        """)
        
        # Örnek destek/direnç verisi oluştur
        dates = pd.date_range(start='2024-01-01', periods=100)
        price = np.cumsum(np.random.normal(0, 1, 100)) + 100
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=price, name='Fiyat'))
        fig.add_hline(y=price.mean() + 10, line_dash="dash", line_color="red", annotation_text="Direnç")
        fig.add_hline(y=price.mean() - 10, line_dash="dash", line_color="green", annotation_text="Destek")
        fig.update_layout(title='Destek ve Direnç Seviyeleri', xaxis_title='Tarih', yaxis_title='Fiyat')
        st.plotly_chart(fig, use_container_width=True)
        
    else:  # İşlem Hacimleri
        st.subheader("📊 İşlem Hacmi")
        st.markdown("""
        İşlem hacmi, bir finansal varlığın belirli bir zaman diliminde gerçekleşen alım-satım miktarını gösterir:

        - 📈 **Yüksek Hacim**: 
          Piyasada yoğun alım-satım aktivitesini gösterir.
          Trendin güçlü olduğunu ve fiyat hareketinin güvenilir olduğunu işaret eder.
          Önemli fiyat kırılımlarında yüksek hacim görülmesi, hareketin güvenilirliğini artırır.

        - 📉 **Düşük Hacim**: 
          Piyasada düşük alım-satım aktivitesini gösterir.
          Trendin zayıf olduğunu ve fiyat hareketinin sürdürülebilir olmayabileceğini işaret eder.
          Fiyat hareketlerinin manipülatif olma riski vardır.
        """)
        
        # Örnek hacim verisi oluştur
        dates = pd.date_range(start='2024-01-01', periods=100)
        price = np.cumsum(np.random.normal(0, 1, 100)) + 100
        volume = np.random.randint(1000, 10000, 100)
        
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                          vertical_spacing=0.03, subplot_titles=('Fiyat', 'Hacim'))
        
        fig.add_trace(go.Scatter(x=dates, y=price, name='Fiyat'), row=1, col=1)
        fig.add_trace(go.Bar(x=dates, y=volume, name='Hacim'), row=2, col=1)
        
        fig.update_layout(height=600, title='Fiyat ve Hacim Analizi')
        st.plotly_chart(fig, use_container_width=True)

def show_technical_analysis_basics():
    """Teknik analiz temellerini göster"""
    st.header("Teknik Analiz Temelleri")
    
    topic = st.selectbox(
        "Hangi konuyu öğrenmek istiyorsunuz?",
        ["Teknik Analiz Nedir?", "Trend Göstergeleri", "Momentum Göstergeleri", "Hacim Göstergeleri"]
    )
    
    if topic == "Teknik Analiz":
        st.markdown("""
        ### 📊 Teknik Analiz Nedir?
        
        Teknik analiz, finansal piyasalarda geçmiş fiyat ve hacim verilerini kullanarak gelecekteki fiyat hareketlerini tahmin etmeye çalışan bir analiz yöntemidir.
        
        ### 🎯 Temel Prensipler:
        
        1. **Fiyat Her Şeyi Yansıtır**
           - Piyasadaki tüm bilgiler (ekonomik, politik, psikolojik) fiyatlara yansır
           - Temel analiz verilerinin etkisi de fiyatlarda görülür
           - Geçmiş fiyat hareketleri gelecekteki hareketler hakkında ipucu verir
        
        2. **Fiyatlar Trend Halinde Hareket Eder**
           - Başlayan bir trend, devam etme eğilimindedir
           - Trendler, karşıt bir güç tarafından durdurulana kadar sürer
           - Trend değişimleri genellikle belirli sinyallerle önceden tespit edilebilir
        
        3. **Tarih Tekerrür Eder**
           - Fiyat formasyonları benzer şekillerde tekrarlanır
           - Trader psikolojisi benzer durumlarda benzer tepkiler verir
           - Geçmiş başarılı stratejiler gelecekte de işe yarayabilir
        """)
        
    elif topic == "Trend Göstergeleri":
        st.markdown("""
        ### 📈 Trend Göstergeleri
        
        Trend göstergeleri, fiyat hareketinin yönünü ve gücünü ölçen teknik analiz araçlarıdır:
        
        1. **Hareketli Ortalamalar**
           - Fiyatların belirli bir dönemdeki ortalamasını gösterir
           - Trend yönünü ve güçlü destek/direnç seviyelerini belirler
           - Farklı periyotların kesişimleri alım-satım sinyali verir
        
        2. **MACD (Moving Average Convergence Divergence)**
           - İki farklı hareketli ortalamanın farkını kullanır
           - Trend değişimlerini ve momentumu gösterir
           - Sinyal çizgisi kesişimleri alım-satım fırsatı sunar
        
        3. **Bollinger Bantları**
           - Fiyat oynaklığını (volatilite) ölçer
           - Aşırı alım/satım bölgelerini gösterir
           - Trend sıkışma ve genişleme dönemlerini belirler
        """)
        
        # Örnek trend göstergeleri grafiği
        dates = pd.date_range(start='2024-01-01', periods=100)
        price = np.cumsum(np.random.normal(0, 1, 100)) + 100
        sma_20 = pd.Series(price).rolling(window=20).mean()
        sma_50 = pd.Series(price).rolling(window=50).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=price, name='Fiyat'))
        fig.add_trace(go.Scatter(x=dates, y=sma_20, name='20 Günlük HO'))
        fig.add_trace(go.Scatter(x=dates, y=sma_50, name='50 Günlük HO'))
        fig.update_layout(title='Hareketli Ortalamalar ile Trend Analizi',
                        xaxis_title='Tarih',
                        yaxis_title='Fiyat')
        st.plotly_chart(fig, use_container_width=True)

    elif topic == "Momentum Göstergeleri":
        st.markdown("""
        ### 🔄 Momentum Göstergeleri
        
        Momentum göstergeleri, fiyat hareketinin hızını ve gücünü ölçen teknik analiz araçlarıdır:
        
        1. **RSI (Göreceli Güç Endeksi)**
           - 0-100 arasında değer alır
           - Aşırı alım (70+) ve aşırı satım (30-) seviyelerini gösterir
           - Fiyat momentumundaki değişimleri ölçer
        
        2. **Stokastik Osilatör**
           - Fiyatın belirli bir dönemdeki en yüksek ve en düşük seviyelere göre konumunu ölçer
           - Aşırı alım/satım bölgelerini belirler
           - Trend dönüş sinyalleri üretir
        
        3. **CCI (Emtia Kanal Endeksi)**
           - Fiyatın ortalamadan sapmasını ölçer
           - Trend gücünü ve potansiyel dönüş noktalarını gösterir
           - Aşırı alım/satım seviyelerini belirler
        """)
        
        # Örnek momentum göstergesi grafiği
        dates = pd.date_range(start='2024-01-01', periods=100)
        price = np.cumsum(np.random.normal(0, 1, 100)) + 100
        rsi = np.random.uniform(30, 70, 100)  # Basit RSI simülasyonu
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=rsi, name='RSI'))
        fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Aşırı Alım")
        fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Aşırı Satım")
        fig.update_layout(title='RSI Momentum Göstergesi',
                        xaxis_title='Tarih',
                        yaxis_title='RSI Değeri')
        st.plotly_chart(fig, use_container_width=True)
        
    else:  # Hacim Göstergeleri
        st.markdown("""
        ### 📊 Hacim Göstergeleri
        
        Hacim göstergeleri, işlem hacmini ve fiyat-hacim ilişkisini analiz eden teknik analiz araçlarıdır:
        
        1. **OBV (On-Balance Volume)**
           - Fiyat değişimleriyle birlikte hacim akışını ölçer
           - Trend doğrulaması yapar
           - Olası trend değişimlerini önceden gösterebilir
        
        2. **Money Flow Index**
           - Fiyat ve hacim verilerini birlikte kullanır
           - Para akışının yönünü gösterir
           - Aşırı alım/satım seviyeleri sunar
        
        3. **Volume Price Trend**
           - Hacim ve fiyat trendlerini karşılaştırır
           - Trend gücünü doğrular
           - Olası trend dönüşlerini işaret eder
        """)
        
        # Örnek hacim göstergesi grafiği
        dates = pd.date_range(start='2024-01-01', periods=100)
        price = np.cumsum(np.random.normal(0, 1, 100)) + 100
        volume = np.random.randint(1000, 10000, 100)
        obv = np.cumsum(np.where(np.diff(price, prepend=price[0]) > 0, volume, -volume))
        
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                          vertical_spacing=0.03,
                          subplot_titles=('Fiyat ve Hacim', 'OBV (On-Balance Volume)'))
        
        fig.add_trace(go.Scatter(x=dates, y=price, name='Fiyat'), row=1, col=1)
        fig.add_trace(go.Bar(x=dates, y=volume, name='Hacim'), row=1, col=1)
        fig.add_trace(go.Scatter(x=dates, y=obv, name='OBV'), row=2, col=1)
        
        fig.update_layout(height=800, title='Hacim Analizi ve OBV Göstergesi')
        st.plotly_chart(fig, use_container_width=True)