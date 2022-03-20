"""
Contributors: Alexander Jüstel

"""

import pytest
import sys
import numpy as np
sys.path.insert(0, '../')


def test_get_website_content():
    from codes.doi_downloads import get_website_content

    website = get_website_content('https://se.copernicus.org/articles/%s/issue%s.html' % (1, 1))

    assert isinstance(website, str)


def test_download_dois_single_issue_copernicus():
    from codes.doi_downloads import download_dois_single_issue_copernicus

    dois_se = download_dois_single_issue_copernicus(journal='se',
                                                    volume=1,
                                                    issue=1)
    assert isinstance(dois_se, list)
    assert all(isinstance(doi, str) for doi in dois_se)


def test_download_dois_multiple_issues_copernicus():
    from codes.doi_downloads import download_dois_multiple_issues_copernicus

    dois_se = download_dois_multiple_issues_copernicus(journal='se',
                                                       volume=7,
                                                       issue_start=1,
                                                       issue_end=2)
    assert isinstance(dois_se, list)
    assert all(isinstance(doi, str) for doi in dois_se)


def test_download_dois_copernicus():
    from codes.doi_downloads import download_dois_copernicus

    dois_se = download_dois_copernicus(journal='se',
                                       volume_start=1,
                                       volume_end=2)
    assert isinstance(dois_se, list)
    assert all(isinstance(doi, str) for doi in dois_se)


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


def test_download_dois_earthdoc():
    from codes.doi_downloads import download_dois_earthdoc

    dois_eage = download_dois_earthdoc(conference_url='eageannual2021', page_number_start=1, page_number_end=2)

    assert isinstance(dois_eage, list)
    assert all(isinstance(doi, str) for doi in dois_eage)


def test_download_dois_single_volume_schweizerbart():
    from codes.doi_downloads import download_dois_single_volume_schweizerbart

    dois_zdgg = download_dois_single_volume_schweizerbart(journal='zdgg',
                                                          volume_number=150)

    assert isinstance(dois_zdgg, list)
    assert all(isinstance(doi, str) for doi in dois_zdgg)


def test_download_dois_multiple_volumes_schweizerbart():
    from codes.doi_downloads import download_dois_multiple_volumes_schweizerbart

    dois_zdgg = download_dois_multiple_volumes_schweizerbart(journal='zdgg',
                                                             volume_start=150,
                                                             volume_end=151)

    assert isinstance(dois_zdgg, list)
    assert all(isinstance(doi, str) for doi in dois_zdgg)
