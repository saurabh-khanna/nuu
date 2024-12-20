import streamlit as st
import pandas as pd
import time
import random
import pydeck as pdk
import re

# Set up the Streamlit page configuration and hide the menu, footer, and header
st.set_page_config(page_icon="📜", page_title="Lost Without Translation", layout="wide")

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Function for streaming text
def stream_data():
    for word in TEXT.split(" "):
        yield word + " "
        time.sleep(0.05)

st.title("📜 Lost Without Translation")
st.write("&nbsp;")

st.sidebar.title("📜 Lost Without Translation")
st.sidebar.write("&nbsp;")
placeholder = st.sidebar.empty()

on = st.toggle("I want this text in English 😕")
st.write("&nbsp;")

if on:

    placeholder.empty()
    
    TEXT = """
    The text you saw was from a randomly chosen extinct language. You just had a very small experience of how it feels when your language is invisible on the internet.

    The internet is an extremely unfair representation of human linguistic diversity. **Lost Without Translation** is an attempt to make these stark inequalities visible by quantifying online visibility for all languages scripted by humans.
    
    Calculating visibility scores [range 0-100] for all languages now... 
    """
    st.write_stream(stream_data)

    with st.expander("How are visibility scores calculated?"):
        st.write(
            """
            We intend to assess the online visibility of all text-based human languages, considering both their human usage and their digital presence. By combining data from Ethnologue and Common Crawl, we can approximate the extent to which languages are represented on the web relative to their real-world usage.

            **Data Sources**

            - [Ethnologue](https://www.ethnologue.com/): Provides comprehensive information on more than 7000 living human languages, including the number of L1 (first language) speakers.
            - [Common Crawl](https://commoncrawl.org/): A massive dataset of monthly web crawls, offering insights into the distribution of languages on the internet.

            **Metric Definitions**

            We define the *visibility* of a language $L$, denoted by $V_L$, as the percentile rank of its *visibility index*, $I_L$. 

            The visibility index, $I_L$, in turn is calculated as follows:
            """
        )

        st.latex(r'''I_L = \frac{P_L}{S_L}''')

        st.write(
            """
            where $P_L$ is the proportion of web pages in Common Crawl written in language $L$, and $S_L$ is the proportion of human population that speaks language $L$ as their first language.

            The percentile rank of each language's visibility index, $V_L$ is calculated as follows:
            """
        )

        st.latex(r'''V_L = \frac{\text{Number of languages with } I_L' \leq I_L}{\text{Total number of languages}} \times 100''')
        
        st.write(
            """
            where $I_L'$ is the visibility index of another language.

            A higher visibility score indicates that a language is more prominent online relative to its number of L1 speakers. This could suggest factors such as:

            - Strong internet penetration in regions where the language is spoken
            - Active online communities and digital content creation
            - Government or institutional support for digital initiatives

            Conversely, a lower score might imply:

            - Limited internet access in language-speaking regions
            - Lower digital literacy rates
            - Lack of government or institutional support for digital initiatives

            By quantifying the online visibility of languages, we can gain valuable insights into the digital divide and the potential challenges faced by language communities in the digital age. This metric can be used to inform language policy, digital inclusion initiatives, and research on language technology.

            We are always looking for ways to improve our approach. Please reach out to [saurabh.khanna@uva.nl](mailto:saurabh.khanna@uva.nl) with feedback and/or questions.
            """
        )

    st.write("&nbsp;")
    
    # Load and prepare data for the map
    df = pd.read_csv("./data/df_clean.csv").drop(columns=['Iso639', 'Country Code', 'Primary Country'])
    df['Visibility'] = df['Visibility'].round(2)
    df = df.dropna(subset=['Lat', 'Lon'])
    df = df.rename(columns={'Lat': 'latitude', 'Lon': 'longitude'})
    df['Langlabel'] = df['Language'].apply(lambda x: re.sub(r"<.*?>", "", x))
    
    # Generate colors based on visibility
    df['color'] = df['Visibility'].apply(lambda x: [255 - int(x * 2.55), int(x * 2.55), 0])

    with st.container(border=True):
        # Print the map with tooltips
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=0,
                longitude=0,
                zoom=1.5,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    get_radius=50000,
                    get_color='color',
                    stroke_color=[0, 0, 0], 
                    fille=True,
                    pickable=True,  # Enables tooltip display on hover
                ),
            ],
            tooltip={"text": "Language: {Langlabel}\nVisibility: {Visibility}/100"}  # Tooltip text
        ))

    # Display the table without latitude and longitude columns
    df = df.drop(columns=['latitude', 'longitude', 'color', 'Langlabel'])
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    st.sidebar.info("**Supported By** \n\n 🌱 Amsterdam School of Communication Research \n\n 🌱 Social and Behavioural Data Science Centre, University of Amsterdam \n\n Reach out to our [team](https://theinvisiblelab.org/team) for feedback and/or collaboration.")

else:
    extinct_langs = [
        "ⲛⲓⲛⲧⲉⲣⲛⲉⲧ ⲉⲧⲁⲓ ⲙⲁⲣⲉϥⲧⲟⲩⲉϣⲧⲉ ⲉⲩⲣⲉϥϩⲓⲧⲣⲉ ⲙⲉⲧⲛⲓⲙⲉ ⲙⲛ ⲛⲓⲗⲁⲗⲉ ⲛⲉⲛⲉϩ. ⲛⲟⲩ ⲛⲟⲩ ⲡⲉ ⲛⲉⲩⲧⲉⲛⲧⲟⲩⲧⲉ ⲙⲛ ⲛⲓⲃⲉⲗⲁⲣⲓⲟⲥ ⲙⲛ ⲛⲉⲙⲉⲧⲣⲉ ⲛⲓⲉⲗⲉⲛⲅⲟⲥ ⲉⲣⲟⲩⲥⲉⲥⲧⲉⲛ ⲉⲛⲉϩ ⲉⲧⲟⲩⲁⲧⲟⲩⲧⲉ.",
        "Internet je un'vara injusta representazione de la diversità linguistica umana. N|uu je un'prova per far queste ineguaglianze visibili per tute le lingue scrite da l'omini.",
        "អ៊ីនធឺណិតគឺជាតំណាងមិនសមស្របណាស់នៃភាពចម្រុះភាសារបស់មនុស្ស។ N|uu គឺជាការប្រឹងប្រែងមួយដើម្បីធ្វើឱ្យមើលឃើញនូវភាពមិនសមស្របយ៉ាងច្បាស់សម្រាប់ភាសាទាំងអស់ដែលត្រូវបានសរសេរដោយមនុស្ស។",
        "Интернет киһи тилин түрлүүлүгүн салгыыҥҥы көрдөрөр. Н|уу киһи билигинэ суруллубут тыллар үөрэнэр кыахпытын көрдөрөр кыах суолуга.",
        "In tlahcuiloliztli ipan tonacayotl tequixpohua huehca in ixquich tlahtolli tequixpohua. In N|uu ce tlayecoliztli in tlahtollotl in tequixpohua in ixquich tlahtolli in huel itechpa tlahtohqueh.",
        "インターネットは人間の言語多様性を非常に不公平に表しています。ン|ウは、人間によって書かれたすべての言語に対するこれらの顕著な不平等を可視化する試みです。",
        "𐌄𐌍𐌕𐌉𐌍𐌄𐌓𐌄𐌕 𐌅𐌀𐌋𐌄𐌉𐌉𐌓𐌄𐌔 𐌑𐌀𐌓𐌄𐌕𐌀𐌉𐌌𐌄 𐌄𐌋𐌀𐌔𐌕𐌄𐌑𐌉𐌉 𐌋𐌀𐌍𐌂𐌖𐌉𐌔𐌀𐌉 𐌃𐌀𐌋𐌀𐌍𐌂𐌖𐌉𐌔𐌀𐌉. 𐌍𐌖𐌖 𐌀𐌉𐌌𐌄𐌕𐌑𐌀𐌉 𐌉𐌍𐌀𐌋𐌄𐌍𐌂𐌖𐌉𐌔𐌉𐌉 𐌉𐌖𐌔𐌉𐌂𐌄𐌉 𐌀𐌋𐌋𐌄𐌋𐌄𐌑𐌉𐌋𐌄𐌑𐌉𐌉 𐌅𐌀𐌋𐌄𐌉𐌉 𐌕𐌉𐌉𐌌𐌄𐌑𐌉𐌉𐌔."
    ]

    # Randomly choose one element from the list
    TEXT = random.choice(extinct_langs)

    st.write_stream(stream_data)
    placeholder.image("confused.gif")

