"""
Contributors: Alexander Jüstel

"""

import pytest

def test_download_dois_one_issue_solid_earth():
    from codes.doi_downloads import download_dois_one_issue_solid_earth

    dois_se = download_dois_one_issue_solid_earth(volume=1, issue=1)
    assert isinstance(dois_se, list)
    assert all(isinstance(doi, str) for doi in dois_se)


def test_download_dois_multiple_issues_solid_earth():
    from codes.doi_downloads import download_dois_multiple_issues_solid_earth

    dois_se = download_dois_multiple_issues_solid_earth(volume=7,
                                                        issue_start=1,
                                                        issue_end=5)
    assert isinstance(dois_se, list)
    assert all(isinstance(doi, str) for doi in dois_se)


def test_download_dois_solid_earth():
    from codes.doi_downloads import download_dois_solid_earth

    dois_se = download_dois_solid_earth(volume_start=1,
                                        volume_end=4)
    assert isinstance(dois_se, list)
    assert all(isinstance(doi, str) for doi in dois_se)





