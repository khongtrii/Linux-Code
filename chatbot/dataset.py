import pandas as pd
from huggingface_hub import login
from datasets import load_dataset


def load_data(access, url, pack, mode, output_json):
    
    access_token = access
    login(token=access_token)
    if pack is None:
        ds = load_dataset(url)
    else:
        ds = load_dataset(url, pack)
    data = ds[mode].to_json(output_json)    
    data = pd.read_json(output_json, lines=True)

    return data

# if __name__ == "__main__":
#     access = "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"
#     url = "lmsys/chatbot_arena_conversations"
#     pack = None
#     mode = "train"
#     output_json = 'tmp.json'

#     data = load_data(access, url, pack, mode, output_json)