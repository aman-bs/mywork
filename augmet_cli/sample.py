import pathlib
import pandas as pd
import pandera as pa
import json
import os

"""
    Idea here is to use pandera groupby
"""

ALLOWED_UPLOAD_FILE_EXTENSIONS = {
    "FASTQ": ["_R1_001.fastq.gz", "_R2_001.fastq.gz", "_1.fq.gz", "_2.fq.gz"],
    "VCF": [".vcf"],
}

def validate_vcf_file(group):
    if "VCF" in group:
        vcf_group = group["VCF"]
        def is_valid_vcf_filepath(filepath):
            return isinstance(filepath, str) and any(filepath.endswith(ext) for ext in ALLOWED_UPLOAD_FILE_EXTENSIONS["VCF"]) and pathlib.Path(filepath).exists() 
        return vcf_group.apply(is_valid_vcf_filepath).all()
    
def validate_fastq_file(group):
    if "FASTQ" in group:
        fastq_group = group["FASTQ"] 
        def is_valid_fastq_filepath(filepath):
            return isinstance(filepath, str) and any(filepath.endswith(ext) for ext in ALLOWED_UPLOAD_FILE_EXTENSIONS["FASTQ"]) and os.path.exists(filepath) #pathlib.Path(filepath).exists()
        return fastq_group.apply(is_valid_fastq_filepath).all()

data = {
    "MRN": [123, 200, 300],
    "Visit_ID": ["123456", "234567", "345678"],
    "Sample_ID": ["S1", "S2", "S3"],
    "Start_Point": ["FASTQ", "VCF", "FASTQ"],
    "Filepath_R1": ["/home/bsl014/Desktop/cli_playground/7682736582_R1_001.fastq.gz", "", "/home/bsl014/Desktop/cli_playground/7682736582_R1_00.fastq.gz"],
    "Filepath_R2": ["/home/bsl014/Desktop/cli_playground/7682736582_R2_001.fastq.gz", "", "/home/bsl014/Desktop/cli_playground/7682736582_R2_001.fastq.gz"],
    "Filepath_VCF": ["", "/home/bsl014/Desktop/cli_playground/temp/dummy.vcf", ""]
}
df = pd.DataFrame(data)

schema = pa.DataFrameSchema(
    {
        "MRN": pa.Column(
            dtype=str,
            required=True,
            nullable=False,
            coerce=True,
        ),
        "Visit_ID":  pa.Column(
            dtype=str,
            nullable=True,
            required=True,
        ),
        "Sample_ID": pa.Column(
            dtype=str,
            nullable=True,
            required=True,
        ),
        "Start_Point": pa.Column(
            dtype=str,
            nullable=True,
            required=True,
            checks = pa.Check.isin(allowed_values=["FASTQ", "VCF"])
        ),
        "Filepath_R1": pa.Column(
            dtype=str,
            nullable=True,
            required=True,
            checks= [pa.Check(
                validate_fastq_file,
                groupby=["Start_Point"]
            )],
        ),
        "Filepath_R2": pa.Column(
            dtype=str,
            nullable=True,
            required=True,
            checks= pa.Check(
                validate_fastq_file,
                groupby=["Start_Point"]
            ),
        ),
        "Filepath_VCF": pa.Column(
            dtype=str,
            nullable=True,
            required=True,
            checks= pa.Check(
                validate_vcf_file,
                groupby=["Start_Point"]
            ),
        ),
    }
)

try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as e:
    print(json.dumps(e.message, indent=2))

# try:
#     sdf = schema.validate(df, lazy=True)
# except pa.errors.SchemaErrors as e:
#     breakpoint()
#     # print(json.dumps(e.message, indent=2))
#     print("Schema errors and failure cases:")
#     print(e.failure_cases)
#     print("\nDataFrame object that failed validation:")
#     print(e.data)

# except pa.errors.SchemaError as e:
#     breakpoint()
#     print(e)
# except Exception as ee:
#     print(f"Uncaught exception: {ee}")