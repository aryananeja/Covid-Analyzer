"""
This module contains the Tree class, along Tree methods and functions used to store world COVID
data in an instance of the Tree class. The Tree will have the following general structure:
World -> Continents -> Countries -> COVID data.
This means, as the root of our Tree, we will
have the world. Its subtrees will be the Trees for each of the continents. Similarly, each
continent Tree's subtrees will contain Trees for each of the countries in the respective
continents. Finally, each country Tree will contain one subtree which will store that country's
COVID data in a nested dictionary format.
The format of COVID data dictionary is as follows:
{<month + year>: {'Total cases': <cases>, 'Total deaths': <deaths>, 'Total vaccinations':
<vaccinations>, 'Population': <population>}} (this will be the case for each month from
January 2020 till April 2024, wherever the data is available).
"""
from __future__ import annotations

import csv
from typing import Any, Optional


# from python_ta.contracts import check_contracts


# @check_contracts
class Tree:
    """A recursive tree data structure.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this
    #       attribute may be empty when self._root is not None, which represents
    #       a tree consisting of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]

    # @check_contracts
    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    # @check_contracts
    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    # @check_contracts
    def __contains__(self, item: Any) -> bool:
        """Return whether the given is in this tree.

        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.__contains__(1)
        True
        >>> t.__contains__(5)
        True
        >>> t.__contains__(4)
        False
        """
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False

    # @check_contracts
    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.
        """
        return self._str_indented(0).rstrip()

    # @check_contracts
    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self._root}\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    # @check_contracts
    def __repr__(self) -> str:
        """Return a one-line string representation of this tree.

        >>> t = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> t
        Tree(2, [Tree(4, []), Tree(5, [])])
        >>> t2 = Tree(5, [Tree(8, [Tree(3, []), Tree(2, []), Tree(6, [])]), Tree(10, []), \
        Tree(7, [Tree(0, [Tree(111, [])])])])
        >>> t2
        Tree(5, [Tree(8, [Tree(3, []), Tree(2, []), Tree(6, [])]), Tree(10, []), \
Tree(7, [Tree(0, [Tree(111, [])])])])
        """
        if self.is_empty():
            return ''
        else:
            subtrees_repr_list = []
            for subtree in self._subtrees:
                subtrees_repr_list.append(subtree.__repr__())
            subtrees_repr = ', '.join(subtrees_repr_list)
            return f'Tree({self._root}, [{subtrees_repr}])'

    # @check_contracts
    def insert_sequence(self, items: list) -> None:
        """Insert the given items into this tree.

        The inserted items form a chain of descendants, where:
            - items[0] is a child of this tree's root
            - items[1] is a child of items[0]
            - items[2] is a child of items[1]
            - etc.

        Do nothing if items is empty.

        The root of this chain (i.e. items[0]) should be added as a new subtree within
        this tree, as long as items[0] does not already exist as a child of the current
        root node. That is, create a new subtree for it and append it to this tree's
        existing list of subtrees.

        If items[0] is already a child of this tree's root, instead recurse into that
        existing subtree rather than create a new subtree with items[0]. If there are
        multiple occurrences of items[0] within this tree's children, pick the left-most
        subtree with root value items[0] to recurse into.

        Preconditions:
            - not self.is_empty()

        >>> t = Tree(111, [])
        >>> t.insert_sequence([1, 2, 3])
        >>> print(t)
        111
          1
            2
              3
        >>> t.insert_sequence([1, 3, 5])
        >>> print(t)
        111
          1
            2
              3
            3
              5
        """
        if items == []:
            return
        elif self._index_child(items[0]) >= 0:
            index = self._index_child(items[0])
            self._subtrees[index].insert_sequence(items[1:])
        else:
            self._insert_subtree(items)  # this helper method is recursive

    # @check_contracts
    def _index_child(self, item: Any) -> int:
        """
        Return the index of the subtree of this Tree has <item> as its root, if any.
        If no such subtree exists, return -1.

        Preconditions:
            - not self.is_empty()

        >>> t = Tree(5, [Tree(8, [Tree(3, []), Tree(2, []), Tree(6, [])]), Tree(10, []), \
        Tree(7, [Tree(0, [Tree(111, [])])])])
        >>> t._index_child(8)
        0
        >>> t._index_child(4)
        -1
        """
        for i in range(len(self._subtrees)):
            if self._subtrees[i]._root == item:
                return i
        return -1

    # @check_contracts
    def _insert_subtree(self, items: list) -> None:
        """
        Recursively insert a subtree into the _subtrees attribute of this Tree.

        Preconditions:
            - not self.is_empty()
        """
        if items == []:
            return
        else:
            self._subtrees.append(Tree(items[0], []))
            self._subtrees[len(self._subtrees) - 1]._insert_subtree(items[1:])

    # @check_contracts
    def get_region_tree(self, region: str = "world") -> Optional[Tree]:
        """Return the COVID data Tree from the world COVID data Tree corresponding to the region (the Tree which has
        region as its root). If this region cannot be found in the world COVID data Tree, return None. By default, the
        region is "world," so if no region is specified, the entire world COVID data Tree will be returned. Note that
        this region search only extends down till the level of continents.

        Preconditions:
            - not self.is_empty()
            - region.lower() in ['world', 'north america', 'south america', 'africa', 'europe', 'asia', 'oceania']
            - self._root == 'World'
        """
        if self._subtrees[0]._subtrees == []:
            return None
        if self._root.lower() == region:
            return self
        else:
            for subtree in self._subtrees:
                if subtree.get_region_tree(region) is not None:
                    return subtree
            return None

    #
    # @check_contracts
    def get_cases(self, month_year: str) -> dict[str, int]:
        """Return a dictionary mapping country names to the total number of COVID cases recorded in that country up
        till the date (month and year) specified by month_year.

        Preconditions:
            - not self.is_empty()
            - month_year.split(' ')[0].lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december']
            - month_year.split(' ')[1] in ['20', '21', '22', '23', '24']
        """
        if self._subtrees[0]._subtrees == []:
            country_data = self._subtrees[0]._root
            if month_year in country_data:
                return {self._root: country_data[month_year]['Total cases']}
            else:
                return {self._root: 0}
        else:
            cases_data = {}
            for subtree in self._subtrees:
                cases_data.update(subtree.get_cases(month_year))
            return cases_data

    # @check_contracts
    def get_deaths(self, month_year: str) -> dict[str, int]:
        """Return a dictionary mapping country names to the total number of COVID deaths recorded in that country up
        till the date (month and year) specified by month_year.

        Preconditions:
            - not self.is_empty()
            - month_year.split(' ')[0].lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december']
            - month_year.split(' ')[1] in ['20', '21', '22', '23', '24']
        """
        if self._subtrees[0]._subtrees == []:
            country_data = self._subtrees[0]._root
            if month_year in country_data:
                return {self._root: country_data[month_year]['Total deaths']}
            else:
                return {self._root: 0}
        else:
            cases_data = {}
            for subtree in self._subtrees:
                cases_data.update(subtree.get_deaths(month_year))
            return cases_data

    # @check_contracts
    def get_vaccinations(self, month_year: str) -> dict[str, int]:
        """Return a dictionary mapping country names to the total number of COVID vaccine doses administered in that
        country up till the date (month and year) specified by month_year.

        Preconditions:
            - not self.is_empty()
            - month_year.split(' ')[0].lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december']
            - month_year.split(' ')[1] in ['20', '21', '22', '23', '24']
        """
        if self._subtrees[0]._subtrees == []:
            country_data = self._subtrees[0]._root
            if month_year in country_data:
                return {self._root: country_data[month_year]['Total vaccinations']}
            else:
                return {self._root: 0}
        else:
            cases_data = {}
            for subtree in self._subtrees:
                cases_data.update(subtree.get_vaccinations(month_year))
            return cases_data

    # @check_contracts
    def get_cases_normalised(self, month_year: str) -> dict[str, int]:
        """Return a dictionary mapping country names to the total number of COVID cases recorded in that country
        as a percentage of the country's population i.e., total number of COVID cases up till the date (month and year)
        specified by month_year relative to the country's population.

        Preconditions:
            - not self.is_empty()
            - month_year.split(' ')[0].lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december']
            - month_year.split(' ')[1] in ['20', '21', '22', '23', '24']
        """
        if self._subtrees[0]._subtrees == []:
            country_data = self._subtrees[0]._root
            if month_year in country_data:
                total_cases = country_data[month_year]['Total cases']
                population = country_data[month_year]['Population']
                return {self._root: total_cases / population}
            else:
                return {self._root: 0}
        else:
            cases_data = {}
            for subtree in self._subtrees:
                cases_data.update(subtree.get_cases_normalised(month_year))
            return cases_data

    # @check_contracts
    def get_deaths_normalised(self, month_year: str) -> dict[str, int]:
        """Return a dictionary mapping country names to the total number of COVID deaths recorded in that country
        as a percentage of the country's population i.e., total number of COVID deaths up till the date (month and
        year) specified by month_year relative to the country's population.

        Preconditions:
            - not self.is_empty()
            - month_year.split(' ')[0].lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december']
            - month_year.split(' ')[1] in ['20', '21', '22', '23', '24']
        """
        if self._subtrees[0]._subtrees == []:
            country_data = self._subtrees[0]._root
            if month_year in country_data:
                total_deaths = country_data[month_year]['Total deaths']
                population = country_data[month_year]['Population']
                return {self._root: total_deaths / population}
            else:
                return {self._root: 0}
        else:
            cases_data = {}
            for subtree in self._subtrees:
                cases_data.update(subtree.get_deaths_normalised(month_year))
            return cases_data

    # @check_contracts
    def get_vaccinations_normalised(self, month_year: str) -> dict[str, int]:
        """Return a dictionary mapping country names to the total number of COVID vaccine doses administered in that
        country as a percentage of the country's population i.e., total number of COVID vaccine doses administered
        up till the date (month and year) specified by month_year relative to the country's population.

        Preconditions:
            - not self.is_empty()
            - month_year.split(' ')[0].lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december']
            - month_year.split(' ')[1] in ['20', '21', '22', '23', '24']
        """
        if self._subtrees[0]._subtrees == []:
            country_data = self._subtrees[0]._root
            if month_year in country_data:
                total_vaccinations = country_data[month_year]['Total vaccinations']
                population = country_data[month_year]['Population']
                return {self._root: total_vaccinations / population}
            else:
                return {self._root: 0}
        else:
            cases_data = {}
            for subtree in self._subtrees:
                cases_data.update(subtree.get_vaccinations_normalised(month_year))
            return cases_data


# @check_contracts
def build_covid_tree(covid_data_csv_file: str) -> Tree:
    """Return a Tree containing the COVID data given in covid_data_csv_file.

    Preconditions:
        - covid_data_csv_file is the path to a csv file containing COVID data
    """
    covid_tree = Tree('World', [])
    months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    with open(covid_data_csv_file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skip the header row
        country = "Afghanistan"
        continent = "Asia"
        country_data = {}
        total_vaccinations = 0
        for row in reader:
            if row[3] != country:
                # add data to tree (insert sequence)
                covid_tree.insert_sequence([continent, country, country_data])
                country_data = {}
                total_vaccinations = 0

            # read new row
            month, year = get_date(row[4])
            continent = row[2]
            country = row[3]
            total_cases = int(row[5])
            total_deaths = int(row[6])
            if int(row[7]) != 0:
                total_vaccinations = int(row[7])
            key = months[month] + " " + str(year)
            country_data[key] = {
                "Total cases": total_cases,
                "Total deaths": total_deaths,
                "Total vaccinations": total_vaccinations,
                "Population": int(row[8])
            }
        # insert the last country's data
        covid_tree.insert_sequence([continent, country, country_data])

    return covid_tree


# @check_contracts
def get_date(date: str) -> tuple[int, int]:
    """
    Return the month and year (as integers) of <date>, given in
    string format as DD-MM-YY.
    """
    month = int(date[5:7])
    year = int(date[0:4])
    return (month, year)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'max-nested-blocks': 4,
        'extra-imports': ['csv']
    })

    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'disable': ['E1136'],
    #     'extra-imports': ['csv', 'networkx'],
    #     'allowed-io': ['load_review_graph'],
    #     'max-nested-blocks': 4
    # })
