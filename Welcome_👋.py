import streamlit as st
import base64

st.set_page_config(page_title='Welcome',
                   page_icon="👋")


st.title('Rural Infrastructure Matrix')

# st.markdown('''\n\nWelcome to the Rural Infrastructure Matrix. This tool is designed to help you identify the most appropriate
#             crossing structure for your project. The tool was developed by Bridges to Prosperity, who are doing lots of
#             work to improve rural access in developing countries. You can find out more about them
#             [here](https://bridgestoprosperity.org/).''')

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

# # When running it locally
# set_png_as_page_bg(r'C:\Users\mwendwa.kiko\Documents\Personal_Kiko\E4C_Internship\Other Images\Helvetas_Bridge_clipped.png')
# When running it on the server
set_png_as_page_bg('Helvetas_Bridge_clipped.png')

# page_bg_img = '''
# <style>
# body {
# background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
# background-size: cover;
# }
# </style>
# '''
#
# st.markdown(page_bg_img, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    # st.markdown('''\n\nWelcome to the Rural Infrastructure Matrix. This tool is designed to help you identify the most appropriate
    #         crossing structure for your project. The tool was developed by Bridges to Prosperity, who are doing lots of
    #         work to improve rural access in developing countries. You can find out more about them
    #         [here](https://bridgestoprosperity.org/). \n\nYou can find information on how to use the tool
    #         [here](https://www.youtube.com/watch?v=WTWmrwjQzog).''')
    st.markdown(
        """<head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rural Infrastructure Matrix</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: justify;
                margin: 20px;
                color: black;
                }
            </style>
        </head>
        <body>
            <p>Welcome to the Rural Infrastructure Matrix. This tool is designed to help you identify the most appropriate 
            crossing structure for your project. The tool was developed by Bridges to Prosperity, who are doing lots of 
            work to improve rural access in developing countries. You can find out more about them 
            <a href="https://bridgestoprosperity.org/">here</a>.</p>
            <p>You can find information on how to use the tool <a href="https://www.youtube.com/watch?v=WTWmrwjQzog">here</a>.</p>
            <p>Kindly leave a review of the tool as well
            <a href="https://docs.google.com/forms/d/e/1FAIpQLSf-yd2ulF1T4QOhDv7XQVegaqXe7tawajWmuoj23s4qlDDxtA/viewform?usp=sf_link">here</a>.</p>
        </body>
</html>""", unsafe_allow_html=True)

    ## Code for adding the survey link
    # <p>Kindly leave a review of the tool as well
    # <a href="https://docs.google.com/forms/d/e/1FAIpQLSf-yd2ulF1T4QOhDv7XQVegaqXe7tawajWmuoj23s4qlDDxtA/viewform?usp=sf_link">here</a>.</p>






