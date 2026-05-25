import os
import pandas as pd

input_path = os.getenv("DATA_INPUT_PATH")
output_path = os.getenv("DATA_OUTPUT_PATH")

if not input_path or not output_path:
    raise EnvironmentError("Set DATA_INPUT_PATH and DATA_OUTPUT_PATH in your .env file")

df_cleaned = pd.read_csv(input_path, encoding='utf-8')
df_cleaned["review_comment_message"] = df_cleaned["review_comment_message"].astype(str).str.replace(r'[\n\r]+', ' ', regex=True)
df_cleaned.to_csv(output_path, index=False)

output_path