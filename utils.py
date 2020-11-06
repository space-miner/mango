import os


def convert_to_pdf(filename='out'):
    '''
    Uses ImageMagick to convert all images in directory to pdf. 

    Args:
        None

    Returns:
        None.
    '''
    os.system(f'convert *.png {filename}.pdf')
    print(f'Created {filename}.pdf')


def remove_images():
    '''
    Clean directory by removing downloaded images.

    Args:
        None.

    Returns:
        None.
    '''
    os.system('rm *.png')
    print('Images have been removed.')


def clear_screen():
    '''
    Clear terminal screen.

    Args:
        None.

    Returns:
        None.
    '''
    os.system('clear')


def download_content(url):
    '''
    Downloads content of url to a file

    Args:
        url: Link to content.

    Returns:
        None.
    '''
    filename = url.split('/')
    os.system(f'curl {url} -o {filename}')
    print(f'Saving {filename}.png.')
