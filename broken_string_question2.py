#!/usr/bin/env python3

# same as with broken_string_question1.sh, this script is to be ran and stored in the data folder in coding-test-main
# (coding-test-main/data/)

# import necessary libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

### Question 2.1: Read in the data
# Define the directory containing the BED files
bed_files_directory = "pre-made_results/AsiSI_site_breaks/"
# Initialize a dictionary to store the data, where keys are sample names and values are DataFrames
asi_si_breaks_dict = {}


# Iterate through the BED files in the directory
print("Reading in AsiSI_site_break bed files")
print("\n")
for bed_file in os.listdir(bed_files_directory):
    if bed_file.endswith(".bed"):
        sample_name = os.path.splitext(bed_file)[0]  # Extract the sample name from the file name
        bed_df = pd.read_csv(os.path.join(bed_files_directory, bed_file), sep='\t', header=None, names=["chromosome", "start", "end", "break_count"])
        asi_si_breaks_dict[sample_name] = bed_df

print("Successfully read in bed files from AsiSI_site_breaks folder")
print("\n")

# Now, asi_si_breaks_data contains DataFrames for each sample





### Question 2.2: Sum the Number of AsiSI Breaks
sum_of_asi_si_breaks = {}

# Loop through ead of the samples and corresponding dfs
# and calculate the total number of breaks in the break_count column
for sample_name, df in asi_si_breaks_dict.items():
    sum_breaks = df["break_count"].sum()
    sum_of_asi_si_breaks[sample_name] = sum_breaks

print("Successfully calculated sum of AsiSI breaks for each sample")
print("\n")
print(sum_of_asi_si_breaks)
print("\n")
# Now, sum_of_asi_si_breaks contains the sum of AsiSI breaks for each sample





### Question 2.3: Normalize the Number of AsiSI Breaks
# Read in sample_total_breaks.tsv
print("Reading in total break file")
total_breaks_file = "pre-made_results/sample_total_breaks.tsv"
total_breaks_df = pd.read_csv(total_breaks_file, sep='\t', header=None, names=["sample_name", "total_breaks"])
print("\n")
print("Successfully read in total break file")
print("\n")
print(total_breaks_df)
print("\n")

# Preprocess the sample names in total_breaks df to match those in sum_of_asi_si_dict
total_breaks_df['sample_name'] = total_breaks_df['sample_name'] + "_AsiSI_breaks"
print("Sample names in sample_total_breaks.tsv have been successfully modified to match those in the sum of AsiSI breaks dictionary")
print("\n")
print(total_breaks_df)
print("\n")

# Merge the Dataframes in the sum_of_asi_si_dict and total_breaks_df on the sample_name column
normalised_df = total_breaks_df.merge(pd.DataFrame(sum_of_asi_si_breaks.items(), columns=['sample_name', 'sum_of_asi_si_breaks']), on="sample_name")
print("Successfully merged data to contain the total number of breaks and the sum of AsiSI breaks for each sample")
print("\n")
print(normalised_df)
print("\n")

# Calculate the normalized AsiSI breaks and store them in a new column
normalised_df["normalised_breaks"] = (normalised_df["sum_of_asi_si_breaks"] / (normalised_df["total_breaks"] / 1000))
print("A normalised breaks column has been successfully added to the data, this is the sum of AsiSI breaks dividing by the total number of breaks / 1000")
print("\n")
print(normalised_df)
print("\n")




### Question 2.4: Plot the data so that it is possible to determine if there are clusters of samples representing control and treated subsets
# Boxplot

# Create a figure and axis object
plt.figure(figsize=(10,6))
ax = sns.boxplot(data=normalised_df, x="sample_name", y="normalised_breaks")

# Customise axis labels and title
plt.xlabel("Sample Name", fontsize=12)
plt.ylabel("Normalised AsiSI breaks", fontsize=12)
plt.title("Normalised AsiSI breaks for each sample", fontsize=14)

# Rotate x-axis sample name labels
plt.xticks(rotation=90, fontsize=12)

# Show plot
plt.tight_layout()
plt.savefig("normalised_AsiSI_breaks.png")
print("Normalised Asi_Si breaks for each sample have been successfully plotted and saved to normalised_AsiSI_breaks.png for your viewing")
print("\n")




### 4. What is the maximum percentage of possible AsiSI cut sites on chromosome 21 (as described in the chr21_AsiSI_sites.t2t.bed file) that is observed in a single sample?
# Read in AsiSI cutes bed file
asi_si_df = pd.read_csv('chr21_AsiSI_sites.t2t.bed', sep='\t', header=None)

# Find sample with the highest numer of AsiSI breaks and save as variable
sample_max_breaks = normalised_df.loc[normalised_df['normalised_breaks'].idxmax()]
print("Sample with the highest number of AsiSI breaks")
print("\n")
print(sample_max_breaks)
print("\n")

# Get count of observed AsiSI breaks in the selected sample
observed_breaks = sample_max_breaks['sum_of_asi_si_breaks']

# Calculate the maximum percentage using the maximum number of observed AsiSI breaks and total number of possible breaks
total_sites = len(asi_si_df)
max_percentage = (observed_breaks / total_sites) * 100

print(f"The maximum percentage of possible AsiSI cut sites observed in a single sample is {max_percentage:.2f}%")
