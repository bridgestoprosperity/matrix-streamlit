import pandas as pd
from functools import partial
from collections import namedtuple
import textwrap

link = namedtuple('link', ['name', 'link'])    # Will be used to store links in a named tuple

def break_at_semicolon(input_string):
    if isinstance(input_string, float):
        return input_string
    else:
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

def break_make_list(input_string):
    '''Break the input string at the semicolon and join elements so that the resulting string in markdown
    format is a bulleted list'''
    output_string = break_at_semicolon(input_string)
    if isinstance(output_string, float) or len(output_string) == 1:
        return input_string
    else:
        output_string = [f'- {strng}' for strng in output_string]
        return '\n'.join(output_string)

def markdown_list_from_dataframe(input_dataframe):
    for col in input_dataframe.columns:
        if input_dataframe[col].dtype == 'object':
            input_dataframe[col] = input_dataframe[col].apply(break_make_list)
    return input_dataframe


def generate_bulleted_list(items):
    '''Generate a bulleted html list from a list of items'''
    if isinstance(items, list):
        html = "<ul>\n"
        for item in items:
            html += "<li>{}</li>\n".format(item)
        html += "</ul>"
        return html
    else:
        return items

def convert_dataframe_to_plotly_table(input_dataframe, column_name):
    items = input_dataframe[column_name].tolist()
    bullet_list = "<ul>{}</ul>".format("".join(["<li>{}</li>".format(item) for item in items]))
    table_data = [[bullet_list]]
    return table_data

def replace_text_with_bulleted_list(input_dataframe):
    '''Replace text with bulleted list in every element of the dataframe'''
    for col in input_dataframe.columns:
        if input_dataframe[col].dtype == 'object':
            input_dataframe[col] = input_dataframe[col].str.split(';').apply(generate_bulleted_list)
    return input_dataframe

def replace_semicolon_with_newline(input_dataframe):
    '''Replace semicolon with newline in every element of the dataframe
    that is a string'''
    for col in input_dataframe.columns:
        if input_dataframe[col].dtype == 'object':
            input_dataframe[col] = input_dataframe[col].replace(';', '\n\n', regex=True)
    return input_dataframe

def replace_semicolon_with_linebreak(input_dataframe):
    '''Replace semicolon with linebreak in every element of the dataframe
    that is a string'''
    for col in input_dataframe.columns:
        if input_dataframe[col].dtype == 'object':
            input_dataframe[col] = input_dataframe[col].replace(';', '<br> -', regex=True)
    return input_dataframe

def make_first_column_bold(input_dataframe):
    '''Make the first column bold'''
    input_dataframe.iloc[:, 0] = input_dataframe.iloc[:, 0].apply(lambda x: f'<b>{x}</b>')
    return input_dataframe

def add_newline(string):
    '''Add a newline to every second word in the string'''
    words = string.split()  # Split the string into words
    new_string = ' '.join(words[i] if (i + 1) % 2 != 0 else words[i] + '\n' for i in range(len(words)))
    return new_string


def add_newline_to_df_columns(input_dataframe):
    '''Add a newline to every second word in the dataframe column names'''
    input_dataframe.columns = [add_newline(col) for col in input_dataframe.columns]
    return input_dataframe

def wrap_dataframe_column_names(input_dataframe):
    '''Apply textwrap to the dataframe column names'''
    input_dataframe.columns = [textwrap.fill(col, width=10) for col in input_dataframe.columns]
    return input_dataframe

def wrap_dataframe_column_values(input_dataframe):
    '''Apply textwrap to the dataframe column values'''
    wrap_function = partial(textwrap.fill, break_on_hyphens=False, width=25)
    for col in input_dataframe.columns:
        if input_dataframe[col].dtype == 'object':
            input_dataframe[col] = input_dataframe[col].apply(wrap_function).replace('\n', '<br>', regex=True)
    return input_dataframe

def add_linebreak(string):
    '''Add a linebreak every 4 words in the string'''
    words = string.split()  # Split the string into words
    new_string = ' '.join(words[i] if (i + 1) % 4 != 0 else words[i] + '<br>' for i in range(len(words)))
    return new_string

def add_linebreak_to_dataframe_column_values(input_dataframe):
    '''Adds a linebreak every 4 words in the dataframe column values'''
    for col in input_dataframe.columns:
        if input_dataframe[col].dtype == 'object':
            input_dataframe[col] = input_dataframe[col].apply(add_linebreak)
    return input_dataframe

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
        # We use the boolean index to filter the dataframe, selecting only columns that met any of the feasibility
        # criteria
        df_out = df.loc[:, filter_df.any(axis=1)]
        return df_out

def break_and_concatenate(strings_list):
    '''Break the strings in the list at the semicolon and concatenate them into a single list'''
    concatenated_list = []
    for string in strings_list:
        substrings = string.split(";")
        concatenated_list.extend(substrings)
    return concatenated_list

def break_and_get_unique(df):
    '''Break the strings in the dataframe at the semicolon and return a list of unique values'''
    concatenated_list = []
    for col in df.columns:
        if df[col].dtype == 'object':
            concatenated_list.extend(break_and_concatenate(df[col]))
            # Remove whitespace
            concatenated_list = [string.strip() for string in concatenated_list]
    return list(set(concatenated_list))

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

def round_non_nan(value, decimals=1):
    """
    Custom function to round off non-NaN values.
    """
    if pd.notna(value) and isinstance(value, float):
        return round(value, decimals)
    else:
        return value



if __name__ == '__main__':
    print(break_at_semicolon("1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20"))
    print(replace_span_and_eval("1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+span+17+18+19+20", 16))
    print(replace_span_and_eval(remove_units("span+17m+18+19+20"), 16))
    print(read_links("IT Transport Guide|https://drive.google.com/file/d/11ptavSSCDtjiI6auCW3FEfp-auJEVloY/view?usp=drive_link"))
    print([read_links(link) for link in break_at_semicolon("1|2; 3|4")])


