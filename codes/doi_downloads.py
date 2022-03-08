"""
Contributors: Alexander Jüstel

"""

import numpy as np
import urllib3
import os
from typing import List


def download_dois_one_issue_solid_earth(volume: int,
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

    # Connect to URL
    http_pool = urllib3.connection_from_url(url)

    # Open URL
    r = http_pool.urlopen('GET', url)

    # Getting the data
    website = r.data.decode('utf-8')

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
        dois_one_issue = download_dois_one_issue_solid_earth(volume=volume,
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
