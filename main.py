"""Main file to execute the final project."""
from FINAL import final_testing

if __name__ == "__main__":
    final_testing.covid_visualisation()

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    # import doctest
    # doctest.testmod()

    import python_ta

    python_ta.check_all()
