import subprocess

from pytest import approx
import json
from pathlib import Path
def ffprobe_sync(filein: Path) -> dict:
    """ get media metadata """
    meta = subprocess.check_output(['ffprobe', '-v', 'warning','-print_format', 'json','-show_streams','-show_format',str(filein)], universal_newlines = True)
    return json.loads(meta)


def test_duration():
    fnin = 'in\\11.mp4'
    fnin2 = 'in\\22.mp4'
    fnout = 'out\\480_11.mp4'
    fnout2 = 'out\\720_11.mp4'
    fnout3 = 'out\\480_22.mp4'
    fnout4 = 'out\\720_22.mp4'

    orig_meta = ffprobe_sync(fnin)
    orig_duration = float(orig_meta['streams'][0]['duration'])

    meta_480 = ffprobe_sync(fnout)
    duration_480 = float(meta_480['streams'][0]['duration'])
    meta_720 = ffprobe_sync(fnout2)
    duration_720 = float(meta_720['streams'][0]['duration'])

    orig_meta = ffprobe_sync(fnin2)
    orig_duration1 = float(orig_meta['streams'][0]['duration'])

    meta_480 = ffprobe_sync(fnout3)
    duration_480_22 = float(meta_480['streams'][0]['duration'])
    meta_720 = ffprobe_sync(fnout4)
    duration_720_22 = float(meta_720['streams'][0]['duration'])
    assert orig_duration == approx(duration_480) == approx(duration_720)
    assert orig_duration1 == approx(duration_480_22) == approx(duration_720_22)
