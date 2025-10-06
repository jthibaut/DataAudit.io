import os


def save_uploaded_file(uploaded_file, target_dir: str) -> str:
    os.makedirs(target_dir, exist_ok=True)
    filename = uploaded_file.name
    output_path = os.path.join(target_dir, filename)
    with open(output_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return output_path