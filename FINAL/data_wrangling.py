"""Python code to clean and wrangle the data."""
import pandas as pd
import geopandas as gpd


def clean_data(file_path: str) -> None:
    """
    Function to clean the data from the csv file.
    Return None.
    """
    covid = pd.read_csv(file_path)

    new_covid = covid[['iso_code', 'continent', 'location', 'date',
                       'total_cases', 'total_deaths', 'total_vaccinations',
                       'population']]

    new_covid['total_cases'] = new_covid['total_cases'].fillna(0)
    new_covid['total_deaths'] = new_covid['total_deaths'].fillna(0)
    new_covid['total_vaccinations'] = new_covid['total_vaccinations'].fillna(0)

    #

    int_cols = ['total_cases', 'total_deaths',
                'total_vaccinations', 'population']
    new_covid[int_cols] = new_covid[int_cols].astype(int)

    new_covid_final = new_covid.dropna(subset=['continent', 'location'])

    new_covid_final.reset_index(inplace=True)
    new_covid_final.index += 1
    new_covid_final.index.name = 'index'
    #

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    country_names = world.set_index('iso_a3')['name'].to_dict()

    for iso_code, country_name in country_names.items():
        new_covid_final.loc[
            new_covid_final['iso_code'] == iso_code, 'location'] = country_name

    new_covid_final = (
        new_covid_final)[new_covid_final['location'] != 'W. Sahara']
    new_covid_final['location'].replace("Côte d'Ivoire",
                                        "Cote d'Ivoire", inplace=True)
    new_covid_final.to_csv("FINAL/FINAL_TESTING_filtered_data_1.csv", index=False)


if __name__ == '__main__':
    # import python_ta.contracts
    #
    # python_ta.contracts.check_all_contracts()
    #
    # import doctest
    # doctest.testmod()

    clean_data("owid-covid-data.csv")

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['geopandas', 'pandas']
    })
