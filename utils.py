import subprocess
import urllib.request


def get_pages(page_url_list):
    """
    Save manga pages to directory.

    Args:
        page_url_list: list of direct image links 

    Returns:
        None.
    """
    for page_url in page_url_list:
        filename = page_url.split('/')[-1]
        urllib.request.urlretrieve(page_url, filename)


def convert(ch):
    """
    Uses ImageMagick to convert all images in directory to pdf. 

    Args:
        ch: chapter number.

    Returns:
        None.
    """
    subprocess.run(['convert', '*.png', f'{ch.zfill(4)}.pdf'])
