import pandas as pd
from collections import namedtuple

link = namedtuple('link', ['name', 'link'])    # Will be used to store links in a named tuple

def break_at_semicolon(input_string):
    output_string = input_string.split(";")
    output_string = [strng.strip() for strng in output_string]
    return output_string

def break_at_pipe(input_string):
    output_string = input_string.split("|")
    output_string = [strng.strip() for strng in output_string]
    return output_string

def markdown_string_of_links(input_string):
    """Takes in an input string, and runs break_at_semicolon and break_at_pipe on it, then returns a named tuple"""
    """with the first element being the name of the link and the second element being the link itself"""
    output_string = break_at_semicolon(input_string)
    output_string = [break_at_pipe(strng) for strng in output_string]
    # Output is a list of markdown link strings
    output_list = [f'[{strng[0]}]({strng[1]})' for strng in output_string]
    return output_list






def replace_span_and_eval(input_string, eval_value):
    '''Replace 'span' with eval_value in the input_string and run eval on it'''
    return eval(input_string.replace('span', str(eval_value)))


def remove_units(input_string):
    '''Remove units from input_string'''
    return input_string.replace('kg', '').replace('m', '')

def read_links(input_string):
    '''Bring input string at the pipe value and return a dictionary, where the key is what's before the pipe and the
    value is what's after the pipe'''
    links = input_string.split('|')
    return {links[0]: links[1]}

def make_regex(input_list):
    '''Make a regex out of a list of strings'''
    return '|'.join(input_list)

def check_strings_in_series(string_list, series):
    for string in string_list:
        if any(string in value for value in series):
            return True
    return False

def check_strings_in_df(non_numeric_criteria, df):
    """This function takes in a dictionary of non-numeric criteria and a dataframe and returns a filtered dataframe
    with only the rows that contain all the non-numeric criteria that have been selected"""
    filter_df = pd.DataFrame()  # empty dataframe to store the boolean index from str.contains
    for key, value in non_numeric_criteria.items():
        for indx in df.index:
            if key == indx:
                for item in value:
                    # The heart of this method: we use str.contains to get a boolean index of the rows that contain
                    # the selected non-numeric criteria
                    contains = df.loc[indx, :].str.contains(item)
                    filter_df = pd.concat([filter_df, contains], axis=1)

    if filter_df.empty:
        return df
    else:
        # We use the boolean index to filter the dataframe, selecting only columns that met all the feasibility
        # criteria
        df_out = df.loc[:, filter_df.all(axis=1)]
        return df_out



def check_numeric_criteria(numeric_criteria, df):
    """This function takes in a dictionary of numeric criteria and a dataframe and returns a filtered dataframe
    with only the rows that contain all the numeric criteria that have been selected"""
    filter_df = pd.DataFrame()  # empty dataframe to store the boolean index from str.contains
    for key, value in numeric_criteria.items():
        for indx in df.index:
            if key == indx:
                # The heart of this method: we use > to get a boolean index of the rows that have a value greater
                # than the selected numeric criteria
                greater_than = df.loc[indx, :] > value
                filter_df = pd.concat([filter_df, greater_than], axis=1)
    if filter_df.empty:
        return df
    else:
        # We use the boolean index to filter the dataframe, selecting only columns that met all the feasibility
        # criteria
        df_out = df.loc[:, filter_df.all(axis=1)]
        return df_out

def barplot(df, title, x_label, y_label, x_axis_rotation=0, figsize=(10, 5)):
    """This function takes in a dataframe and a title and returns a barplot of the dataframe"""
    ax = df.plot(kind='bar', figsize=figsize)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticklabels(df.index, rotation=x_axis_rotation)
    return ax




if __name__ == '__main__':
    print(break_at_semicolon("1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20"))
    print(replace_span_and_eval("1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+span+17+18+19+20", 16))
    print(replace_span_and_eval(remove_units("span+17m+18+19+20"), 16))
    print(read_links("IT Transport Guide|https://drive.google.com/file/d/11ptavSSCDtjiI6auCW3FEfp-auJEVloY/view?usp=drive_link"))
    print([read_links(link) for link in break_at_semicolon("1|2; 3|4")])


