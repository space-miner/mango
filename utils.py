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
