"""
Contributors: Alexander Jüstel

"""

import pytest
import sys

sys.path.insert(0, '../')


def test_get_website_content():
    from codes.doi_downloads import get_website_content

    website = get_website_content(url='https://se.copernicus.org/articles/%s/issue%s.html' % (1, 1))

    assert isinstance(website, str)

    url = 123

    with pytest.raises(TypeError):
        website = get_website_content(url=url)


def test_download_dois_single_issue_copernicus():
    from codes.doi_downloads import download_dois_single_issue_copernicus

    dois_se = download_dois_single_issue_copernicus(journal='se',
                                                    volume=1,
                                                    issue=1)
    assert isinstance(dois_se, list)
    assert all(isinstance(doi, str) for doi in dois_se)

    with pytest.raises(TypeError):
        se = 123
        dois_se = download_dois_single_issue_copernicus(journal=se,
                                                        volume=1,
                                                        issue=1)

    with pytest.raises(ValueError):
        dois_se = download_dois_single_issue_copernicus(journal='sea',
                                                        volume=1,
                                                        issue=1)

    with pytest.raises(TypeError):
        dois_se = download_dois_single_issue_copernicus(journal='se',
                                                        volume=1.1,
                                                        issue=1)
    with pytest.raises(TypeError):
        dois_se = download_dois_single_issue_copernicus(journal='se',
                                                        volume=1,
                                                        issue=1.1)

    dois_adgeo = download_dois_single_issue_copernicus(journal='adgeo',
                                                       volume=1,
                                                       issue=1)
    assert isinstance(dois_adgeo, list)
    assert all(isinstance(doi, str) for doi in dois_adgeo)


def test_download_dois_multiple_issues_copernicus():
    from codes.doi_downloads import download_dois_multiple_issues_copernicus

    dois_se = download_dois_multiple_issues_copernicus(journal='se',
                                                       volume=7,
                                                       issue_start=1,
                                                       issue_end=2)
    assert isinstance(dois_se, list)
    assert all(isinstance(doi, str) for doi in dois_se)

    with pytest.raises(TypeError):
        se = 123
        dois_se = download_dois_multiple_issues_copernicus(journal=se,
                                                           volume=1,
                                                           issue_start=1,
                                                           issue_end=2)

    with pytest.raises(ValueError):
        dois_se = download_dois_multiple_issues_copernicus(journal='sea',
                                                           volume=1,
                                                           issue_start=1,
                                                           issue_end=2)

    with pytest.raises(TypeError):
        dois_se = download_dois_multiple_issues_copernicus(journal='se',
                                                           volume=1.1,
                                                           issue_start=1,
                                                           issue_end=2)
    with pytest.raises(TypeError):
        dois_se = download_dois_multiple_issues_copernicus(journal='se',
                                                           volume=1,
                                                           issue_start=1.1,
                                                           issue_end=2)

    with pytest.raises(TypeError):
        dois_se = download_dois_multiple_issues_copernicus(journal='se',
                                                           volume=1,
                                                           issue_start=1,
                                                           issue_end=2.1)


    dois_adgeo = download_dois_multiple_issues_copernicus(journal='adgeo',
                                                          volume=1,
                                                          issue_start=1,
                                                          issue_end=2)
    assert isinstance(dois_adgeo, list)
    assert all(isinstance(doi, str) for doi in dois_adgeo)


def test_download_dois_copernicus():
    from codes.doi_downloads import download_dois_copernicus

    dois_se = download_dois_copernicus(journal='se',
                                       volume_start=1,
                                       volume_end=2)
    assert isinstance(dois_se, list)
    assert all(isinstance(doi, str) for doi in dois_se)

    with pytest.raises(TypeError):
        se = 123
        dois_se = download_dois_copernicus(journal=se,
                                           volume_start=1,
                                           volume_end=2)
    with pytest.raises(ValueError):
        dois_se = download_dois_copernicus(journal='sea',
                                           volume_start=1,
                                           volume_end=2)

    with pytest.raises(TypeError):
        dois_se = download_dois_copernicus(journal='se',
                                           volume_start=1.1,
                                           volume_end=2)

    with pytest.raises(TypeError):
        dois_se = download_dois_copernicus(journal='se',
                                           volume_start=1,
                                           volume_end=2.1)


def test_create_earth_doc_url():
    from codes.doi_downloads import create_earth_doc_url

    url = create_earth_doc_url(conference_url='eageannual2021')

    assert url == 'https://www.earthdoc.org/content/proceedings/eageannual2021?page=1'

    url = create_earth_doc_url(conference_url='eageannual2021', page_number=2)

    assert url == 'https://www.earthdoc.org/content/proceedings/eageannual2021?page=2'

    url = create_earth_doc_url(conference_url='eageannual2021', titles_per_page=20)

    assert url == 'https://www.earthdoc.org/content/proceedings/eageannual2021?page=1'

    url = create_earth_doc_url(conference_url='eageannual2021', titles_per_page=50)

    assert url == 'https://www.earthdoc.org/content/proceedings/eageannual2021?pageSize=50&page=1'

    url = create_earth_doc_url(conference_url='eageannual2021', titles_per_page=50, page_number=2)

    assert url == 'https://www.earthdoc.org/content/proceedings/eageannual2021?pageSize=50&page=2'

    with pytest.raises(TypeError):
        conference_url = 123
        url = create_earth_doc_url(conference_url=conference_url)

    with pytest.raises(TypeError):
        url = create_earth_doc_url(conference_url='eageannual2021',
                                   titles_per_page='50')

    with pytest.raises(TypeError):
        url = create_earth_doc_url(conference_url='eageannual2021',
                                   titles_per_page=50,
                                   page_number='2')

    with pytest.raises(ValueError):
        url = create_earth_doc_url(conference_url='eageannual2021',
                                   titles_per_page=200)


def test_download_dois_earthdoc():
    from codes.doi_downloads import download_dois_earthdoc

    dois_eage = download_dois_earthdoc(conference_url='eageannual2021', page_number_start=1, page_number_end=2)

    assert isinstance(dois_eage, list)
    assert all(isinstance(doi, str) for doi in dois_eage)

    with pytest.raises(TypeError):
        conference_url = 123
        dois_eage = download_dois_earthdoc(conference_url=conference_url,
                                           page_number_start=1,
                                           page_number_end=2)

    with pytest.raises(TypeError):
        dois_eage = download_dois_earthdoc(conference_url='eageannual2021',
                                           titles_per_page='50',
                                           page_number_start=1,
                                           page_number_end=2)

    with pytest.raises(TypeError):
        dois_eage = download_dois_earthdoc(conference_url='eageannual2021',
                                           titles_per_page=50,
                                           page_number_start=1.1,
                                           page_number_end=2)

    with pytest.raises(TypeError):
        dois_eage = download_dois_earthdoc(conference_url='eageannual2021',
                                           titles_per_page=50,
                                           page_number_start=1,
                                           page_number_end=2.1)

    with pytest.raises(ValueError):
        dois_eage = download_dois_earthdoc(conference_url='eageannual2021',
                                           titles_per_page=200,
                                           page_number_start=1,
                                           page_number_end=2)


def test_download_dois_single_volume_schweizerbart():
    from codes.doi_downloads import download_dois_single_volume_schweizerbart

    dois_zdgg = download_dois_single_volume_schweizerbart(journal='zdgg',
                                                          volume_number=150)

    assert isinstance(dois_zdgg, list)
    assert all(isinstance(doi, str) for doi in dois_zdgg)

    with pytest.raises(TypeError):
        journal = 123
        dois_zdgg = download_dois_single_volume_schweizerbart(journal=journal,
                                                              volume_number=150)

    with pytest.raises(TypeError):
        dois_zdgg = download_dois_single_volume_schweizerbart(journal='zdgg',
                                                              volume_number=150.1)

    with pytest.raises(ValueError):
        dois_zdgg = download_dois_single_volume_schweizerbart(journal='zdggg',
                                                              volume_number=150)


def test_download_dois_multiple_volumes_schweizerbart():
    from codes.doi_downloads import download_dois_multiple_volumes_schweizerbart

    dois_zdgg = download_dois_multiple_volumes_schweizerbart(journal='zdgg',
                                                             volume_start=150,
                                                             volume_end=151)

    assert isinstance(dois_zdgg, list)
    assert all(isinstance(doi, str) for doi in dois_zdgg)

    with pytest.raises(TypeError):
        journal = 123
        dois_zdgg = download_dois_multiple_volumes_schweizerbart(journal=journal,
                                                                 volume_start=150,
                                                                 volume_end=151)

    with pytest.raises(ValueError):
        dois_zdgg = download_dois_multiple_volumes_schweizerbart(journal='zdggg',
                                                                 volume_start=150,
                                                                 volume_end=151)

    with pytest.raises(TypeError):
        dois_zdgg = download_dois_multiple_volumes_schweizerbart(journal='zdgg',
                                                                 volume_start=150.1,
                                                                 volume_end=151)

    with pytest.raises(TypeError):
        dois_zdgg = download_dois_multiple_volumes_schweizerbart(journal='zdgg',
                                                                 volume_start=150,
                                                                 volume_end=151.1)


def test_download_doi_one_page_hindawi_journal():
    from codes.doi_downloads import download_doi_one_page_hindawi_journal

    dois_geo = download_doi_one_page_hindawi_journal(journal='geofluids',
                                                     year=2022,
                                                     page_number=1)

    assert isinstance(dois_geo, list)
    assert all(isinstance(doi, str) for doi in dois_geo)

    with pytest.raises(TypeError):
        journal = 123
        dois_geo = download_doi_one_page_hindawi_journal(journal=journal,
                                                         year=2022,
                                                         page_number=1)

    with pytest.raises(TypeError):
        dois_geo = download_doi_one_page_hindawi_journal(journal='geofluids',
                                                         year=2022.2,
                                                         page_number=1)

    with pytest.raises(TypeError):
        dois_geo = download_doi_one_page_hindawi_journal(journal='geofluids',
                                                         year=2022,
                                                         page_number=1.1)


def test_download_dois_multiple_pages_hindawi_journal():
    from codes.doi_downloads import download_dois_multiple_pages_hindawi_journal

    dois_geo = download_dois_multiple_pages_hindawi_journal(journal='geofluids',
                                                            year=2022,
                                                            page_number_start=1,
                                                            page_number_end=2)

    assert isinstance(dois_geo, list)
    assert all(isinstance(doi, str) for doi in dois_geo)

    with pytest.raises(TypeError):
        journal = 123
        dois_geo = download_dois_multiple_pages_hindawi_journal(journal=journal,
                                                                year=2022,
                                                                page_number_start=1,
                                                                page_number_end=2)

    with pytest.raises(TypeError):
        dois_geo = download_dois_multiple_pages_hindawi_journal(journal='geofluids',
                                                                year=2022.2,
                                                                page_number_start=1,
                                                                page_number_end=2)

    with pytest.raises(TypeError):
        dois_geo = download_dois_multiple_pages_hindawi_journal(journal='geofluids',
                                                                year=2022,
                                                                page_number_start=1.1,
                                                                page_number_end=2)

    with pytest.raises(TypeError):
        dois_geo = download_dois_multiple_pages_hindawi_journal(journal='geofluids',
                                                                year=2022,
                                                                page_number_start=1,
                                                                page_number_end=2.1)


def test_download_dois_hindawi_journal():
    from codes.doi_downloads import download_dois_hindawi_journal

    dois_geo = download_dois_hindawi_journal(journal='geofluids',
                                             year_start=2021,
                                             year_end=2022,
                                             page_number_start=1,
                                             page_number_end=2)

    assert isinstance(dois_geo, list)
    assert all(isinstance(doi, str) for doi in dois_geo)

    with pytest.raises(TypeError):
        journal = 123
        dois_geo = download_dois_hindawi_journal(journal=journal,
                                                 year_start=2021,
                                                 year_end=2022,
                                                 page_number_start=1,
                                                 page_number_end=2)

    with pytest.raises(TypeError):
        dois_geo = download_dois_hindawi_journal(journal='geofluids',
                                                 year_start=2021.2,
                                                 year_end=2022,
                                                 page_number_start=1,
                                                 page_number_end=2)

    with pytest.raises(TypeError):
        dois_geo = download_dois_hindawi_journal(journal='geofluids',
                                                 year_start=2021,
                                                 year_end=2022.2,
                                                 page_number_start=1,
                                                 page_number_end=2)

    with pytest.raises(TypeError):
        dois_geo = download_dois_hindawi_journal(journal='geofluids',
                                                 year_start=2021,
                                                 year_end=2022,
                                                 page_number_start=1.1,
                                                 page_number_end=2)

    with pytest.raises(TypeError):
        dois_geo = download_dois_hindawi_journal(journal='geofluids',
                                                 year_start=2021,
                                                 year_end=2022,
                                                 page_number_start=1,
                                                 page_number_end=2.1)


def test_save_doi_numbers():
    from codes.doi_downloads import save_doi_numbers

    save_doi_numbers(list_dois=['1', '2'],
                     path=None)

    save_doi_numbers(list_dois=['1', '2'],
                     path='../DOIs.txt')

    with pytest.raises(TypeError):
        save_doi_numbers(list_dois='1')

    with pytest.raises(TypeError):
        path = 123
        save_doi_numbers(list_dois=['1', '2'],
                         path=path)