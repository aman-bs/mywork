import pathlib
import pandas as pd
import pandera as pa
import json
import os

ALLOWED_UPLOAD_FILE_EXTENSIONS = {
    "FASTQ": ["_R1_001.fastq.gz", "_R2_001.fastq.gz", "_1.fq.gz", "_2.fq.gz"],
    "VCF": [".vcf"],
}

validation_summary= {}

def validate_fastq_file(group):
    
    if "FASTQ" in group:
        fastq_group = group["FASTQ"]
        column_name = fastq_group.name

        def is_valid_fastq_filepath(filepath):
            if isinstance(filepath, str) and any(filepath.endswith(ext) for ext in ALLOWED_UPLOAD_FILE_EXTENSIONS["FASTQ"]):
                return pathlib.Path(filepath).exists()
            else:
                return False
        
        invalid_files = fastq_group[~fastq_group.apply(is_valid_fastq_filepath)]
        if not invalid_files.empty:
            print(f"Invalid FASTQ files for column {column_name}: {invalid_files.tolist()}")
            # validation_summary["Invalid Fastq"].append(invalid_files)
            return False
        return True
    return True

def validate_vcf_file(group):
    if "VCF" in group:
        vcf_group = group["VCF"]
        column_name = vcf_group.name
        def is_valid_vcf_filepath(filepath):
            if isinstance(filepath, str) and any(filepath.endswith(ext) for ext in ALLOWED_UPLOAD_FILE_EXTENSIONS["VCF"]):
                return pathlib.Path(filepath).exists()
            else:
                return False
        
        invalid_files = vcf_group[~vcf_group.apply(is_valid_vcf_filepath)]
        if not invalid_files.empty:
            print(f"Invalid VCF files for column {column_name}: {invalid_files.tolist()}")
            return False
        return True
    return True

data = {
    "MRN": [123, 200, 300],
    "Visit_ID": ["123456", "234567", "345678"],
    "Sample_ID": ["S1", "S2", "S3"],
    "Start_Point": ["FASTQ", "VCF", "FASTQ"],
    "Filepath_R1": ["/home/bsl014/Desktop/cli_playground/7682736582_R1_00.fastq.gz", "", "/home/bsl014/Desktop/cli_playground/7682736582_R1_00.fastq.gz"],
    "Filepath_R2": ["/home/bsl014/Desktop/cli_playground/7682736582_R2_001.fastq.gz", "", "/home/bsl014/Desktop/cli_playground/7682736582_R2_00.fastq.gz"],
    "Filepath_VCF": ["", "/home/bsl014/Desktop/cli_playground/temp/dumm.vcf", ""]
}

df = pd.DataFrame(data)

schema = pa.DataFrameSchema(
    {
        "MRN": pa.Column(dtype=str, required=True, nullable=False, coerce=True),
        "Visit_ID": pa.Column(dtype=str, nullable=True, required=True),
        "Sample_ID": pa.Column(dtype=str, nullable=True, required=True),
        "Start_Point": pa.Column(dtype=str, nullable=True, required=True, checks=pa.Check.isin(allowed_values=["FASTQ", "VCF"])),
        "Filepath_R1": pa.Column(dtype=str, nullable=True, required=True, checks=[pa.Check(validate_fastq_file, groupby=["Start_Point"])]),
        "Filepath_R2": pa.Column(dtype=str, nullable=True, required=True, checks=pa.Check(validate_fastq_file, groupby=["Start_Point"])),
        "Filepath_VCF": pa.Column(dtype=str, nullable=True, required=True, checks=pa.Check(validate_vcf_file, groupby=["Start_Point"])),
    }
)

try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as e:
    print(json.dumps(e.message, indent=2))
