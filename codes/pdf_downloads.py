"""
Contributors: Alexander Jüstel

"""

from pathlib import Path
import requests


def download_pdf_copernicus(doi: str,
                            journal: str,
                            path: str = ''):
    """Function to download a freely accessible Copernicus Article as PDF

    Parameters:
    ___________

        doi: str
            DOI Number of the Copernicus Article

        journal: str
            Journal identifier

        path: str
            Folder name to download the PDF


    """

    # Checking that the DOI Number provided is of type string
    if not isinstance(doi, str):
        raise TypeError('DOI Number must be provided as string')

    # Checking that the correct journal identifier is provided
    if journal not in ['se',
                       'adgeo',
                       'gmd',
                       'esurf',
                       'esd',
                       'gc',
                       'gi',
                       'hess',
                       'nhess',
                       'npg',
                       'angeo',
                       'acp',
                       'amt',
                       'bg',
                       'cp',
                       'gchron',
                       'os',
                       'soil',
                       'tc'
                       'wcd']:
        raise ValueError('Journal identifier not recognized')

    # Getting the ending of the DOI Number
    ending = doi.split('https://doi.org/10.5194/')[1]

    # Extracting the volume, page numbers and the year
    volume, page_number, year = ending.split('%s-' % journal)[1].split('-')

    # Creating download URL
    url = 'https://se.copernicus.org/articles/%s/%s/%s/%s.pdf' % (volume, page_number, year, ending)

    # Downloading PDF
    Path('%s.pdf' % (path + ending)).write_bytes(requests.get(url).content)


def download_pdfs_copernicus(dois: list,
                             journal: str,
                             path: str = ''):
    """Function to download a freely accessible Copernicus Article as PDF

    Parameters:
    ___________

        dois: list
            List of DOI Numbers of the Copernicus Journal

        journal: str
            Journal identifier

        path: str
            Folder name to download the PDF


    """

    # Checking that the DOI Number provided is of type string
    if not isinstance(dois, list):
        raise TypeError('DOI Numbers must be provided as list')

    # Checking that the correct journal identifier is provided
    if journal not in ['se',
                       'adgeo',
                       'gmd',
                       'esurf',
                       'esd',
                       'gc',
                       'gi',
                       'hess',
                       'nhess',
                       'npg',
                       'angeo',
                       'acp',
                       'amt',
                       'bg',
                       'cp',
                       'gchron',
                       'os',
                       'soil',
                       'tc'
                       'wcd']:
        raise ValueError('Journal identifier not recognized')

    # Downloading all PDFs
    [download_pdf_copernicus(doi=doi,
                             journal=journal,
                             path=path) for doi in dois]
