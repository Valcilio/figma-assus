# -*- coding: utf-8 -*-

# TEMPLATE_NAME = context
# TEMPLATE_VERSION = 0.0.2

from datetime import datetime
import os
import logging
from pathlib import Path
import re
import sys

# Look for file **.proj_root**
found_root = False
cur_path = Path(__file__).parent

for depth in range(5):
    list_files = os.listdir(cur_path)

    # If we don't find .proj_root in list_files, look in the folder 
    # above
    if '.proj_root' not in list_files:
        cur_path /= '..'
        continue

    # Solve PROJ_DIR and change var found_root
    PROJ_DIR = cur_path.resolve()
    found_root = True
    break

# Check if PROJ_DIR was found
if not found_root:
    raise RuntimeError("Project root folder not found. Please check if "
                       "the file ** .proj_root ** exists."
    )

# Initiate Logging Feature
handlers=[
    logging.FileHandler(PROJ_DIR / 'proj_log.log'),
    logging.FileHandler(PROJ_DIR /
                        'logs' /
                        'proj_log_{}.log'.format(
                            datetime.now().strftime("%Y%m%d%H%M%S")
                        )
                       ),
    logging.StreamHandler()
]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s (%(levelname)s)	||| %(message)s',
    handlers=handlers
)

# Add references to Project Folders
DATA_FLD = PROJ_DIR / 'data'
DATA_EXT_FLD = DATA_FLD / 'external'
DATA_INT_FLD = DATA_FLD / 'interim'
DATA_PROC_FLD = DATA_FLD / 'processed'
DATA_RAW_FLD = DATA_FLD / 'raw'

NB_FLD = PROJ_DIR / 'notebooks'
REPORT_FLD = PROJ_DIR / 'reports'
SRC_FLD = PROJ_DIR / 'src'
RESOURCES_FLD = SRC_FLD / 'resources'

FIG_FLD = REPORT_FLD / 'figures'

# Add reference to HOME_FLD
if 'USERPROFILE' in os.environ:
    HOME_FLD = Path(os.environ['USERPROFILE'])
elif 'HOME' in os.environ:
    HOME_FLD = Path(os.environ['HOME'])
else:
    logging.warning("Cannot find the HOME / USERPROFILE folder.")

# Adding source folder to Python Path
sys.path.insert(0, str(SRC_FLD))


def get_last_file(folder: str or Path, regexp: str):
    """ get_last_file(folder: str or Path, regexp: str)

    Get last file in a directory. It will:
      1. List all files in directory;
      2. Filter the files using the regexp;
      3. Capture the last file using the max() function;

    Ideally, this function is used to get the last timestamp in a group
        of file.

    Parameters
    ==========
        folder: str or Path
        regex: str

    Returns
    =======
        Path, containing: `folder / file`
    """

    PATH = Path(folder)
    files = os.listdir(PATH)
    FILE = max([f for f in files if re.match(regexp, f)])

    return PATH / FILE
