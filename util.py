import numpy as np
from numpy import linalg as LA
import cv2


"""
Settings
"""

SAMPLING_UNIFORM = 2048 * 5
SAMPLING_POISSON = 2048

CONSTRUCT_ALPHA = 0.2

"""
Functions
"""

def show_depth_map(name: str, map: np.ndarray) -> None:
    image = 255 * (map / 4)
    image = image.astype(np.uint8)
    cv2.imshow(name, image)
    cv2.waitKey(1)

def show_normal_map(name: str, map: np.ndarray) -> None:
    image = 255 * (map * 0.5 + 0.5)
    image = image.astype(np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imshow(name, image)
    cv2.waitKey(1)

def write_depth_map(path: str, map: np.ndarray) -> None:
    image = 255 * (map / 4)
    image = image.astype(np.uint8)
    cv2.imwrite(path, image)
    cv2.waitKey(1)

def write_normal_map(path: str, map: np.ndarray) -> None:
    image = 255 * (map * 0.5 + 0.5)
    image = image.astype(np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, image)
    cv2.waitKey(1)

def normalize_pts(pts: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
    mean = pts.mean(axis=0)
    pts_ = pts - mean
    norm = LA.norm(pts_, axis=1).max() * 2
    pts_ = pts_ / norm
    return pts_, mean, norm
