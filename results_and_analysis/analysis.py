import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import glob
import re

#get number of loops from a file
def get_loop_int(filename):
    with open(filename) as loops:
        return int(loops.read())

#setup main pandas results table
results_columns = ["Length [l]", "Seed [s * 10-8]", "Total Runtime (s)", "Perc Loop Runtime (s)", "Loop Total Count (n)"]
dtypes = ['int', 'int', 'float64', 'float64', 'int']
results = pd.DataFrame(columns = results_columns)

#loop over profile text files - split into /loops /profiles dirs
os.chdir('profiles')
os.getcwd()
list = glob.glob('*.txt')
for filename in list:
    print("Working on filename: {}".format(filename))
    print(list)
    split = re.findall( r"[a-zA-Z0-9-]+|[.,!?;]", filename)
    filename_short, length, seed = split[0] + "_" + split[1], split[0], split[1]
    seed = int(str(seed)[0])

    loop_total_number = get_loop_int("../loops/{}_{}_loops.txt".format(split[0],split[1]))
    print(loop_total_number)

    #gprof output uses a fixed width format with the following column widths:
    colspecs=[(1,6),(9,16),(18,25),(26,34),(39,43),(48,52),(54,93)]

    names = ["Percentage Time", "Cumulative Seconds", "Self Seconds", "Calls", "Self T/S", "Total T/S", "Name"]
    dtypes = ['float64', 'float64', 'float64', 'int', 'int', 'int', 'object']

    #strip headers - deal with the case where there are additional blank rows.
    with open(filename) as data:
        if 'no time accumulated' in data.readlines()[3]:
            print("No time accumulated")
            skiprows = 7
        else:
            skiprows = 5

    df = pd.read_fwf(filename,colspecs=colspecs, skiprows=skiprows, names=names, dtypes=dtypes)


    #calculate total time spent in the key sections of the Percolate program
    total_time = df["Self Seconds"].sum()
    perc = df[df['Name'].str.contains("(15[1-9]|16[0-9]|17[0-8])", regex=True)]
    perc_loop_time = perc["Self Seconds"].sum()

    #write out our results
    result_row = [int(length), int(seed), total_time, float(perc_loop_time), int(loop_total_number)]
    results.loc[len(results)] = result_row

#go back to main directory.
os.chdir("..")

#additonal processing, generation of latex formatted tables and scatter graphs
sorted_results = results.convert_dtypes().sort_values(by=['Length [l]'])
results_mask = sorted_results['Length [l]']>=100
sorted_results = sorted_results[results_mask]
#print(sorted_results.to_string())

head_tail_results = sorted_results.head(4)
head_tail_results = head_tail_results.append(sorted_results.tail(4))
print(head_tail_results.to_string())
ltx_head_tail = head_tail_results.to_latex()

head_tail_results = sorted_results.head(4)
head_tail_results = head_tail_results.append(sorted_results.tail(4))
print(head_tail_results.to_string())
ltx_head_tail = head_tail_results.to_latex(index=False)
print(ltx_head_tail)

sorted_results.plot(x ='Length [l]', y='Total Runtime (s)', c='Seed [s * 10-8]', marker="x", kind = 'scatter', s=1)
plt.show()

seed_groups = sorted_results.groupby('Seed [s * 10-8]')
seed_groups.plot(x ='Length [l]', y='Total Runtime (s)', marker="x", kind = 'scatter', s=1)
plt.show()

sorted_results.plot(x ='Length [l]', y='Loop Total Count (n)', kind = 'scatter', s=1)
plt.show()

sorted_results.plot(x ='Total Runtime (s)', y='Loop Total Count (n)', kind = 'scatter', s=1)
plt.show()

results_lengths = sorted_results.groupby('Length [l]', as_index=False).mean()
results_lengths = results_lengths.drop(['Seed [s * 10-8]'], axis=1)
results_lengths['Total Runtime (s)'] = results_lengths['Total Runtime (s)'].round(decimals=2)
results_lengths['Perc Loop Runtime (s)'] = results_lengths['Perc Loop Runtime (s)'].round(decimals=2)
results_lengths['Loop Total Count (n)'] = results_lengths['Loop Total Count (n)'].round(decimals=2)
results_lengths['Loops/sec (s)'] = results_lengths['Loop Total Count (n)'] / results_lengths['Perc Loop Runtime (s)']
results_lengths['Loops/sec (s)'] = results_lengths['Loops/sec (s)'].round(decimals=2)
ltx_results_lengths = results_lengths.to_latex(index=False)
print(ltx_results_lengths)

results_lengths.plot(x ='Length [l]', y='Perc Loop Runtime (s)', kind = 'scatter', title="Size of Grid v Percolate Algorithm Runtime")
plt.show()
results_lengths.plot(x ='Length [l]', y='Loops/sec (s)', kind = 'scatter', title="Size of Grid v Cluster Iterations per Second")
plt.show()
results_lengths.plot(x ='Length [l]', y='Loop Total Count (n)', kind = 'scatter', title="Size of Grid v Loop Total Count")
plt.show()
results_lengths.plot(x ='Perc Loop Runtime (s)', y='Loop Total Count (n)', kind = 'scatter', title="Percolate Algorithm Runtime v Loop Total Count")
plt.show()
