"""
Contributors: Alexander Jüstel

"""

import pytest


def test_download_pdf_copernicus():
    from codes.pdf_downloads import download_pdf_copernicus

    download_pdf_copernicus(doi='https://doi.org/10.5194/se-1-1-2010',
                            journal='se')

    with pytest.raises(TypeError):
        doi = 123
        download_pdf_copernicus(doi=doi,
                                journal='se')

    with pytest.raises(ValueError):
        download_pdf_copernicus(doi='https://doi.org/10.5194/se-1-1-2010',
                                journal='sea')


def test_download_pdfs_copernicus():
    from codes.pdf_downloads import download_pdfs_copernicus

    download_pdfs_copernicus(dois=['https://doi.org/10.5194/se-1-1-2010'],
                             journal='se')

    with pytest.raises(TypeError):
        doi = 123
        download_pdfs_copernicus(dois=doi,
                                 journal='se')

    with pytest.raises(ValueError):
        download_pdfs_copernicus(dois=['https://doi.org/10.5194/se-1-1-2010'],
                                 journal='sea')
