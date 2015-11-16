#!bin/python

import argparse

import numpy as np
import pandas as pd

def select_chair(df, area1, date, start_time, end_time,
                 area2=None, area3=None, mode="all"):

    """
    Select chairs by their area of expertise and whether they give a talk
    in the session they are supposed to chair.

    The input data comes in the form of a pandas DataFrame, which needs
    to have the following columns (for all participants) at the very least:

    "area_of_expertise_1": primary area of expertise
    "area_of_expertise_2": secondary area of expertise
    "area_of_expertise_3": tertiary area of expertise
    "session_date": the dates in which a given person gives a talk
    "session_start"; the start time for the session where the talk takes place
    "session_end"; the end time for the session where the talk takes place

    The precise format of the areas of expertise, session dates and times
    is not important, as long as the input of the query (i.e. that supplied
    to the keywords above) matches exactly that in the columns of the file,
    such that one can find it via a query!.


    Parameters
    ----------
    df: pandas.DataFrame
        DataFrame with the data. Rows are candidates, columns must at least
        be "area_of_expertise_1", "area_of_expertise_2", "area_of_expertise_3",
        "session_date", "session_start" and "session_end"

    area1: {string | iterable of strings}
        Either a string or a list of strings that match exactly one (or more)
        of the potential areas of expertise in the DataFrame

    area2: {string | iterable of strings}, optional
        Either a string or a list of strings that match exactly one (or more)
        of the potential areas of expertise in the DataFrame

    area3: {string | iterable of strings}, optional
        Either a string or a list of strings that match exactly one (or more)
        of the potential areas of expertise in the DataFrame

    date: string
        The date of the session in question where you do *not* want candidates
        who give a talk in that session. Format of this string must match
        entries in the "session_date" column of the DataFram

    start_time: string
        The start time of the session in question where you do *not* want
        candidates who give a talk in that session. Format of this string must
        match entries in the "session_date" column of the DataFram

    end_time: string
        The end time of the session in question where you do *not* want
        candidates who give a talk in that session. Format of this string must
        match entries in the "session_date" column of the DataFram

    mode: string, {"all" | "random"}
        The mode of the output. If "all", then the code will print all
        entries in the DataFrame that match the conditions given by the
        command keywords above. If "random", it will pick a random entry
        and display that.

    """

    area1_data = f["area_of_expertise_1"]
    area2_data = f["area_of_expertise_2"]
    area3_data = f["area_of_expertise_3"]

    session_date = f["session_date"]
    session_start = f["session_start"]
    session_end = f["session_end"]


    if np.size(area1) == 1:
        df_selected = df[(area1_data == area1)]
    else:
        df_selected = df[(area1_data == area1[0])]
        for a in area1[1:]:
            df_selected += df_selected[(area1_data == a)]

    if area2 is not None:
        if np.size(area2) == 1:
            df_selected_new = df_selected[(area2_data == area2)]

        else:
            df_selected_new = df_selected[(area2_data == area2[0])]
            for a in area2[1:]:
                df_selected_new += df_selected[(area2_data == a)]
    else:
        df_selected_new = df_selected

    if area3 is not None:
        if np.size(area3) == 1:
            df_selected_all= df_selected_new[(area3_data == area3)]

        else:
            df_selected_all = df_selected_new[(area3_data == area3[0])]
            for a in area2[1:]:
                df_selected_all += df_selected_new[(area3_data == a)]
    else:
        df_selected_all = df_selected_new



    df_off_date = df_selected_all[(session_date != date)]
    df_on_date =  df_selected_all[((session_date == date) &
                            (session_start != start_time) &
                            (session_end != end_time)) ]

    df_selected_all = df_off_date + df_on_date

    if mode == "all":
        return df_selected_all
    elif mode == "random":
        return df_selected_all.loc[ \
                np.random.choice(np.array(df_selected_all.index))]



def read_data(filename):
    df = pd.read_csv(filename)
    df.index += 2.0
    return df

def main():

    ## parse command line arguments
    clargs = parser()

    ## read the data from the csv file.
    df = read_data(clargs.filename)

    ## run query on database
    selected =  select_chair(df, clargs.area1, clargs.date,
                             clargs.start_time, clargs.end_time,
                             area2=clargs.area2, area3=clargs.area3,
                             mode=clargs.mode)

    ## print out the results to the screen
    print(selected)


    return


def parser():
    ### DEFINE PARSER FOR COMMAND LINE ARGUMENTS
    parser = argparse.ArgumentParser(description="Selection of AAS Chairs."
                                                 "Strings in command line "
                                                 "arguments need to match those "
                                                 "in the form *exactly*.")


    parser.add_argument("-f", "--filename", action="store", dest="filename",
                        required=True, help="File name with session chairs.")

    parser.add_argument("-a", "--area1", action="store", dest="area1",
                        required=True,
                        help="Primary area of expertise.")

    parser.add_argument("-d", "--date", action="store", dest="date",
                        required=True,
                        help="Date of the session")

    parser.add_argument("-s", "--start_time", action="store", dest="start_time",
                        required=True,
                        help="Start time of the session")

    parser.add_argument("-e", "--end_time", action="store", dest="end_time",
                        required=True,
                        help="End time of the session")

    parser.add_argument("-m", "--mode", action="store", dest="mode",
                        default="all",
                        help='Extract all possible chairs ("all") or pick '
                             'a chair from the available sample at random'
                             '("random").')

    parser.add_argument("--area2", action="store", dest="area2", default="None",
                        required=False, help="Secondary area of expertise.")

    parser.add_argument("--area3", action="store", dest="area3", default="None",
                        required=False, help="Tertiary area of expertise.")


    clargs = parser.parse_args()

    if clargs.area3 == "None":
        clargs.area3 = None

    if clargs.area2 == "None":
        clargs.area2 = None

    return clargs


if __name__ == "__main__":

    main()