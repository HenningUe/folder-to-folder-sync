
from dataclasses import dataclass
import datetime as dt
from pathlib import Path
from collections import abc

import exiftool

@dataclass
class ExifData:
    file: Path
    date_taken: dt.datetime


def read_exif_data(files: abc.Iterable[Path | str]) -> list[ExifData]:

    def to_dt(str_in):
        return dt.datetime.strptime(str_in, '%Y:%m:%d %H:%M:%S')

    exif_data_all = []
    p_dir = Path(__file__).parent
    exiftool_exe = p_dir / "exiftool" / "exiftool(-k).exe"
    with exiftool.ExifToolHelper(executable=str(exiftool_exe)) as et:
        for f in files:
            metadata = et.get_metadata(str(f))
            date_taken = to_dt(metadata["EXIF:CreateDate"])
            exif_data = ExifData(file=Path(f), date_taken=date_taken)
            exif_data_all.append(exif_data)
    return exif_data_all


if __name__ == "__main__":
    p_dir_ = Path(__file__).parent
    files_test = ["IMG_8884.jpg", "IMG_8887.png"]
    files_test = [str(p_dir_/f) for f in files_test]
    read_exif_data(files_test)
