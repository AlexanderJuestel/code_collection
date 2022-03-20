"""
Contributors: Alexander Jüstel

"""

import numpy as np
import urllib3
from typing import List
import os


def get_website_content(url: str):
    """Function to retrieve data from a website

    Parameters
    __________

        url: str
            URL to the website

    """

    # Checking that the URL is of type string
    if not isinstance(url, str):
        raise TypeError('URL must be provided as string')

    # Connect to URL
    http_pool = urllib3.connection_from_url(url)

    # Open URL
    r = http_pool.urlopen('GET', url)

    # Getting the data
    website = r.data.decode('utf-8')

    return website


def download_dois_single_issue_copernicus(journal: str = '',
                                          volume: int = None,
                                          issue: int = None) -> List[str]:
    """Function to download the DOI numbers of one Solid Earth Issue of one Volume

    Parameters
    __________

        journal: str
            Journal identifier

        volume: int, np.integer
            Volume Number

        issue: int
            Issue Number

    """

    # Checking that the journal identifier is of type str
    if not isinstance(journal, str):
        raise TypeError('Journal identifier must be provided as string')

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

    # Checking that the volume number is of type int
    if not isinstance(volume, (int, np.integer)):
        raise TypeError('Volume Number must be of type int')

    # Checking that the issue number is of type int
    if journal != 'adgeo' and not isinstance(issue, (int, np.integer)):
        raise TypeError('Issue Number must be of type int')

    # Defining the URL with volume number and issue number
    if journal == 'adgeo':
        url = 'https://%s.copernicus.org/articles/%s/index.html' % (journal, volume)
    else:
        url = 'https://%s.copernicus.org/articles/%s/issue%s.html' % (journal, volume, issue)

    # Retrieving website data
    website = get_website_content(url)

    # Extracting the DOI numbers
    dois_copernicus = ['https://doi.org/10.5194' + website.split('https://doi.org/10.5194')[i + 1].split(',')[0] for i
                       in
                       range(len(website.split('https://doi.org/10.5194')) - 1)]

    return dois_copernicus


def download_dois_multiple_issues_copernicus(journal: str = '',
                                             volume: int = None,
                                             issue_start: int = None,
                                             issue_end: int = None) -> List[str]:
    """ Function to download the DOI numbers of multiple Solid Earth Issues of one Volume

    Parameters:
    ___________

        volume: int, np.integer
            Volume Number

        issue_start: int
            Issue Number Start

        issue_end: int
            Issue Number End

    """

    # Checking that the journal identifier is of type str
    if not isinstance(journal, str):
        raise TypeError('Journal identifier must be provided as string')

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

    # Checking that the volume number is of type int
    if not isinstance(volume, (int, np.integer)):
        raise TypeError('Volume Number must be of type int')

    # Checking that the issue number is of type int
    if journal != 'adgeo' and not isinstance(issue_start, int):
        raise TypeError('Issue Number Start must be of type int')

    # Checking that the issue number is of type int
    if journal != 'adgeo' and not isinstance(issue_end, (int, np.integer)):
        raise TypeError('Issue Number End must be of type int')

    # Defining range of issues
    step = 1
    issues = np.arange(issue_start, issue_end + 1, step)

    # Defining empty list to store DOI Numbers
    dois_copernicus = []

    # Extracting DOI Numbers for each issue and store them in a new list
    for issue_number in issues:
        dois_one_issue = download_dois_single_issue_copernicus(journal=journal,
                                                               volume=volume,
                                                               issue=issue_number)

        dois_copernicus = dois_copernicus + dois_one_issue

    return dois_copernicus


def download_dois_copernicus(journal: str = '',
                             volume_start: int = None,
                             volume_end: int = None) -> List[str]:
    """ Function to download the DOI numbers of multiple Solid Earth volumes

    Parameters:
    ___________

        volume_start: int
            Volume number start

        volume_end: int
            Volume number end

    """

    # Checking that the journal identifier is of type str
    if not isinstance(journal, str):
        raise TypeError('Journal identifier must be provided as string')

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

    # Checking that the volume number start is of type int
    if not isinstance(volume_start, int):
        raise TypeError('Volume Number Start must be of type int')

    # Checking that the volume number end is of type int
    if not isinstance(volume_end, int):
        raise TypeError('Volume Number End must be of type int')

    # Defining range of issues
    step = 1
    volumes = np.arange(volume_start, volume_end + 1, step)

    # Defining empty list to store DOI Numbers
    dois_copernicus = []

    # Extracting DOI Numbers for each issue and store them in a new list
    for volume_number in volumes:
        dois_one_issue = download_dois_multiple_issues_copernicus(journal=journal,
                                                                  volume=volume_number,
                                                                  issue_start=1,
                                                                  issue_end=20)

        dois_copernicus = dois_copernicus + dois_one_issue

    return dois_copernicus


def download_dois_earthdoc(conference_url: str,
                           titles_per_page: int = 20,
                           page_number_start: int = 1,
                           page_number_end: int = 100):
    """ Function to download EarthDoc DOI Numbers

    Parameters:
    ___________

        conference_url: str
           URL of the Conference

        titles_per_page: int
            Number of titles that are displayed on one page

        page_number_start: int
            Page Number Start

        page_number_end: int
            Page Number End

    """

    # Checking that the conference URL is of type string
    if not isinstance(conference_url, str):
        raise TypeError('The conference or workshop URL must be provided as string')

    # Checking that the titles per page value is of type int
    if not isinstance(titles_per_page, int):
        raise TypeError('The title of pages attribute must be of type int')

    # Checking that the page number start is of type int
    if not isinstance(page_number_start, int):
        raise TypeError('The page number start must be provided as int')

    # Checking that the page number end is of type int
    if not isinstance(page_number_end, int):
        raise TypeError('The page number end must be provided as int')

    # Checking that the titles per page attribute is only either 20, 50 or 100
    if titles_per_page not in [20, 50, 100]:
        raise ValueError('Please use only either 20, 50 or 100 as a value for the titles per page')

    # Creating array of pages
    pages = np.arange(page_number_start, page_number_end + 1, 1)

    # Creating empty list to store DOI numbers
    dois_earthdoc = []

    # Creating URLs and downloading DOIs
    for page in pages:
        url = create_earth_doc_url(conference_url=conference_url,
                                   titles_per_page=titles_per_page,
                                   page_number=page)

        website = get_website_content(url)

        doi_earthdoc = [
            website.split('content/papers/')[j + 1].split('data-itemId')[0].split('dir=')[0].split('/-->')[0].split(
                '>\n<i')[0].split('"')[0].split('>\n<i')[0].split(',http://')[0] for j in
            range(len(website.split('content/papers/')) - 1)]

        dois_earthdoc = dois_earthdoc + doi_earthdoc

    return dois_earthdoc


def create_earth_doc_url(conference_url: str, titles_per_page: int = 20, page_number: int = 1) -> str:
    """ Function to create an URL of a webpage containing EarthDoc DOI Numbers

    Parameters:
    ___________

        conference_url: str
           URL of the Conference

        titles_per_page: int
            Number of titles that are displayed on one page

        page_number: int
            Page Number

    """

    # Checking that the conference URL is of type string
    if not isinstance(conference_url, str):
        raise TypeError('The conference or workshop URL must be provided as string')

    # Checking that the titles per page value is of type int
    if not isinstance(titles_per_page, int):
        raise TypeError('The title of pages attribute must be of type int')

    # Checking that the page number is of type int
    if not isinstance(page_number, (int, np.integer)):
        raise TypeError('The page number must be provided as int')

    # Checking that the titles per page attribute is only either 20, 50 or 100
    if titles_per_page not in [20, 50, 100]:
        raise ValueError('Please use only either 20, 50 or 100 as a value for the titles per page')

    # Creating URL for 20 titles per page
    if titles_per_page == 20:
        url = 'https://www.earthdoc.org/content/proceedings/' + conference_url + '?page=' + str(page_number)
    else:
        url = 'https://www.earthdoc.org/content/proceedings/' + conference_url + '?pageSize=' + str(
            titles_per_page) + '&page=' + str(page_number)

    return url


def download_dois_single_volume_schweizerbart(journal: str = 'zdgg',
                                              volume_number: int = None) -> List[str]:
    """ FUnction to download the DOI numbers of one Schweizerbart Journal volume

    Parameters:
    ___________

        journal: str
            Journal identifier

        volume_number : int
            Volume number

    """

    # Checking that the volume number is of type int
    if not isinstance(volume_number, (int, np.integer)):
        raise TypeError('Volume Number must be of type int')

    # Checking that the journal identifier is of type str
    if not isinstance(journal, str):
        raise TypeError('Journal identifier must be provided as string')

    # Checking that the correct journal identifier is provided
    if journal not in ['zdgg', 'jber_oberrh', 'njgpa']:
        raise ValueError('Journal identifier not recognized')

    # Creating URL
    url = 'https://www.schweizerbart.de/papers/%s/list/%s' % (journal, volume_number)

    # Getting Website Data
    website = get_website_content(url=url)

    dois_schweizerbart = [website.split('DOI: ')[j + 1].split('\n')[0] for j in range(len(website.split('DOI: ')) - 1)]

    return dois_schweizerbart


def download_dois_multiple_volumes_schweizerbart(journal: str, volume_start: int, volume_end: int = 172) -> List[str]:
    """ Function to download DOI numbers of multiple Schweizerbart Journal volumes

    Parameters:
    ___________

        journal: str
            Journal identifier

        volume_start: int
            Volume number start

        volume_end: int
            Volume number end

    """

    # Checking that the journal identifier is of type str
    if not isinstance(journal, str):
        raise TypeError('Journal identifier must be provided as string')

    # Checking that the correct journal identifier is provided
    if journal not in ['zdgg', 'jber_oberrh', 'njgpa']:
        raise ValueError('Journal identifier not recognized')

    # Checking that the volume number start is of type int
    if not isinstance(volume_start, int):
        raise TypeError('Volume Number Start must be of type int')

    # Checking that the volume number end is of type int
    if not isinstance(volume_end, int):
        raise TypeError('Volume Number End must be of type int')

    # Defining range of issues
    step = 1
    volumes = np.arange(volume_start, volume_end + 1, step)

    # Defining empty list to store DOI Numbers
    dois_schweizerbart = []

    # Extracting DOI Numbers for each issue and store them in a new list
    for volume_number in volumes:
        dois_single_issue = download_dois_single_volume_schweizerbart(journal=journal,
                                                                      volume_number=volume_number)

        dois_schweizerbart = dois_schweizerbart + dois_single_issue

    return dois_schweizerbart


def download_doi_one_page_hindawi_journal(journal: str,
                                          year: int,
                                          page_number: int) -> list:
    """Function to download the DOI Number for on Hindawi Journal Article

    Parameters:
    ___________

        journal: str
            Journal identifier

        year: int
            Year of the Hindawi journal article

        page_number: int
            Page number on the Hindawi Journal page

    """

    # Checking that the journal identifier is of type str
    if not isinstance(journal, str):
        raise TypeError('Journal identifier must be provided as string')

    # Checking that the year is of type int
    if not isinstance(year, (int, np.integer)):
        raise TypeError('The year must be provided as type int')

    # Checking that the page number is of type int
    if not isinstance(page_number, (int, np.integer)):
        raise TypeError('The page number must be provided as int')

    # Creating URL
    url = 'https://www.hindawi.com/journals/%s/contents/year/%s/page/%s/' % (journal, year, page_number)

    # Getting website content
    website = get_website_content(url=url)

    # Extracting the DOI numbers
    dois_one_page_hindawi = [
        'https://doi.org/10.1155/%s/' % year + website.split('Article ID ')[i + 1].split('</li>')[0] for i
        in range(len(website.split('Article ID ')) - 1)]

    return dois_one_page_hindawi


def download_dois_multiple_pages_hindawi_journal(journal: str,
                                                 year: int,
                                                 page_number_start: int,
                                                 page_number_end: int) -> list:
    """

    Parameters:
    ___________

        journal: str
            Journal identifier

        year: int
            Year on the Hindawi journal articles

        page_number_start: int
            Page number start on the Hindawi Journal page

        page_number_end: int
            Page number end on the Hindawi Journal page

    """

    # Checking that the journal identifier is of type str
    if not isinstance(journal, str):
        raise TypeError('Journal identifier must be provided as string')

    # Checking that the year is of type int
    if not isinstance(year, (int, np.integer)):
        raise TypeError('The year must be provided as type int')

    # Checking that the page number start is of type int
    if not isinstance(page_number_start, (int, np.integer)):
        raise TypeError('The page number start must be provided as int')

    # Checking that the page number end is of type int
    if not isinstance(page_number_end, (int, np.integer)):
        raise TypeError('The page number end must be provided as int')

    # Creating empty list for DOI Numbers
    dois_hindawi = []

    # Creating array of pages
    pages = np.arange(page_number_start, page_number_end + 1, 1)

    # Extracting DOI Numbers
    for page in pages:
        dois_single_page = download_doi_one_page_hindawi_journal(journal=journal,
                                                                  year=year,
                                                                  page_number=page)

        dois_hindawi = dois_hindawi + dois_single_page

    return dois_hindawi


def download_dois_hindawi_journal(journal: str,
                                  year_start: int,
                                  year_end: int,
                                  page_number_start: int = 1,
                                  page_number_end: int = 20) -> list:
    """

        Parameters:
        ___________

            journal: str
                Journal identifier

            year: int
                Year on the Hindawi journal articles

            page_number_start: int
                Page number start on the Hindawi Journal page

            page_number_end: int
                Page number end on the Hindawi Journal page

        """

    # Checking that the journal identifier is of type str
    if not isinstance(journal, str):
        raise TypeError('Journal identifier must be provided as string')

    # Checking that the year start is of type int
    if not isinstance(year_start, int):
        raise TypeError('The year start must be provided as type int')

    # Checking that the year end is of type int
    if not isinstance(year_end, int):
        raise TypeError('The year end must be provided as type int')

    # Checking that the page number start is of type int
    if not isinstance(page_number_start, (int, np.integer)):
        raise TypeError('The page number start must be provided as int')

    # Checking that the page number end is of type int
    if not isinstance(page_number_end, (int, np.integer)):
        raise TypeError('The page number end must be provided as int')

    # Creating empty list for DOI Numbers
    dois_hindawi = []

    # Creating array of years
    years = np.arange(year_start, year_end + 1, 1)

    # Extracting DOI Numbers
    for year in years:
        dois_multiple_pages = download_dois_multiple_pages_hindawi_journal(journal=journal,
                                                                           year=year,
                                                                           page_number_start=page_number_start,
                                                                           page_number_end=page_number_end)

        dois_hindawi = dois_hindawi + dois_multiple_pages

    return dois_hindawi


def save_doi_numbers(list_dois: list,
                     path: str = None):
    """Function to save list of DOIs to a text file

    Parameters:
    ___________

        list_dois: list
            List containing the DOI numbers

        path: str
            Path where file is being saved

    """

    # Checking that the list of DOI numbers is of type list
    if not isinstance(list_dois, list):
        raise TypeError('List of DOIs must be provided as list')

    # Checking that the path is of type string
    if not isinstance(path, (str, type(None))):
        raise TypeError('Path must be of type string')

    # Setting a path if path es None
    if isinstance(path, type(None)):
        path = os.path.abspath(os.getcwd()) + 'DOIs.txt'

    # Save DOI Numbers as text file
    with open(path, 'w') as f:
        for doi in list_dois:
            f.write("%s\n" % doi)

    print('DOIs successfully saved to disc')
