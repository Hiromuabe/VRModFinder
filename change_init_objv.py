import glob
import gzip
import json
import multiprocessing
import os
import urllib.request
import warnings
from typing import Any, Dict, List, Optional, Tuple
import re

from tqdm import tqdm
BASEPATH = os.path.join("static","object")

__version__ = "0.0.7"
# _VERSIONED_PATH = os.path.join(BASE_PATH, "hf-objaverse-v1")


def load_annotations(uids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Load the full metadata of all objects in the dataset.

    Args:
        uids: A list of uids with which to load metadata. If None, it loads
        the metadata for all uids.
    """
    metadata_path = os.path.join(BASEPATH, "metadata")
    object_paths = _load_object_paths()
    dir_ids = (
        set([object_paths[uid].split("/")[1] for uid in uids])
        if uids is not None
        else [f"{i // 1000:03d}-{i % 1000:03d}" for i in range(160)]
    )
    if len(dir_ids) > 10:
        dir_ids = tqdm(dir_ids)
    out = {}
    for i_id in dir_ids:
        json_file = f"{i_id}.json.gz"
        local_path = os.path.join(metadata_path, json_file)
        if not os.path.exists(local_path):
            hf_url = f"https://huggingface.co/datasets/allenai/objaverse/resolve/main/metadata/{i_id}.json.gz"
            # wget the file and put it in local_path
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            urllib.request.urlretrieve(hf_url, local_path)
        with gzip.open(local_path, "rb") as f:
            data = json.load(f)
        if uids is not None:
            data = {uid: data[uid] for uid in uids if uid in data}
        out.update(data)
        if uids is not None and len(out) == len(uids):
            break
    return out


def _load_object_paths() -> Dict[str, str]:
    """Load the object paths from the dataset.

    The object paths specify the location of where the object is located
    in the Hugging Face repo.

    Returns:
        A dictionary mapping the uid to the object path.
    """
    object_paths_file = "object-paths.json.gz"
    local_path = os.path.join(BASEPATH, object_paths_file)
    if not os.path.exists(local_path):
        hf_url = f"https://huggingface.co/datasets/allenai/objaverse/resolve/main/{object_paths_file}"
        # wget the file and put it in local_path
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        urllib.request.urlretrieve(hf_url, local_path)
    with gzip.open(local_path, "rb") as f:
        object_paths = json.load(f)
    return object_paths


def load_uids() -> List[str]:
    """Load the uids from the dataset.

    Returns:
        A list of uids.
    """
    return list(_load_object_paths().keys())


def _download_object(
    uid: str,
    object_path: str,
    total_downloads: float,
    start_file_count: int,
) -> Tuple[str, str]:
    """Download the object for the given uid.

    Args:
        uid: The uid of the object to load.
        object_path: The path to the object in the Hugging Face repo.

    Returns:
        The local path of where the object was downloaded.
    """
    # print(f"downloading {uid}")
    pattern = r'glbs/\d+-\d+/'
    object_path2 = re.sub(pattern,"",object_path)
    local_path = os.path.join(BASEPATH, object_path2)
    print(local_path)
    tmp_local_path = os.path.join(BASEPATH, object_path2 + ".tmp")
    #tmp_local_path2 = os.path.join(BASEPATH, object_path2 + ".tmp")
    print(tmp_local_path)
    hf_url = (
        f"https://huggingface.co/datasets/allenai/objaverse/resolve/main/{object_path}"
    )
    # wget the file and put it in local_path
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    urllib.request.urlretrieve(hf_url, tmp_local_path)

    os.rename(tmp_local_path, local_path)
    files = glob.glob(os.path.join(BASEPATH, "glbs", "*", "*.glb"))
    print(f"files: {files}")
    print(
        "Downloaded",
        len(files) - start_file_count,
        "/",
        total_downloads,
        "objects",
    )

    return uid, local_path


def load_objects(uids: List[str]) -> Dict[str, str]:
    object_paths = _load_object_paths()
    out = {}
    uids_to_download = []
    for uid in uids:
        if uid.endswith(".glb"):
            uid = uid[:-4]
        if uid not in object_paths:
            warnings.warn(f"Could not find object with uid {uid}. Skipping it.")
            continue
        object_path = object_paths[uid]
        local_path = os.path.join(BASEPATH, object_path)
        if os.path.exists(local_path):
            out[uid] = local_path
            continue
        uids_to_download.append((uid, object_path))
        
    if len(uids_to_download) == 0:
        return out

    start_file_count = len(glob.glob(os.path.join(BASEPATH, "glbs", "*", "*.glb")))
    for uid, object_path in uids_to_download:
        uid, local_path = _download_object(uid, object_path, len(uids_to_download), start_file_count)
        out[uid] = local_path
    return out



def load_lvis_annotations() -> Dict[str, List[str]]:
    """Load the LVIS annotations.

    If the annotations are not already downloaded, they will be downloaded.

    Returns:
        A dictionary mapping the LVIS category to the list of uids in that category.
    """
    hf_url = f"https://huggingface.co/datasets/allenai/objaverse/resolve/main/lvis-annotations.json.gz"
    local_path = os.path.join(BASEPATH, "lvis-annotations.json.gz")
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if not os.path.exists(local_path):
        urllib.request.urlretrieve(hf_url, local_path)
    with gzip.open(local_path, "rb") as f:
        lvis_annotations = json.load(f)
    return lvis_annotations


if __name__ == "__main__":
    object_paths = _load_object_paths()
    uids = [k for k, v in object_paths.items() if v.startswith("glbs/000-000")][
        500:1000
    ]
    load_annotations(uids)
    print(f"Loaded {len(uids)} uids")
    objects = load_objects(uids, download_processes=10)
    print(f"Loaded {len(objects)} objects")
