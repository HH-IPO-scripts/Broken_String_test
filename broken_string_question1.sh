
#!/bin/bash

# this script is to be ran and stored in the data folder in coding-test-main.
# (coding-test-main/data/)

### Question 1.1 Map the reads to chromosome 21

# We will need to index the chromosome in the chr21 folder using bwa
echo -e "Performing indexing of Chromosome 21"
echo -e "\n"
bwa index chr21/chr21.fasta
echo -e "\n"
echo -e "Successfully indexed Chromosome 21"

# Once we have indexed the chromosome, we'll need to map the fastq files to chromosome 21
# Create a new directory to save the sam files
mkdir -p mapped_sam_files

echo -e "Mapping fastq files to Chromosome 21, saving mapped sample files in .sam to mapped_sam_files folder"
echo -e "\n"
# Loop through each of the sample files
for sample in fastqs/*.fastq.gz; do
    # Extract sample name from the file name
    sample_name=$(basename "$sample" .fastq.gz)
    
    # Map the sample to chromosome 21 and save results in mapped_sam_files
    bwa mem chr21/chr21.fasta "$sample" > "mapped_sam_files/${sample_name}.sam"
done
echo -e "\n"
echo -e "Successfully mapped fastq files to Chromosome 21, output .sam files saved in mapped_sam_files folder"
echo -e "\n"





# Convert sam files to bam files using samtools 
# Create a new directory to save the bam files
mkdir -p mapped_bam_files

# Loop through each sam file and convert to bam file
for sam_file in mapped_sam_files/*.sam; do
    # Extract the sample name from the .sam file
    sample_name=$(basename "$sam_file" .sam)
    
    # Convert the sam file to bam file and save it in mapped_bam_files
    samtools view -b -o "mapped_bam_files/${sample_name}.bam" "$sam_file"
done


echo -e "sam files in mapped_sam_files have been successfully converted to bam files and saved in the mapped_bam_files folder"
echo -e "\n"


### Questions 1.2  Convert the bam files in mapped_bam_files to bed format for downstream processing
# Create a new directory to save the bed files
mkdir -p mapped_bed_files

# Loop through each bam file, convert to bed file and save them in mapped_bed_files
for bam_file in mapped_bam_files/*.bam; do
    # Extract the sample name from the bam file
    sample_name=$(basename "$bam_file" .bam)
    
    # Convert the bam file to bed file and save it in mapped_bed_files
    bedtools bamtobed -i "$bam_file" > "mapped_bed_files/${sample_name}.bed"
done

echo -e "bam files in mapped_bam_files have been successfully converted to bed files and saved in the mapped_bed_files folder"
echo -e "\n"



### Question 1.3 Process the bed file so that the coordinates are adjusted to just include the break site
# Create a new directory to save the adjusted bed files
mkdir -p adjusted_bed_files

# Loop through each of the bed files, adjust coordinates in bed files and save them in adjusted_bed_files
for bed_file in mapped_bed_files/*.bed; do
    # Extract the sample name from the bed file
    sample_name=$(basename "$bed_file" .bed)
    
    # Create a temporary file to store adjusted coordinates
    temp_file="adjusted_bed_files/${sample_name}_temp.bed"
    
    # Adjust coordinates based on strand and save them in the temporary file
    while IFS=$'\t' read -r chrom start end name score strand; do
        if [ "$strand" == "+" ]; then
            end=$((start + 1))
        elif [ "$strand" == "-" ]; then
            start=$((end - 1))
        fi
        echo -e "${chrom}\t${start}\t${end}\t${name}\t${score}\t${strand}" >> "$temp_file"
    done < "$bed_file"
    
    # Rename the temporary file to the final adjusted bed file and save in adjusted_bed_files
    mv "$temp_file" "adjusted_bed_files/${sample_name}_adjusted.bed"
done


echo -e "bed files in mapped_bed_files have successfully had their coordinates adjusted to include break sites, adjusted bed files are saved in the adjusted_bed_files folder"
echo -e "\n"


### Question 1.4 Intersect the breaks encoded in the bed file with predicted AsiSI sites
# Create a new directory to save the intersection results
mkdir -p intersection_results

# Loop through each of the adjusted bed files, perform the intersection and save results in intersection_results
for adjusted_bed_file in adjusted_bed_files/*.bed; do
    # Extract the sample name from the adjusted bedfiles
    sample_name=$(basename "$adjusted_bed_file" _adjusted.bed)
    
    # Perform the intersection with AsiSI cut sites and save the results in intersection_results
    bedtools intersect -a "$adjusted_bed_file" -b chr21_AsiSI_sites.t2t.bed > "intersection_results/${sample_name}_intersection.bed"
done 

echo -e "breaks in adjusted bed files have been successfully intersected with the predicted AsiSI sites, intersection results are saved in the intersection_results folder"
echo -e "\n"

