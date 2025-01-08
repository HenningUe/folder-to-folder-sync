
import datetime as dt
from pathlib import Path
import re

from read_exif_data import read_exif_data


def rename_files(dst_dir: Path):
    files = read_files_with_wrong_names(dst_dir)
    files_metadata = read_exif_data(files)
    max_id_getter = MaxFileIdGetter(dst_dir)
    for f in files_metadata:
        date_taken_str = _convert_date_to_str(f.date_taken)
        max_id_str = max_id_getter.get_max_id_formatted(f.date_taken)
        new_name = f"{date_taken_str}_{max_id_str}{f.file.suffix}"
        new_path = dst_dir / new_name
        f.file.rename(new_path)


class MaxFileIdGetter:
    def __init__(self, src_dir: Path):
        self.src_dir = src_dir
        self.max_ids = dict()  # pylint: disable=use-dict-literal

    def get_max_id_formatted(self, date_taken: dt.datetime) -> str:
        max_id = self.get_max_id(date_taken)
        return str(max_id).zfill(3)

    def get_max_id(self, date_taken: dt.datetime) -> int:
        if date_taken not in self.max_ids:
            max_id_new = self._get_max_id_from_existing_files(date_taken)
            self.max_ids[date_taken] = max_id_new
        self.max_ids[date_taken] += 1
        return self.max_ids[date_taken]

    def _get_max_id_from_existing_files(self, date_taken: dt.datetime) -> int:
        date_taken = _convert_date_to_str(date_taken)
        cst_reg_cmp = re.compile(r"$.*?_(\d\d\d)")
        max_id = 0
        for f in self.src_dir.glob(f"{date_taken}_*.*"):
            match = cst_reg_cmp.match(f.stem)
            if match:
                max_id = max(int(match.group(1), max_id))
        return max_id

def _convert_date_to_str(date_taken: dt.datetime) -> str:
    return date_taken.strftime("%Y-%m-%d")

def read_files_with_wrong_names(src_dir: Path) -> list[Path]:
    files = []
    cst_reg_cmp = re.compile(r"[^-]")
    for f in src_dir.glob("*"):
        if f.is_file() and cst_reg_cmp.match(f.stem):
            files.append(f)
    return files
