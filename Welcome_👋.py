import streamlit as st
import base64

st.set_page_config(page_title='Welcome',
                   page_icon="👋")


st.title('Rural Infrastructure Matrix')

st.markdown('''\n\nWelcome to the Rural Infrastructure Matrix. This tool is designed to help you identify the most appropriate
            crossing structure for your project. The tool was developed by Bridges to Prosperity, who are doing lots of
            work to improve rural access in developing countries. You can find out more about them
            [here](https://bridgestoprosperity.org/).''')

# @st.cache(allow_output_mutation=True)
# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()
#
#
# def set_png_as_page_bg(png_file):
#     bin_str = get_base64_of_bin_file(png_file)
#     page_bg_img = '''
#     <style>
#     .stApp {
#     background-image: url("data:image/png;base64,%s");
#     background-size: cover;
#     }
#     </style>
#     ''' % bin_str
#
#     st.markdown(page_bg_img, unsafe_allow_html=True)
#     return
#
#
# set_png_as_page_bg(r'C:\Users\mwendwa.kiko\Documents\Personal_Kiko\E4C_Internship\Other Images\Helvetas_Bridge_clipped.png')
#
# # page_bg_img = '''
# # <style>
# # body {
# # background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
# # background-size: cover;
# # }
# # </style>
# # '''
# #
# # st.markdown(page_bg_img, unsafe_allow_html=True)
#
# col1, col2 = st.columns(2)
# with col1:
#     st.markdown('''\n\nWelcome to the Rural Infrastructure Matrix. This tool is designed to help you identify the most appropriate
#             crossing structure for your project. The tool was developed by Bridges to Prosperity, who are doing lots of
#             work to improve rural access in developing countries. You can find out more about them
#             [here](https://bridgestoprosperity.org/).''')
#



