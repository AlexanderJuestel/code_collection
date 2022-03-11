"""
Contributors: Alexander Jüstel

"""

import numpy as np
import urllib3
from typing import List


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


def download_dois_single_issue_solid_earth(volume: int,
                                           issue: int) -> List[str]:
    """Function to download the DOI numbers of one Solid Earth Issue of one Volume

    Parameters
    __________

        volume: int, np.int32
            Volume Number

        issue: int
            Issue Number

    """

    # Checking that the volume number is of type int
    if not isinstance(volume, (int, np.int32)):
        raise TypeError('Volume Number must be of type int')

    # Checking that the issue number is of type int
    if not isinstance(issue, (int, np.int32)):
        raise TypeError('Issue Number must be of type int')

    # Defining the URL with volume number and issue number
    url = 'https://se.copernicus.org/articles/%s/issue%s.html' % (volume, issue)

    # Retrieving website data
    website = get_website_content(url)

    # Extracting the DOI numbers
    dois_se = ['https://doi.org/10.5194' + website.split('https://doi.org/10.5194')[i + 1].split(',')[0] for i in
               range(len(website.split('https://doi.org/10.5194')) - 1)]

    return dois_se


def download_dois_multiple_issues_solid_earth(volume: int,
                                              issue_start: int = 1,
                                              issue_end: int = 20) -> List[str]:
    """ Function to download the DOI numbers of multiple Solid Earth Issues of one Volume

    Parameters:
    ___________

        volume: int, np.int32
            Volume Number

        issue_start: int
            Issue Number Start

        issue_end: int
            Issue Number End

    """

    # Checking that the volume number is of type int
    if not isinstance(volume, (int, np.int32)):
        raise TypeError('Volume Number must be of type int')

    # Checking that the issue number is of type int
    if not isinstance(issue_start, int):
        raise TypeError('Issue Number Start must be of type int')

    # Checking that the issue number is of type int
    if not isinstance(issue_end, int):
        raise TypeError('Issue Number End must be of type int')

    # Defining range of issues
    step = 1
    issues = np.arange(issue_start, issue_end + 1, step)

    # Defining empty list to store DOI Numbers
    dois_se = []

    # Extracting DOI Numbers for each issue and store them in a new list
    for issue_number in issues:
        dois_one_issue = download_dois_single_issue_solid_earth(volume=volume,
                                                                issue=issue_number)

        dois_se = dois_se + dois_one_issue

    return dois_se


def download_dois_solid_earth(volume_start: int = 1,
                              volume_end: int = 13) -> List[str]:
    """ Function to download the DOI numbers of multiple Solid Earth volumes

    Parameters:
    ___________

        volume_start: int
            Volume number start

        volume_end: int
            Volume number end

    """

    # Checking that the volume number start is of type int
    if not isinstance(volume_start, int):
        raise TypeError('Volume Number Start must be of type int')

    # Checking that the volume number end is of type int
    if not isinstance(volume_end, int):
        raise TypeError('Volume Number End must be of type int')

    # Checking that the current volume is at 13
    if volume_end > 13:
        raise ValueError('The current latest volume is number 13')

    # Defining range of issues
    step = 1
    volumes = np.arange(volume_start, volume_end + 1, step)

    # Defining empty list to store DOI Numbers
    dois_se = []

    # Extracting DOI Numbers for each issue and store them in a new list
    for volume_number in volumes:
        dois_one_issue = download_dois_multiple_issues_solid_earth(volume=volume_number,
                                                                   issue_start=1,
                                                                   issue_end=20)

        dois_se = dois_se + dois_one_issue

    return dois_se


def download_dois_earthdoc(conference_url: str, titles_per_page: int = 20, page_number_start: int = 1,
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
    if not isinstance(page_number, (int, np.int32)):
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


def download_dois_single_volume_zdgg(volume_number: int) -> List[str]:
    """ FUnction to download the DOI numbers of one ZDGG volume

    Parameters:
    ___________

        volume_number : int
            Volume number

    """

    # Checking that the volume number is of type int
    if not isinstance(volume_number, (int, np.int32)):
        raise TypeError('Volume Number must be of type int')

    # Creating URL
    url = 'https://www.schweizerbart.de/papers/zdgg/list/%s' % volume_number

    # Getting Website Data
    website = get_website_content(url=url)

    dois_zdgg = [website.split('DOI: ')[j + 1].split('\n')[0] for j in range(len(website.split('DOI: ')) - 1)]

    return dois_zdgg


def download_dois_single_volume_jmogv(volume_number: int) -> List[str]:
    """ FUnction to download the DOI numbers of one JMOGV volume

    Parameters:
    ___________

        volume_number : int
            Volume number

    """

    # Checking that the volume number is of type int
    if not isinstance(volume_number, (int, np.int32)):
        raise TypeError('Volume Number must be of type int')

    # Creating URL
    url = 'https://www.schweizerbart.de/papers/jber_oberrh/list/%s' % volume_number

    # Getting Website Data
    website = get_website_content(url=url)

    dois_jmogv = [website.split('DOI: ')[j+1].split('\n')[0] for j in range(len(website.split('DOI: '))-1)]

    return dois_jmogv


def download_dois_multiple_volumes_zdgg(volume_start: int, volume_end: int = 172) -> List[str]:
    """ Function to download DOI numbers of multiple ZDGG volumes

    Parameters:
    ___________

        volume_start: int
            Volume number start

        volume_end: int
            Volume number end

    """

    # Checking that the volume number start is of type int
    if not isinstance(volume_start, int):
        raise TypeError('Volume Number Start must be of type int')

    # Checking that the volume number end is of type int
    if not isinstance(volume_end, int):
        raise TypeError('Volume Number End must be of type int')

    # Checking that the current volume is at 13
    if volume_end > 172:
        raise ValueError('The current latest volume is number 172')

    # Defining range of issues
    step = 1
    volumes = np.arange(volume_start, volume_end + 1, step)

    # Defining empty list to store DOI Numbers
    dois_zdgg = []

    # Extracting DOI Numbers for each issue and store them in a new list
    for volume_number in volumes:
        dois_single_issue = download_dois_single_volume_zdgg(volume_number=volume_number)

        dois_zdgg = dois_zdgg + dois_single_issue

    return dois_zdgg


def download_dois_multiple_volumes_jmogv(volume_start: int, volume_end: int = 172) -> List[str]:
    """ Function to download DOI numbers of multiple JMOGV volumes

    Parameters:
    ___________

        volume_start: int
            Volume number start

        volume_end: int
            Volume number end

    """

    # Checking that the volume number start is of type int
    if not isinstance(volume_start, int):
        raise TypeError('Volume Number Start must be of type int')

    # Checking that the volume number end is of type int
    if not isinstance(volume_end, int):
        raise TypeError('Volume Number End must be of type int')

    # Checking that the current volume is at 13
    if volume_end > 103:
        raise ValueError('The current latest volume is number 103')

    # Defining range of issues
    step = 1
    volumes = np.arange(volume_start, volume_end + 1, step)

    # Defining empty list to store DOI Numbers
    dois_jmogv = []

    # Extracting DOI Numbers for each issue and store them in a new list
    for volume_number in volumes:
        dois_single_issue = download_dois_single_volume_jmogv(volume_number=volume_number)

        dois_jmogv = dois_jmogv + dois_single_issue

    return dois_jmogv


def download_dois_single_volume_njgpa(volume_number: int) -> List[str]:
    """ FUnction to download the DOI numbers of one NJGPA volume

    Parameters:
    ___________

        volume_number : int
            Volume number

    """

    # Checking that the volume number is of type int
    if not isinstance(volume_number, (int, np.int32)):
        raise TypeError('Volume Number must be of type int')

    # Creating URL
    url = 'https://www.schweizerbart.de/papers/njgpa/list/%s' % volume_number

    # Getting Website Data
    website = get_website_content(url=url)

    dois_njgpa = [website.split('DOI: ')[j+1].split('\n')[0] for j in range(len(website.split('DOI: '))-1)]

    return dois_njgpa


def download_dois_multiple_volumes_njgpa(volume_start: int, volume_end: int = 172) -> List[str]:
    """ Function to download DOI numbers of multiple NJGPA volumes

    Parameters:
    ___________

        volume_start: int
            Volume number start

        volume_end: int
            Volume number end

    """

    # Checking that the volume number start is of type int
    if not isinstance(volume_start, int):
        raise TypeError('Volume Number Start must be of type int')

    # Checking that the volume number end is of type int
    if not isinstance(volume_end, int):
        raise TypeError('Volume Number End must be of type int')

    # Checking that the current volume is at 13
    if volume_end > 303:
        raise ValueError('The current latest volume is number 303')

    # Defining range of issues
    step = 1
    volumes = np.arange(volume_start, volume_end + 1, step)

    # Defining empty list to store DOI Numbers
    dois_njgpa = []

    # Extracting DOI Numbers for each issue and store them in a new list
    for volume_number in volumes:
        dois_single_issue = download_dois_single_volume_njgpa(volume_number=volume_number)

        dois_njgpa = dois_njgpa + dois_single_issue

    return dois_njgpa


def save_doi_numbers(list_dois: list,
                     path: str):
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
    if not isinstance(path, str):
        raise TypeError('Path must be of type string')

    # Save DOI Numbers as text file
    with open(path, 'w') as f:
        for doi in list_dois:
            f.write("%s\n" % doi)

    print('DOIs successfully saved to disc')
