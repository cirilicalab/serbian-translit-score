from datasets import load_dataset
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser("Loads datasets from a huggingface repository to disk.")
    parser.add_argument("-r", "--repo", required=True, help="Huggingface dataset identifier - username/dastaset.")
    parser.add_argument("-d", "--datadir", required=True, help="Directory where the text will be extracted, if not already.")
    parser.add_argument("-f", "--fnamefield", required=True, help="Huggingface dataset identifier - username/dastaset.")
    parser.add_argument("-t", "--textfield", required=True, help="Directory where the text will be extracted, if not already.")
    return parser.parse_args()


def load_txt_from_dataset(name, out_dir, text_field, fname_field):
    # define folder name: replace "/" with "_"
    folder_name = name.replace("/", "_")
    target_dir = os.path.join(out_dir, folder_name)

    # if the folder exists, dont process
    if os.path.exists(target_dir):
        return

    # create dir
    os.makedirs(target_dir, exist_ok=True)

    # load dataset from Hugging Face (lazy)
    dataset = load_dataset(name, split="train", streaming=True) 

    # iterate over dataset and write each text to a file
    for i, item in enumerate(dataset):
        title = item.get(fname_field, f"sample_{i}")  # fallback if no title
        text = item.get(text_field, "")

        # sanitize filename
        safe_title = "".join(c if c.isalnum() else "_" for c in title)
        file_path = os.path.join(target_dir, f"{safe_title}.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

    print(f"Dataset {name} saved to {target_dir}")


if __name__ == "__main__":
    args = parse_args()
    repo_name = args.repo
    data_dir = args.datadir
    text_field = args.textfield
    fname_field = args.fnamefield
    load_txt_from_dataset(repo_name, data_dir, text_field, fname_field)
