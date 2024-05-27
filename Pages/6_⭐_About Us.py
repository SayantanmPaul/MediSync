import streamlit as st
from PIL import Image

st.title("Overview")
st.header("Insights into Our Endeavor")

# Multiline text using triple-quotes
description_text = """
Embark on a Data Odyssey: Unleashing the Power of Analysis, 
Visualization, NLP, and Machine Learning in the 
Exploration of Pharmaceutical Insights
"""

st.text(description_text)


st.header("Contributors")

# Define the columns
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])

with col1:
    #Display Images
    # import Image from pillow to open images
    img = Image.open("Pages/Images/photo_deblina1.png")

    # display image using streamlit
    # width is used to set the width of an image
    st.image(img, width=100)

    st.text("Deblina Banerjee")

    # Add contributor information
    contributor_info = """ 
     [LinkedIn](https://www.linkedin.com/in/deblina-banerjee-231290206/)  [GitHub](https://github.com/DEBLINA29)
    """

    st.markdown(contributor_info)

with col2:
    # Display Images
    # import Image from pillow to open images
    img = Image.open("Pages/Images/photo_shreya.png")

    # display image using streamlit
    # width is used to set the width of an image
    st.image(img, width=100)

    st.text("Shreya Dubey")

    # Add contributor information
    contributor_info = """
     [LinkedIn](https://www.linkedin.com/search/results/all/?fetchDeterministicClustersOnly=true&heroEntityKey=urn%3Ali%3Afsd_profile%3AACoAADowDyMBdP7xDdydkk5w_mepghHG5-MCpSc&keywords=shreya%20dubey&origin=RICH_QUERY_SUGGESTION&position=0&searchId=f116f3fb-4699-4a06-9ae9-cfca8cdd4252&sid=VX-&spellCorrectionEnabled=false)  [GitHub](https://github.com/ShreyaDubey1105)
    """

    st.markdown(contributor_info)


with col3:
    # Display Images
    # import Image from pillow to open images
    img = Image.open("Pages/Images/photo_sayantan.png")

    # display image using streamlit
    # width is used to set the width of an image
    st.image(img, width=100)

    st.text("Sayantan Paul")

    # Add contributor information
    contributor_info = """
     [LinkedIn](https://www.linkedin.com/search/results/all/?fetchDeterministicClustersOnly=true&heroEntityKey=urn%3Ali%3Afsd_profile%3AACoAADveaOcBKdOjcq1y3HuDK40d_xFFtTT7ZVc&keywords=sayantan%20paul&origin=RICH_QUERY_SUGGESTION&position=2&searchId=027e811c-4cd6-4706-ac21-ff5b3d6a1eca&sid=ZLf&spellCorrectionEnabled=false)  [GitHub](https://github.com/SayantanmPaul)
    """

    st.markdown(contributor_info)


with col4:
    # Display Images
    # import Image from pillow to open images
    img = Image.open("Pages/Images/photo_avani.png")

    # display image using streamlit
    # width is used to set the width of an image
    st.image(img, width=100)

    st.text("Avani Sethia")

    # Add contributor information
    contributor_info = """
     [LinkedIn](https://www.linkedin.com/in/avani-sethia-84b64621b?trk=contact-info)  [GitHub](https://github.com/sia1504)
    """

    st.markdown(contributor_info)


with col5:
    # Display Images
    # import Image from pillow to open images
    img = Image.open("Pages/Images/photo_durgesh.png")

    # display image using streamlit
    # width is used to set the width of an image
    st.image(img, width=100)

    st.text("Durgesh Gupta")

    # Add contributor information
    contributor_info = """
     [LinkedIn](https://www.linkedin.com/search/results/all/?fetchDeterministicClustersOnly=true&heroEntityKey=urn%3Ali%3Afsd_profile%3AACoAAB2RnKgBUs_jmkXa-52GyUBWcUElTz4RUWU&keywords=durgesh%20gupta&origin=RICH_QUERY_SUGGESTION&position=0&searchId=5d613db7-d95e-4781-a77e-88c7186435b2&sid=5!i&spellCorrectionEnabled=false)  [GitHub](https://github.com/Durgesh6969)
    """

    st.markdown(contributor_info)


with col6:
    # Display Images
    # import Image from pillow to open images
    img = Image.open("Pages/Images/photo_tanisha.png")

    # display image using streamlit
    # width is used to set the width of an image
    st.image(img, width=100)

    st.text("Tanisha Gupta")

    # Add contributor information
    contributor_info = """
    [LinkedIn](https://www.linkedin.com/in/tanisha-gupta-a81158210)  [GitHub](https://github.com/tanishagupta0811)
    """

    st.markdown(contributor_info)