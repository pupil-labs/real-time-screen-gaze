import json
import logging
import sys
from typing import List
from pathlib import Path

import requests

from .camera_models import Radial_Dist_Camera

if sys.version_info < (3, 8):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict


def load_camera_intrinsics(
    serial_number_scene_cam: str,
    api_endpoint: str = "https://api.cloud.pupil-labs.com/hardware/{}/calibration.v1?json",
) -> "CloudIntrinsics":
    cache_file = Path(f"cache/intrinsics.{serial_number_scene_cam}.json")
    cache_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(cache_file) as fh:
            return json.load(fh)
    except FileNotFoundError:
        url = api_endpoint.format(serial_number_scene_cam)
        resp = requests.get(url)
        resp.raise_for_status()
        intrinsics: CloudIntrinsics = resp.json()["result"]
        try:
            with open(cache_file, "w") as fh:
                json.dump(intrinsics, fh)
        except OSError:
            logging.warning(f"Unable to cache intrinsics to {cache_file}")
        return intrinsics


def camera_for_scene_cam_serial(
    serial_number_scene_cam: str = "default",
) -> Radial_Dist_Camera:
    intrinsics_scene_cam = load_camera_intrinsics(serial_number_scene_cam)
    return Radial_Dist_Camera(
        name='Scene',
        resolution=(1, 1),
        K=intrinsics_scene_cam["camera_matrix"],
        D=intrinsics_scene_cam["dist_coefs"],
    )


class CloudIntrinsics(TypedDict):
    camera_matrix: List[List[float]]
    dist_coefs: List[List[float]]
    rotation_matrix: List[List[float]]
    serial_number: str
    version: str