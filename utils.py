import subprocess


def convert():
    """
    Uses ImageMagick to convert all images in directory to pdf. 

    Args:
        None

    Returns:
        None.
    """
    subprocess.run(['convert', '*.png', 'out.pdf'])


def clean():
    """
    Clean directory by removing downloaded images.

    Args:
        None.

    Returns:
        None.
    """
    subprocess.run(['rm', '*.png'])
