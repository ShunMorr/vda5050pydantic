from datamodel_code_generator import generate
from pathlib import Path
import glob

input_dir = Path("./json_schemas")

for input_file in glob.glob("./json_schemas/*.schema"):
    input_path = Path(input_file)
    output_path = Path(f"./pydantic_models/{input_path.stem}.py")
    print(f"generate {output_path} from {input_path}")
    generate(
        input_=input_path,
        output=output_path,
        input_file_type="jsonschema"
    )