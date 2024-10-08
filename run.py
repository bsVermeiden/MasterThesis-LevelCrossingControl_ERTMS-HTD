#!/usr/bin/env python3

import subprocess
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

debug = True

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def replace_pattern(filename, pattern, replacement):
    content = read_file(filename)
    content = re.sub(pattern, replacement, content)
    write_file(filename, content)

def replace_track(filename, new_string):
    replace_pattern(filename, r"(?<=TRACK_0 = ).*", new_string)

def change_announcement(filename, new_string):
    replace_pattern(filename, r"(?<=TYPE_0 = ).*", new_string)

def change_warning_time(filename, new_number):
    pattern = r'val\(t_active\s*>\s*ANNOUNCEMENT_TIME\s*\+\s*\d+\)'
    replacement = f'val(t_active > ANNOUNCEMENT_TIME + {new_number})'
    replace_pattern(filename, pattern, replacement)

def change_lx_location(filename, new_number):
    replace_pattern(filename, r"(?<=LXLOCATION_0 = ).*", new_number)

def change_train_speed(filename, new_number):
    replace_pattern(filename, r"(?<=SPEED_0 = ).*", new_number)

def change_train_max_speed(filename, new_number):
    replace_pattern(filename, r"(?<=MAX_SPEED_0 = ).*", new_number)

def change_departure_detection(filename, new_string):
    replace_pattern(filename, r"(?<=DEPARTURE_DETECTION_0 = ).*", new_string)

def compile_model(data):
    # Change working dir to the script path
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Check if type in data
    if len(data) == 3:
        data = f'TVP-TR/{data}'

    # Compile the model
    run = subprocess.run(['mcrl22lps', '-cbwa', '--balance-summands', 'Crossing_spec.mcrl2'], stdout=subprocess.PIPE, check=True)
    run = subprocess.run(['lpssumelm', '-c'], input=run.stdout, stdout=subprocess.PIPE, check=True)
    run = subprocess.run(['lps2lts', '--cached', '--save-at-end', f'--timings=./Results/Timings/{data}', '-', 'crossing.lts'], input=run.stdout, check=True)

def run_simulation():
    run = subprocess.run(['lts2pbes', '--formula=./properties/Maximum_Warning_Time.mcf', 'crossing.lts'], stdout=subprocess.PIPE, check=True)
    run = subprocess.run(['pbessolve'], input=run.stdout, stdout=subprocess.PIPE, check=True)

    return run

def simulate_for_track(track, max_speeds, types):
    results = []
    t_tr = t_tvp = 25
 
    for ms in max_speeds:        
        change_train_max_speed('Crossing_spec.mcrl2', ms)
        change_train_speed('Crossing_spec.mcrl2', ms)

        t_tr = 25
        t_tvp = 25
        for t in types:
            change_announcement('Crossing_spec.mcrl2', t)
            compile_model([track, ms, t])

            exceeding_time = 0
            change_warning_time('./properties/Maximum_Warning_Time.mcf', exceeding_time)

            while run_simulation().stdout == b'true\n':
                exceeding_time += 1
                change_warning_time('./properties/Maximum_Warning_Time.mcf', exceeding_time)

            if t == 'TR;':
                t_tr += exceeding_time
            else:
                t_tvp += exceeding_time

        if debug:
            print('Track: {}, Max Speed: {}, Warning Time TVP: {}, Warning Time TR: {}'.format(track, ms, t_tvp, t_tr))

        results.append({'Track': track[:-1], 'Max_Speed': ms[:-1], 'Warning_Time_TVP': t_tvp, 'Warning_Time_TR': t_tr})

    return results

def test_maximum_warning_time():
    types = ['TVP;', 'TR;']
    # All track options to test 1000 - 1500
    # 
    tracks = ['[1000,100,100];', '[1100,100,100];', '[1200,100,100];',
              '[1300,100,100];', '[1400,100,100];', '[1500,100,100];'
              ]
    
    tracks2 = ['[100,1500,100,100];', '[200,1500,100,100];', '[300,1500,100,100];',
               '[400,1500,100,100];', '[500,1500,100,100];', '[600,1500,100,100];',
               '[700,1500,100,100];'  
              ]
    
    # All speeds from 0 to 38 in steps of 10
    max_speeds = ['10;', '20;', '30;', '38;']

    # Create a dataframe to store the results
    df = pd.DataFrame(columns=['Track', 'Max_Speed', 'Warning_Time_TVP', 'Warning_Time_TR'])

    change_lx_location('Crossing_spec.mcrl2', '1;')
    for tr in tracks:
        replace_track('Crossing_spec.mcrl2', tr)
        results = simulate_for_track(tr, max_speeds, types)
        df = df._append(results, ignore_index=True)

    change_lx_location('Crossing_spec.mcrl2', '2;')
    for tr in tracks2:
        replace_track('Crossing_spec.mcrl2', tr)
        results = simulate_for_track(tr, max_speeds, types)
        df = df._append(results, ignore_index=True)

    # Save the results to a csv file
    df.to_csv('results.csv')

def test_departure_detection():
    tracks = ['[125,100,100];', '[150,100,100];', '[175,100,100];', '[200,100,100];']

    df = pd.DataFrame(columns=['Tracks', 'Warning_Time_Departure_Detection', 'Warning_Time_No_Departure_Detection'])

    for track in tracks:
        replace_track('Crossing_spec.mcrl2', track)
        change_departure_detection('Crossing_spec.mcrl2', 'true;')
        compile_model([track, 'true'])
        exceeding_time = 0
        change_warning_time('./properties/Maximum_Warning_Time.mcf', exceeding_time)

        while run_simulation().stdout == b'true\n':
            exceeding_time += 1
            change_warning_time('./properties/Maximum_Warning_Time.mcf', exceeding_time)

        wtd = exceeding_time + 25

        change_departure_detection('Crossing_spec.mcrl2', 'false;')
        compile_model([track, 'false'])
        exceeding_time = 0
        change_warning_time('./properties/Maximum_Warning_Time.mcf', exceeding_time)

        while run_simulation().stdout == b'true\n':
            exceeding_time += 1
            change_warning_time('./properties/Maximum_Warning_Time.mcf', exceeding_time)

        wtdnd = exceeding_time + 25
        print(f'Track: {track[:-1]}, Warning Time Departure Detection: {wtd}, Warning Time No Departure Detection: {wtdnd}')
        df = df._append({'Track': track[:-1], 'Warning_Time_Departure_Detection': wtd, 'Warning_Time_No_Departure_Detection': wtdnd}, ignore_index=True)

    df.to_csv('results/results_departure_detection_30.csv')

def to_df():
    # Read in the file.txt file and write it to a dataframe in the format 
    # pd.DataFrame(columns=['Track', 'Max_Speed', 'Warning_Time_TVP', 'Warning_Time_TR'])

    with open("file.txt", "r") as file:
        data = file.readlines()
        data = [x.strip() for x in data]
    df = pd.DataFrame(columns=['Track', 'Warning Time Departure Detection', 'Warning Time No Departure Detection'])

    for row in data:
        vals = row.split(" ")

        track = vals[1][:-2]
        max_speed = vals[4][:-2]
        t_tvp = vals[8][:-1]
        t_tr = vals[-1]        
        df = df._append({'Track': track, 'Max_Speed': max_speed, 'Warning_Time_TVP': t_tvp, 'Warning_Time_TR': t_tr}, ignore_index=True)

    df.to_csv('results.csv')

def create_plot():
    # Load the CSV file into a DataFrame
    df = pd.read_csv('results.csv')

    # Calculate the difference in warning time between TVP and TR
    df['Warning_Time_Difference'] = df['Warning_Time_TVP'] - df['Warning_Time_TR']

    # Convert columns to appropriate types
    df['Max_Speed'] = df['Max_Speed'].astype(int)
    df['Track'] = df['Track'].astype(str)

    # Set up the plot
    plt.figure(figsize=(14, 8))

    # Create a bar plot to show the difference in warning time
    sns.barplot(x='Track', y='Warning_Time_Difference', hue='Max_Speed', data=df)

    # Customize the plot
    plt.title('Difference in Warning Time between TVP and TR by Track and Speed')
    plt.xlabel('Track')
    plt.ylabel('Warning Time Difference (TVP - TR)')
    plt.legend(title='Max Speed')
    plt.xticks(rotation=90)

    # Show the plot
    plt.tight_layout()
    plt.savefig('plot.png')

def csv_to_latex():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Function that converts a CSV file to a LaTeX table
    df = pd.read_csv('./results.csv')

    # Remove the first collum
    df = df.drop(df.columns[0], axis=1)

    # Only add each track option to the table once, but still display all speeds
    # Like
    # [1000, 100, 100] | 10
    #                  | 20
    #                  | 30
    #                  | 38 
    # [1100, 100, 100] | 10

    # Create a new DataFrame to store the LaTeX table
    new_df = pd.DataFrame(columns=['Track', 'Max_Speed', 'Warning_Time_TVP', 'Warning_Time_TR'])

    for i, row in df.iterrows():
        track = row['Track']
        max_speed = row['Max_Speed']
        t_tvp = row['Warning_Time_TVP']
        t_tr = row['Warning_Time_TR']

        if i == 0:
            new_df = new_df._append({'Track': track, 'Max_Speed': max_speed, 'Warning_Time_TVP': t_tvp, 'Warning_Time_TR': t_tr}, ignore_index=True)
        else:
            if track == df.iloc[i-1]['Track']:
                new_df = new_df._append({'Track': '', 'Max_Speed': max_speed, 'Warning_Time_TVP': t_tvp, 'Warning_Time_TR': t_tr}, ignore_index=True)
            else:
                new_df = new_df._append({'Track': track, 'Max_Speed': max_speed, 'Warning_Time_TVP': t_tvp, 'Warning_Time_TR': t_tr}, ignore_index=True)

    df = new_df

    # Center the tracks in the table
    df['Track'] = df['Track'].apply(lambda x: f'\\multicolumn{{1}}{{c}}{{{x}}}' if x != '' else x)

    # Convert the DataFrame to a LaTeX table
    latex_table = df.to_latex(index=False)

    print(latex_table)

def get_average_timings():
    # Read in all the files from the Timings folder
    files = os.listdir('./Timings/TVP-TR')

    # Create a DataFrame to store the times
    tr_times = pd.DataFrame(columns=['Track', 'Max_Speed', 'Time'])
    tvp_times = pd.DataFrame(columns=['Track', 'Max_Speed', 'Time'])

    for file in files:
        if file[-1] == ']':
            # Remove the first and last character from the file name
            # Also remove ' and ; from the file name
            fileN = file[1:-1].replace("'", '').replace(';', '')
            os.rename(f'./Timings/TVP-TR/{file}', f'./Timings/TVP-TR/{fileN}')

    for file in files:
        # Get the track, max speed and type from the file name
        track, max_speed, type = file.split(', ')

        # Read in the file
        with open(f'./Timings/TVP-TR/{file}', 'r') as f:
            # Get only the number value from the file
            #- tool: lps2lts
            # timing:
            # total: 246.199043

            time = float(f.readlines()[-1].split(':')[-1])

        if type == 'TR':
            tr_times = tr_times._append({'Track': track, 'Max_Speed': max_speed, 'Time': time}, ignore_index=True)
        else:
            tvp_times = tvp_times._append({'Track': track, 'Max_Speed': max_speed, 'Time': time}, ignore_index=True)

    # Calculate the average time for each max speed
    tr_times = tr_times.groupby(['Max_Speed']).mean().reset_index()
    tvp_times = tvp_times.groupby(['Max_Speed']).mean().reset_index()

    # Save the results to a CSV file
    tr_times.to_csv('./Timings/tr_times.csv')
    tvp_times.to_csv('./Timings/tvp_times.csv')



if __name__ == '__main__':
    test_maximum_warning_time()
    # change_train_speed('Crossing_spec.mcrl2', 0)
    # test_departure_detection()
    # get_average_timings()