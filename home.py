import streamlit as st
import pandas as pd
import time
import random

# Set up the Streamlit page configuration and hide the menu, footer, and header
st.set_page_config(page_icon="📜", page_title="N|uu", layout="centered")

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

def stream_data():
    for word in TEXT.split(" "):
        yield word + " "
        time.sleep(0.05)


st.title("📜 N|uu")
st.write("&nbsp;")

st.sidebar.title("📜 N|uu")
st.sidebar.write("&nbsp;")

on = st.toggle("I want this text in English 👀")
st.write("&nbsp;")

if on:
    TEXT = """
    The text you saw was from a randomly chosen extinct language. You just had a very small experience of how it feels when your language is invisible on the Internet.

    The Internet is a very unfair representation of human linguistic diversity. `N|uu` is an attempt to make these stark inequalities visible by quantifying internet representation for all languages scripted by humans.

    Calculating representation scores now... 
    """
    st.warning("`N|uu` is named after a nearly-extinct language with only [one living speaker left](https://youtu.be/WFH4h75X2j8?si=lnYAOr7zCGwA4H4e).")
    st.write_stream(stream_data)
    st.write("&nbsp;")

    df = pd.read_csv("./data/df_clean.csv").drop(columns=['Iso639', 'Country Code', 'Primary Country'])
    df['Representation Score'] = df['Representation Score'].round(2)
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    st.sidebar.info("**Supported By** \n\n 🌱 Amsterdam School of Communication Research \n\n 🌱 Social and Behavioural Data Science Centre, University of Amsterdam \n\n Reach out to our [team](https://theinvisiblelab.org/team) for feedback and/or collaboration.")

else:
    # List of 10 elements
    elements = [
        "ⲛⲓⲛⲧⲉⲣⲛⲉⲧ ⲉⲧⲁⲓ ⲙⲁⲣⲉϥⲧⲟⲩⲉϣⲧⲉ ⲉⲩⲣⲉϥϩⲓⲧⲣⲉ ⲙⲉⲧⲛⲓⲙⲉ ⲙⲛ ⲛⲓⲗⲁⲗⲉ ⲛⲉⲛⲉϩ. ⲛⲟⲩ ⲛⲟⲩ ⲡⲉ ⲛⲉⲩⲧⲉⲛⲧⲟⲩⲧⲉ ⲙⲛ ⲛⲓⲃⲉⲗⲁⲣⲓⲟⲥ ⲙⲛ ⲛⲉⲙⲉⲧⲣⲉ ⲛⲓⲉⲗⲉⲛⲅⲟⲥ ⲉⲣⲟⲩⲥⲉⲥⲧⲉⲛ ⲉⲛⲉϩ ⲉⲧⲟⲩⲁⲧⲟⲩⲧⲉ.",
        "Internet je un'vara injusta representazione de la diversità linguistica umana. N|uu je un'prova per far queste ineguaglianze visibili per tute le lingue scrite da l'omini.",
        "អ៊ីនធឺណិតគឺជាតំណាងមិនសមស្របណាស់នៃភាពចម្រុះភាសារបស់មនុស្ស។ N|uu គឺជាការប្រឹងប្រែងមួយដើម្បីធ្វើឱ្យមើលឃើញនូវភាពមិនសមស្របយ៉ាងច្បាស់សម្រាប់ភាសាទាំងអស់ដែលត្រូវបានសរសេរដោយមនុស្ស។",
        "Интернет киһи тилин түрлүүлүгүн салгыыҥҥы көрдөрөр. Н|уу киһи билигинэ суруллубут тыллар үөрэнэр кыахпытын көрдөрөр кыах суолуга.",
        "In tlahcuiloliztli ipan tonacayotl tequixpohua huehca in ixquich tlahtolli tequixpohua. In N|uu ce tlayecoliztli in tlahtollotl in tequixpohua in ixquich tlahtolli in huel itechpa tlahtohqueh.",
        "El Internet es una representación muy injusta de la diversidad lingüística humana. N|uu es un intento de hacer visibles estas marcadas desigualdades para todos los idiomas escritos por humanos.",
        "インターネットは人間の言語多様性を非常に不公平に表しています。ン|ウは、人間によって書かれたすべての言語に対するこれらの顕著な不平等を可視化する試みです。",
        "𐌄𐌍𐌕𐌉𐌍𐌄𐌓𐌄𐌕 𐌅𐌀𐌋𐌄𐌉𐌉𐌓𐌄𐌔 𐌑𐌀𐌓𐌄𐌕𐌀𐌉𐌌𐌄 𐌄𐌋𐌀𐌔𐌕𐌄𐌑𐌉𐌉 𐌋𐌀𐌍𐌂𐌖𐌉𐌔𐌀𐌉 𐌃𐌀𐌋𐌀𐌍𐌂𐌖𐌉𐌔𐌀𐌉. 𐌍𐌖𐌖 𐌀𐌉𐌌𐌄𐌕𐌑𐌀𐌉 𐌉𐌍𐌀𐌋𐌄𐌍𐌂𐌖𐌉𐌔𐌉𐌉 𐌉𐌖𐌔𐌉𐌂𐌄𐌉 𐌀𐌋𐌋𐌄𐌋𐌄𐌑𐌉𐌋𐌄𐌑𐌉𐌉 𐌅𐌀𐌋𐌄𐌉𐌉 𐌕𐌉𐌉𐌌𐌄𐌑𐌉𐌉𐌔."
    ]

    # Randomly choose one element from the list
    TEXT = random.choice(elements)

    st.write_stream(stream_data)