"""
DAISO path translation — convert between NFS (Linux) and Samba (Windows UNC) paths.

Usage:
    from paths import nfs_path

    # On Windows: returns \\\\sc8-samba.sc.intel.com\\nfs\\site\\disks\\mfg_nvl_016\\...
    # On Linux:   returns /nfs/site/disks/mfg_nvl_016/...
    p = nfs_path("/nfs/site/disks/mfg_nvl_016/amaraaba/run_area")

Configuration priority:
    1. DAISO_SAMBA_SERVER env var
    2. .daiso-sync.conf (dest= line, extracts server from UNC path)
    3. Default: sc8-samba.sc.intel.com
"""

import os
import platform
import re

_DEFAULT_SAMBA = "sc8-samba.sc.intel.com"
_NFS_PREFIX = "/nfs/"

# Intel site → Samba server mapping
# Source: https://wiki.ith.intel.com/spaces/HPCTraining/pages/1803211685/How+do+I+access+Samba
SAMBA_SERVERS = {
    "png":  "samba.png.intel.com",
    "iind-ec": "inecsamba.iind.intel.com",
    "ims":  "samba.ims.intel.com",
    "inn":  "samba.inn.intel.com",
    "ir":   "samba.ir.intel.com",
    "iir":  "iir-samba.ir.intel.com",
    "sie":  "sie-samba.ir.intel.com",
    "imu":  "samba.imu.intel.com",
    "ka":   "samba.ka.intel.com",
    "tor":  "samba.tor.intel.com",
    "jf":   "samba.jf.intel.com",
    "iind": "samba.iind.intel.com",
    "an":   "samba.an.intel.com",
    "fm":   "samba.fm.intel.com",
    "vc":   "samba.vc.intel.com",
    "igk":  "samba.igk.intel.com",
    "pdx":  "samba.pdx.intel.com",
    "gm":   "gmssamba.zpn.intel.com",
    "cr":   "samba.cr.intel.com",
    "hd":   "samba.hd.intel.com",
    "iil":  "samba.iil.intel.com",
    "lc":   "samba.lc.intel.com",
    "aw":   "samba.aw.intel.com",
    "ch":   "samba.ch.intel.com",
    "sc":   "samba.sc.intel.com",
    "sc1":  "sc1-samba.sc.intel.com",
    "sc3":  "sc3-samba.sc.intel.com",
    "sc4":  "sc4-samba.sc.intel.com",
    "sc5":  "sc5-samba.sc.intel.com",
    "sc6":  "sc6-samba.sc.intel.com",
    "sc8":  "sc8-samba.sc.intel.com",
    "zsc2": "samba.zsc2.intel.com",
    "zsc3": "samba.zsc3.intel.com",
    "zsc7": "samba.zsc7.intel.com",
    "zsc9": "samba.zsc9.intel.com",
    "zsc10": "samba.zsc10.intel.com",
    "zsc11": "samba.zsc11.intel.com",
    "zsc12": "samba.zsc12.intel.com",
    "zsc14": "samba.zsc14.intel.com",
    "zsc15": "samba.zsc15.intel.com",
    "zsc16": "samba.zsc16.intel.com",
    "zsc18": "samba.zsc18.intel.com",
    "zsc22": "samba.zsc22.intel.com",
    "zsc24": "samba.zsc24.intel.com",
    "zsc28": "samba.zsc28.intel.com",
    "zsc97": "samba.zsc97.intel.com",
    "zsc98": "samba.zsc98.intel.com",
    "sc-oc6": "samba-oc6.sc.intel.com",
}


def _read_samba_from_config() -> str:
    """Extract samba server from .daiso-sync.conf if it exists."""
    # Walk up from this file to find repo root
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(5):
        conf = os.path.join(here, ".daiso-sync.conf")
        if os.path.isfile(conf):
            with open(conf, "r") as f:
                for line in f:
                    m = re.match(r"^dest=\\\\([^\\]+)\\", line.strip())
                    if m:
                        return m.group(1)
            break
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    return _DEFAULT_SAMBA


def _get_samba_server() -> str:
    """Get samba server from env or config."""
    return os.environ.get("DAISO_SAMBA_SERVER", "") or _read_samba_from_config()


def get_samba_for_site(site: str) -> str:
    """Look up the Samba server for an Intel site code (e.g. 'iil', 'sc8', 'png').
    Returns the server hostname, or raises ValueError if not found.
    """
    key = site.lower().strip()
    if key in SAMBA_SERVERS:
        return SAMBA_SERVERS[key]
    raise ValueError(
        f"Unknown site '{site}'. Known sites: {', '.join(sorted(SAMBA_SERVERS))}"
    )


def nfs_path(path: str) -> str:
    """Translate a path for the current platform.

    - Linux paths starting with /nfs/ are converted to UNC on Windows.
    - UNC paths are converted to /nfs/ on Linux.
    - Non-NFS paths are returned unchanged.
    """
    is_windows = platform.system() == "Windows"

    if path.startswith(_NFS_PREFIX):
        if is_windows:
            # /nfs/site/disks/X → \\samba\nfs\site\disks\X
            server = _get_samba_server()
            return "\\\\" + server + "\\" + path[1:].replace("/", "\\")
        return path  # already native

    if path.startswith("\\\\"):
        if not is_windows:
            # \\server\nfs\site\disks\X → /nfs/site/disks/X
            # Strip \\server\ prefix, keep from \nfs\ onward
            m = re.match(r"^\\\\[^\\]+\\(nfs\\.*)$", path)
            if m:
                return "/" + m.group(1).replace("\\", "/")
        return path  # already native

    return path  # not an NFS path


def nfs_to_unc(path: str, server: str = "") -> str:
    """Explicitly convert /nfs/... to UNC, regardless of platform."""
    if not path.startswith(_NFS_PREFIX):
        return path
    srv = server or _get_samba_server()
    return "\\\\" + srv + "\\" + path[1:].replace("/", "\\")


def unc_to_nfs(path: str) -> str:
    """Explicitly convert UNC \\\\server\\nfs\\... to /nfs/..., regardless of platform."""
    m = re.match(r"^\\\\[^\\]+\\(nfs\\.*)$", path)
    if m:
        return "/" + m.group(1).replace("\\", "/")
    return path
