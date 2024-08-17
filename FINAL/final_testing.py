import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
from FINAL.modified_tree_FINAL import *
from FINAL.data_wrangling import *

plt.style.use('dark_background')
plt.rcParams['text.color'] = 'black'

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
clean_data("FINAL/owid-covid-data.csv")

covid_tree = build_covid_tree("FINAL_TESTING_filtered_data_1.csv")


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

dates = []
for i in range(2020, 2024):
    for j in months:
        dates.append(f'{months[j]} {i}')

chosen_option = "cases"
date_index = 0
region = "World"

fig, (ax_map, ax_bar) = plt.subplots(1, 2, figsize=(16, 8))
plt.subplots_adjust(left=0.04, right=0.65, bottom=0.15, top=0.88, wspace=0.5)

fig.suptitle('Pandemic Patterns: Navigating the Spread of Covid',
             fontsize=20, fontweight='bold',
             color='#e74c3c', y=0.97)


def close(event) -> None:
    """
    Closes the event and sets the global variable 'playing' to False.
    """
    global playing
    playing = False


fig.canvas.mpl_connect('close_event', close)


def update_plot(chosen_option: str, date_index: int, region: str = "World") -> None:
    """
    This function is used to update the world map that we are going to visualize.
    Instance Attributes:
    - chosen_option (str) :The selected option from ‘cases’, ‘deaths’, ‘vaccinations’, ‘cases (pop.adjusted)’,
     ‘deaths (pop.adjusted)’, ‘vaccinations (pop.adjusted)’
    - date_index (int) : The selected index of the date from the list we made above named as ‘dates’
    - region (str) : The region that the user selects to see the visualizations. For this, the default value is ‘World’

    Preconditions:
    - chosen option must be from ‘cases’, ‘deaths’, ‘vaccinations’, ‘cases (pop.adjusted)’, ‘deaths (pop.adjusted)’,
     ‘vaccinations (pop.adjusted)’
    - The date_index must be non-negative and from the list ‘dates’

    """
    ax_map.clear()
    ax_bar.clear()

    dict1 = {}
    if chosen_option == "cases":
        dict1 = {date: covid_tree.get_cases(date) for date in dates}
        colormap = 'Blues'
        title = 'Cases'
    elif chosen_option == "deaths":
        dict1 = {date: covid_tree.get_deaths(date) for date in dates}
        colormap = 'Reds'
        title = 'Deaths'
    elif chosen_option == 'vaccinations':
        dict1 = {date: covid_tree.get_vaccinations(date) for date in dates}
        colormap = 'Greens'
        title = 'Vaccinations'

    elif chosen_option == 'cases (pop. adjusted)':
        dict1 = {date: covid_tree.get_cases_normalised(date) for date in dates}
        colormap = 'Blues'
        title = 'Cases (Pop. Adjusted)'

    elif chosen_option == 'deaths (pop. adjusted)':
        dict1 = {date: covid_tree.get_deaths_normalised(date) for date in dates}
        colormap = 'Reds'
        title = 'Deaths (Pop. Adjusted)'

    elif chosen_option == 'vaccinations (pop. adjusted)':
        dict1 = {date: covid_tree.get_vaccinations_normalised(date) for date in dates}
        colormap = 'Greens'
        title = 'Vaccinations (Pop. Adjusted)'

    selected_date = dates[date_index]

    if region != "World":
        # world_area = world[world['continent'] == region].copy()
        world_area = world.loc[world['continent'] == region].copy()
        world_area.loc[:, 'covid_data'] = world_area['name'].map(dict1[selected_date])
        world_area.plot(column='covid_data', cmap=colormap, linewidth=0.8, ax=ax_map, edgecolor='0.8', legend=False)
        ax_map.set_title(f'COVID-19 {title} \n by Country ({region} - {selected_date})', color='lime')

        region_data = {country: data for country, data in dict1[selected_date].items()
                       if country in world_area['name'].values}
        countries = list(region_data.keys())
        cases = list(region_data.values())
        cases_per_million = [case / 100000 for case in cases]
        ax_bar.barh(countries, cases_per_million, color='skyblue')

        ax_bar.set_xlabel(f'No of {title}', color='lime', fontsize=12)
        ax_bar.set_title(f'COVID-19 {title} \n by Country ({region} - {selected_date})', color='lime')
        ax_bar.invert_yaxis()

        ax_map.set_position([0.05, 0.13, 0.30, 0.72])
        ax_bar.set_position([0.50, 0.13, 0.27, 0.72])

        ax_bar.set_visible(True)
    else:
        new_world = world.copy()
        new_world.loc[:, 'covid_data'] = new_world['name'].map(dict1[selected_date])
        new_world.plot(column='covid_data', cmap=colormap, linewidth=0.8, ax=ax_map, edgecolor='0.8', legend=False)
        ax_map.set_title(f'COVID-19 {title} by Country ({selected_date})', color='lime')

        ax_bar.set_visible(False)

        ax_map.set_position([0.05, 0.13, 0.72, 0.9])
        ax_bar.set_position([0, 0, 0, 0])


update_plot(chosen_option, date_index, region)


def on_option_select(label: str) -> None:
    """
    Callback function for radio button selection of options.

    Instance Attributes:
    - label (str): The label of the selected option.

    Preconditions:
    - label must be one of 'cases', 'deaths', 'vaccinations',
      'cases (pop. adjusted)', 'deaths (pop. adjusted)', or 'vaccinations (pop. adjusted)'.
    """

    global chosen_option
    chosen_option = label
    update_plot(chosen_option, date_index, region)


def on_slider_change(val: float) -> None:
    """
    Callback function for slider change event.

    Instance Attributes:
    - val (float): The value of the slider indicating the selected date index.

    Preconditions:
    - val must be a float representing a valid index within the range of the data in the list 'dates'.

    """
    global date_index
    date_index = int(val)
    update_plot(chosen_option, date_index, region)


#
def on_region_select(label: str) -> None:
    """
    Callback function for radio button selection of regions.

    Instance Attributes:
    - label (str): The label of the selected region.

    Preconditions:
    - label must be a valid region label present in the list 'regions'.

    """
    global region
    region = label
    update_plot(chosen_option, date_index, region)


# Define function to reset slider position to zero
def reset_slider(event) -> None:
    """
    Resets the visualisation to initial position

    """
    global playing
    playing = False
    slider.set_val(0)
    button.label.set_text('Play')


ax_options = plt.axes((0.78, 0.3, 0.19, 0.25), facecolor='#ffffff')
radio_options = RadioButtons(ax_options, ('cases', 'deaths', 'vaccinations', 'cases (pop. adjusted)',
                                          'deaths (pop. adjusted)', 'vaccinations (pop. adjusted)'),
                             active=0, activecolor='grey')
radio_options.on_clicked(on_option_select)

ax_slider = plt.axes((0.14, 0.02, 0.60, 0.03), facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Date', 0, len(dates) - 1, valinit=0, valstep=1, color='#e74c3c')
slider.on_changed(on_slider_change)

ax_region = plt.axes((0.78, 0.6, 0.19, 0.25), facecolor='#ffffff')
regions = ['World', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']
radio_region = RadioButtons(ax_region, regions, active=0)
radio_region.on_clicked(on_region_select)

ax_button = plt.axes((0.04, 0.025, 0.08, 0.03))
button = Button(ax_button, '', color='white', hovercolor='#e74c3c')

ax_reset = plt.axes((0.89, 0.025, 0.08, 0.03))
button_reset = Button(ax_reset, 'Reset', color='white', hovercolor='#e74c3c')
button_reset.on_clicked(reset_slider)

button.label.set_text('Play')

playing = False


def toggle_animation(event) -> None:
    """
    This function is used for defining the play and pause button to run the animation showing the number of cases,
    deaths and vaccinations

    Instance Attributes:
    - event: Event data.

    """

    global playing
    if playing:
        button.label.set_text('Play')
        playing = False
    else:
        button.label.set_text('Pause')
        playing = True
        for i in range(int(slider.val), len(dates)):
            slider.set_val(i)
            plt.pause(0.5)
            if not playing:
                break


button.on_clicked(toggle_animation)


def covid_visualisation() -> None:
    """
    Visualise the COVID tree.
    """

    plt.show()
