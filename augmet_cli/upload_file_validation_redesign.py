import pathlib
import pandas as pd
import pandera as pa
from pandera import Column, Check
from pandera.typing import DataFrame, Series
import os

ALLOWED_UPLOAD_FILE_EXTENSIONS = {
    "FASTQ": ["_R1_001.fastq.gz", "_R2_001.fastq.gz", "_1.fq.gz", "_2.fq.gz"],
    "VCF": [".vcf"],
}

data = {
    "MRN": [123, 200, 300],
    "Visit_ID": ["123456", "234567", "345678"],
    "Sample_ID": ["S1", "S2", "S3"],
    "Start_Point": ["fastq", "vcf", "fastq"],
    "Filepath_R1": ["/path/to/file1.fastq", None, "/path/to/file3.fastq"],
    "Filepath_R2": ["/path/to/file1.fastq", None, "/path/to/file3.fastq"],
    "Filepath_VCF": [None, "/path/to/file2.vcf", None]
}
df = pd.DataFrame(data)

class Schema(pa.DataFrameModel):
    MRN: Series[int] = pa.Field(gt=0, nullable=False, coerce=True)
    # MRN = Column(int, Check.ge(0), nullable=False)
    Visit_ID =  pa.Field(nullable=True)
    Sample_ID = pa.Field(nullable=True)
    Start_Point = pa.Field(nullable=True)
    Filepath_R1 = pa.Field(nullable=True)
    Filepath_R2 = pa.Field(nullable=True)
    Filepath_VCF = pa.Field(nullable=True)

    @pa.check("Filepath_R1")
    def check_filepath_r1(cls, series: pd.Series) -> bool:
        return series["Start_Point"].apply(lambda x: (
            (
                x.upper() == "FASTQ" and
                isinstance(series["Filepath_R1"], str) and
                os.path.exists(series["Filepath_R1"]) and
                any(series["Filepath_R1"].endswith(ext) for ext in ALLOWED_UPLOAD_FILE_EXTENSIONS["FASTQ"])
            ) or
            (x.upper() == "VCF" and pd.isna(series["Filepath_R1"]))
        )).all()

    # Custom row-level check for Filepath_R2
    @pa.check("Filepath_R2")
    def check_filepath_r2(cls, series: pd.Series) -> bool:
        return series["Start_Point"].apply(lambda x: (
            (
                x.upper() == "FASTQ" and
                isinstance(series["Filepath_R2"], str) and
                os.path.exists(series["Filepath_R2"]) and
                any(series["Filepath_R2"].endswith(ext) for ext in ALLOWED_UPLOAD_FILE_EXTENSIONS["FASTQ"])
            ) or
            (x.upper() == "VCF" and pd.isna(series["Filepath_R2"]))
        )).all()

    # Custom row-level check for Filepath_VCF
    @pa.check("Filepath_VCF")
    def check_filepath_vcf(cls, series: pd.Series) -> bool:
        return series["Start_Point"].apply(lambda x: (
            (
                x.upper() == "FASTQ" and pd.isna(series["Filepath_VCF"])
            ) or
            (
                x.upper() == "VCF" and 
                isinstance(series["Filepath_VCF"], str) and 
                any(series["Filepath_VCF"].endswith(ext) for ext in ALLOWED_UPLOAD_FILE_EXTENSIONS["VCF"])
            )
        )).all()

# Function to validate and split DataFrame
def validate_and_split_df(df: pd.DataFrame):
    valid_rows = []
    invalid_rows = []
    error_messages = []
    
    # Validate the DataFrame using the Pandera schema
    try:
        # Full DataFrame validation (with check_obj argument)
        MyDataFrameSchema.validate(df)  # pass the DataFrame here
        valid_rows = df
    except pa.errors.SchemaErrors as e:
        # If validation fails, iterate through the errors
        for idx, failure_case in e.failure_cases.iterrows():
            row = df.iloc[idx]  # Get the row that failed validation
            row["errors"] = str(failure_case["failure_case"])  # Add error details
            invalid_rows.append(row)
        
    # Convert the lists of valid and invalid rows back to DataFrames
    validated_df = pd.DataFrame(valid_rows)
    skiprows = pd.DataFrame(invalid_rows)
    
    return validated_df, skiprows

# Run the validation and splitting
validated_df, skiprows = validate_and_split_df(df)

# Show the results
print("Validated DataFrame:")
print(validated_df)

print("\nSkiprows DataFrame (Invalid Rows):")
print(skiprows)

# Save to CSV files
validated_df.to_csv('validated_data.csv', index=False)
skiprows.to_csv('skiprows_data.csv', index=False)
