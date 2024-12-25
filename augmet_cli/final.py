import pathlib
import pandas as pd
import pandera as pa
import json
import os
import numpy as np
ALLOWED_UPLOAD_FILE_EXTENSIONS = {
    "FASTQ": ["_R1_001.fastq.gz", "_R2_001.fastq.gz", "_1.fq.gz", "_2.fq.gz"],
    "VCF": [".vcf"],
}

validation_summary = {}

def validate_MRN(val):
    def is_valid_MRN_val(val):
        return val != ""
    invalid_values = val[~val.apply(is_valid_MRN_val)]
    if not invalid_values.empty:
        invalid_rows = invalid_values.index.tolist() 
        invalid_mrns = invalid_values.tolist()
        validation_summary[f"Invalid MRN data for column {val.name}"] = {
            "Rows": invalid_rows,
            "Invalid MRN values": invalid_mrns
        }
        return False
    return True

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
            validation_summary[f"Invalid Fastq files for column {column_name}"]=invalid_files.to_list()
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
            validation_summary[f"Invalid VCF file for column {column_name}"]=invalid_files.to_list()
            return False
        return True
    return True

data = {
    "MRN": ['11', '2', ''],
    "Visit_ID": ["123456", "234567", "345678"],
    "Sample_ID": ["S1", "S2", "S3"],
    "Start_Point": ["FASTQ", "VCF", "FASTQ"],
    "Filepath_R1": ["/home/bsl014/Desktop/cli_playground/7682736582_R1_001.fastq.gz", "", "/home/bsl014/Desktop/cli_playground/7682736582_R1_001.fastq.gz"],
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
            checks=pa.Check(
                validate_MRN
            )
        ),
        "Visit_ID": pa.Column(
            dtype=str,
            nullable=True,
            required=True
        ),
        "Sample_ID": pa.Column(
            dtype=str,
            nullable=True,
            required=True),
        "Start_Point": pa.Column(
            dtype=str, 
            nullable=True, 
            required=True, 
            checks=pa.Check.isin(allowed_values=["FASTQ", "VCF"])
        ),
        "Filepath_R1": pa.Column(
            dtype=str, 
            nullable=True, 
            required=True, 
            checks=pa.Check(
                validate_fastq_file, 
                groupby=["Start_Point"]
            )
        ),
        "Filepath_R2": pa.Column(
            dtype=str, 
            nullable=True, 
            required=True, 
            checks=pa.Check(
                validate_fastq_file, 
                groupby=["Start_Point"]
            )
        ),
        "Filepath_VCF": pa.Column(
            dtype=str, 
            nullable=True, 
            required=True, 
            checks=pa.Check(
                validate_vcf_file, 
                groupby=["Start_Point"]
            )
        ),
    }
)

try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as e:
    print(validation_summary)
    exit(1)
except Exception as ue:
    print("Unknown Error!!")
    exit(1)
    # print(json.dumps(e.message, indent=2))

print(f">>>>>>>>>>>>>>>>>>>>>>>   VALIDATION SUMMARY   <<<<<<<<<<<<<<<<<<<<<<<<<<<<")
print(json.dumps(validation_summary))



# provided_columns: t.List[str] = d_f.columns.to_list()  # type: ignore
# missing_columns: list[str] = list(set(required_columns) - set(provided_columns))    # type: ignore
# if len(missing_columns) > 0:
#     if "Filepath" in provided_columns:  # type: ignore
#         console.error(
#             "Use of column `Filepath` is deprecated. Instead, use `Filepath_VCF` to pass path of the VCF file in the upload sheet.",
#             err=True,
#         )
#     console.error(
#         f"Missing required columns {missing_columns} in the upload sheet. Check out reference upload_sheet provided in the package.",
#         err=True,
#     )
#     console.exit(1)
# console.info(click.style("Starting data verification", fg="yellow"))