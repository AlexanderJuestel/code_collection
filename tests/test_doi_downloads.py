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


def test_get_website_content():
    from codes.doi_downloads import get_website_content

    website = get_website_content('https://se.copernicus.org/articles/%s/issue%s.html' % (1, 1))

    assert isinstance(website, str)


def test_create_earth_doc_url():
    from codes.doi_downloads import create_earth_doc_url

    url = create_earth_doc_url(conference_url='eageannual2021')

    assert url == 'https://www.earthdoc.org/content/proceedings/eageannual2021?page=1'

    url = create_earth_doc_url(conference_url='eageannual2021', page_number=2)

    assert url == 'https://www.earthdoc.org/content/proceedings/eageannual2021?page=2'

    url = create_earth_doc_url(conference_url='eageannual2021', titles_per_page=50)

    assert url == 'https://www.earthdoc.org/content/proceedings/eageannual2021?pageSize=50&page=1'

    url = create_earth_doc_url(conference_url='eageannual2021', titles_per_page=50, page_number=2)

    assert url == 'https://www.earthdoc.org/content/proceedings/eageannual2021?pageSize=50&page=2'
