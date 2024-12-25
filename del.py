import pandas as pd
import numpy as np

# Sample DataFrame
data = {
    "abc":[
        1,2,3,4,5,6
    ],
    "tag": [
        ["Rule-Engine-Check", "NO_DATA", "Rule-Engine-Check"],
        ["ont_oop", "ont_oop"],
        ["VCF-Test", "VCF-Test"],
        ["Rule-Engine-Check", "Rule-Engine-Check"],
        ["BT-4338", "oop_test", "BT-4338", "oop_test"],
        np.nan
    ]
}

all_sample_df = pd.DataFrame(data)
all_sample_df["tag"] = all_sample_df["tag"].apply(tuple)
# all_sample_df = all_sample_df.dropna(subset=['tag'])

# all_sample_df["tag"] = all_sample_df["tag"].apply(
#     lambda x: tuple(x) if isinstance(x, list) else x
# )

print(all_sample_df)
