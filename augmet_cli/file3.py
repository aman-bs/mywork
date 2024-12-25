import pathlib
import pandas as pd
import pandera as pa
from pandera import Column, Check
from pandera.typing import DataFrame, Series
import os


    """Idea is to split into two DFs
    """
ALLOWED_UPLOAD_FILE_EXTENSIONS = {
    "FASTQ": ["_R1_001.fastq.gz", "_R2_001.fastq.gz", "_1.fq.gz", "_2.fq.gz"],
    "VCF": [".vcf"],
}

data = {
    "MRN": [123, 200, 300],
    "Visit_ID": ["123456", "234567", "345678"],
    "Sample_ID": ["S1", "S2", "S3"],
    "Start_Point": ["fastq", "vcf", "fastq"],
    "Filepath_R1": ["/home/bsl014/Desktop/cli_playground/7682736582_R1_001.fastq.gz", "", "/home/bsl014/Desktop/cli_playground/7682736582_R1_001.fastq.gz"],
    "Filepath_R2": ["/home/bsl014/Desktop/cli_playground/7682736582_R2_001.fastq.gz", "", "/home/bsl014/Desktop/cli_playground/7682736582_R2.fastq.gz"],
    "Filepath_VCF": ["", "/path/to/file2.vcf", "/home/bsl014/Desktop/cli_playground/7682736582_R2_001.fastq.gz"]
}

df = pd.DataFrame(data)

df = df.groupby("Start_Point")
df_fastq = df.get_group("fastq")
df_vcf = df.get_group("vcf")

df_schema = pa.DataFrameSchema(
    {
        "MRN": pa.Column(dtype=pa.INT64,nullable=False,coerce=True, checks=pa.Check.gt(min_value=0)),
        "Visit_ID":  pa.Column(dtype=str, nullable=True),
        "Sample_ID": pa.Column(dtype=str, nullable=True),
        "Start_Point": pa.Column(dtype=str, nullable=True), #checks=pa.Check.isin(allowed_values=["fastq", "vcf"]),),
        "Filepath_R1": pa.Column(dtype=str, nullable=True), #checks=pa.Check(check_fn=pathlib.Path.exists)),
        "Filepath_R2": pa.Column(dtype=str, nullable=True), #checks=pa.Check(check_fn=pathlib.Path.exists)),
        "Filepath_VCF": pa.Column(dtype=str, nullable=True), #checks=pa.Check(check_fn=pathlib.Path.exists))    ,
    }
)



# :
#     MRN: Series[int] = pa.Column(dtype=pa.INT64,nullable=False,coerce=True, checks=pa.Check.gt(min_value=0))
#     Visit_ID: Series[str] =  pa.Column(dtype=pa.STRING, nullable=True)
#     Sample_ID: Series[str] = pa.Column(dtype=pa.STRING, nullable=True)
#     Start_Point: Series[str] = pa.Column(dtype=pa.STRING, nullable=True, checks=pa.Check.isin(allowed_values=["fastq", "vcf"]),)
#     Filepath_R1: Series[str] = pa.Column(dtype=pa.STRING, nullable=True, checks=pa.Check(pathlib.Path.exists))
#     Filepath_R2: Series[str] = pa.Column(dtype=pa.STRING, nullable=True, checks=pa.Check(pathlib.Path.exists))
#     Filepath_VCF: Series[str] = pa.Column(dtype=pa.STRING, nullable=True, checks=pa.Check(pathlib.Path.exists))

    # @pa.check("Filepath_R1")
    # @pa.dataframe_check
    # def check_filepaths(cls, df: pd.Series) -> bool:
    #     return df.apply(lambda x: (
    #         (
    #             x["Start_Point"].upper() == "FASTQ" and
    #             (
    #                 isinstance(x["Filepath_R1"], str) and
    #                 os.path.exists(x["Filepath_R1"]) and
    #                 any(x["Filepath_R1"].endswith(ext) for ext in ALLOWED_UPLOAD_FILE_EXTENSIONS["FASTQ"])
    #             ) and
    #             (
    #                 isinstance(x["Filepath_R2"], str) and
    #                 os.path.exists(x["Filepath_R2"]) and
    #                 any(x["Filepath_R2"].endswith(ext) for ext in ALLOWED_UPLOAD_FILE_EXTENSIONS["FASTQ"])
    #             )
    #         ) or
    #         (x["Start_Point"].upper() == "VCF" and x["Filepath_R1"] =="" and x["Filepath_R2"] =="")
    #     ), axis=1)
    
import json
# Schema.validate(df, lazy=True)
sdf = df_schema.validate(df)
breakpoint()
# try:
#     Schema.validate(df, lazy=True)
# except pa.errors.SchemaErrors as e:
#     breakpoint()
#     print(json.dumps(e.message, indent=2))
# except Exception as ex:
#     print(f"An unexpected error occurred: {ex}")
