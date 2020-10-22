import subprocess

def convert(ch):
    """
    # uses ImageMagick to convert all images in directory to pdf. 

    Args:
        ch: chapter number.

    Returns:
        None.
    """
    subprocess.run(['convert', '*.png', f'{ch.zfill(4)}.pdf'])
