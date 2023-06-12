# Making a streamlit app
import streamlit as st
import pandas as pd
import os
import sys


def dashboard_streamlit():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

    apptitle = 'Trial Dashboard'
    st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")
    st.title('Trial Dashboard')

    # Load data
    df = pd.read_excel('Test_data.xlsx', header=0, index_col=0)
    
    # Get column names and datatypes as a dictionary
    columns = df.columns.tolist()
    # columns.remove('Unnamed: 0')
    datatypes = df.dtypes.tolist()
    dtype_dict = dict(zip(columns, datatypes))
    # col_dict = dict(zip(columns, datatypes))

    # Dictionary of columns and their respective checkbox values
    col_dict = {}

    # Checkboxes for all columns in columns list
    st.sidebar.subheader('Feasibility Criteria')
    for col in columns:
        col_dict[col] = st.sidebar.checkbox(col, value=True)

    # A number input for numeric columns in dtype_dict
    numeric_dict_filtered = {}   # Empty dictionary to store numeric column filtering values
    numeric_dict = {}   # Empty dictionary to store all numeric column values
    st.sidebar.subheader('Numeric Criteria')

    # Collecting the numeric values into a dictionary
    for key, value in dtype_dict.items():
        if value == 'int64' or value == 'float64':
            if col_dict[key] == True:
                numeric_dict_filtered[key] = st.sidebar.number_input(key, value=0)

    # A multiselect for non-numeric columns in dtype_dict which have value = True in col_dict
    non_numeric_dict_filtered = {}   # Empty dictionary to store non-numeric column filtering values
    non_numeric_dic = {}   # Empty dictionary to store all non-numeric column values
    st.sidebar.subheader('Non-Numeric Criteria')
    for key, value in dtype_dict.items():
        if value == 'object':
            if col_dict[key] == True:
                non_numeric_dict_filtered[key] = st.sidebar.multiselect(key, options=df[key].unique().tolist())


    # Select all columns with value=False for plotting
    columns_plotting = [key for key, value in col_dict.items() if value == False]

    # # Filter dataframe based on checkbox values
    # df_display = df[columns_plotting]

    # We will define two different dataframes, one that will be used for plotting and one that will be used for displaying
    # the numeric columns that are being considered for plotting
    # for plotting
    df_plotting = df.copy()   # Copying the original dataframe, to avoid a local unbound error if
    # numeric_dict_filtered is empty
    for key, value in numeric_dict_filtered.items():
        df_plotting = df.loc[(df[key] > value), :]


    # for plotting
    # for key, value in numeric_dict_filtered.items():
    #     df_showing_plot = df.loc[(df[key] > value) & (df[key] < 1E5), numeric_dict_filtered.keys()]
    keys_shown = [key for key in col_dict.keys() if col_dict[key] == False and dtype_dict[key] == 'int64' or dtype_dict[key] == 'float64']
    df_showing_plot = df[keys_shown]

    # Original data frame
    st.subheader('Original Data Frame')
    st.write(df.replace(99999, 'NA'))

    # # Data Frame Being Considered for Plotting
    # st.subheader('Data Frame Being Considered for Plotting')
    # st.write(df_display)

    # Plotting
    st.subheader('Plotting')
    try:
        st.write(df_showing_plot.replace(99999, 'NA'))
    except UnboundLocalError:
        st.write('No numeric columns selected')

    # Bar plot of numeric columns in df_plotting
    st.subheader('Bar Plot of Numeric Columns')
    try:
        for key, value in dtype_dict.items():
            if value == 'int64' or value == 'float64':
                if col_dict[key] == False:
                    # We're dropping the rows with value 99999 because they are just fillers
                    st.bar_chart(df_plotting[key].drop(df_plotting[df_plotting[key] == 99999].index, inplace=False))
    except UnboundLocalError:
        st.write('No numeric columns selected')


    # Define df_write by filtering out the columns not in non_numeric_dict_filtered
    df_write = df[[key for key in df.columns if key not in numeric_dict_filtered.keys()]]

    # For each list in non_numeric_dict_filtered, filter df_write by the values in that list
    for key, value in non_numeric_dict_filtered.items():
        df_write = df_write[df_write[key].isin(value)]

    # For each non-numeric column in df_plotting, for each unique value, list the indices that have that value
    st.subheader('List of non-numeric values')
    try:
        for key, value in non_numeric_dict_filtered.items():
            st.subheader(key)

            for unique_value in df_write[key].unique().tolist():
                options_with_value = ', '.join(df_write.index[df_write[key] == unique_value].tolist())
                st.write(f"**{unique_value}**" + ": " + options_with_value)

    except UnboundLocalError:
        st.write('No non-numeric columns selected')


if __name__ == '__main__':
    dashboard_streamlit()



