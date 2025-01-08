
from pathlib import Path

from rename_acc_to_date import rename_files
from simplefilemirror import handler

from media_to_folder_sync import _get_dir

def sync_files(src_dir: Path, dst_dir: Path):
    rename_files(src_dir)
    dir_getter = _get_dir.DirectoryGetter()
    simplefilemirror.mirror(dir_getter.get_src_dir(),
                            dir_getter.get_trg_dir())          
