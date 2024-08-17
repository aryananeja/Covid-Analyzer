# COVID-19 SPREAD ANALYSIS: TRACKING THE PANDEMIC'S IMPACT

This repository contains the source code and documentation for a project focused on analyzing and visualizing the spread of COVID-19. The goal is to explore how the pandemic affected different regions globally using various algorithms and data structures.

## Table of Contents

- [Introduction](#introduction)
- [Datasets](#datasets)
- [Computational Overview](#computational-overview)
- [Instructions for Running](#instructions-for-running)
- [Discussion](#discussion)
- [References](#references)

## Introduction

This project aims to examine the impact of the COVID-19 pandemic across different geographic areas. COVID-19, a highly contagious respiratory disease caused by the novel coronavirus, has disrupted communities worldwide. Through this analysis, we seek to highlight the virus's spread and its effects on global health and the economy.

The project emphasizes the importance of effectively visualizing virus transmission patterns to provide insights into the pandemic's impact on various regions. By studying these trends, health officials, policymakers, and the public can make better-informed decisions on prevention and control measures.

**Objective:** How can we effectively represent COVID-19's spread across regions of varying sizes? The aim is to create an interactive visualization tool that allows users to explore COVID-19 case data, deaths, and vaccination rates—adjusted for population—at both continental and national levels. By integrating population and pandemic data, this visualization aims to offer a clear understanding of how different areas were affected and how vaccination efforts played a role.

## Datasets

For this analysis, we used the following dataset:

- Source: [COVID-19 Data](https://github.com/owid/covid-19-data/tree/master/public/data)

This dataset provided key statistics on COVID-19 cases, deaths, and vaccinations at both country and regional levels, forming the foundation for our analysis and visualization.

## Computational Overview

Our project utilizes tree data structures to represent the hierarchical relationship between the world, regions, and individual countries, allowing for a clear depiction of COVID-19's spread.

- **Data Preprocessing:** Cleaning and organizing raw data to extract relevant information such as dates, cases, deaths, and vaccination rates.
- **Tree Construction:** Implementing custom recursive algorithms to build a tree structure that represents the relationship between continents, countries, and regions.
- **Data Analysis:** Calculating statistics and trends to display them as bar plots and maps.
- **Visualization:** Creating interactive visualizations with Python libraries like [GeoPandas](https://geopandas.org/en/stable/) and [Matplotlib](https://matplotlib.org/) to display COVID-19's spread and its influencing factors.

## Instructions for Running

To run the project, follow these steps:

1. **Download the files** and unzip the package to access the program files and directories.
2. **Install necessary Python libraries** using the `requirements.txt` file.
    ```sh
    pip install -r requirements.txt
    ```
3. **Run the `main.py` file.**
    ```sh
    python main.py
    ```

Once the program runs, an interactive visualization window will open. It will display COVID-19 statistics at a global level. The interface includes play/pause controls, reset functionality, and filters to visualize specific regions. Upon selecting a region, you can view corresponding bar plots that present COVID-19 statistics for countries within that region.

## Discussion

Our exploration provided valuable insights into the spread of COVID-19 and its influencing factors. Key takeaways include:

- Tracking the transmission of COVID-19 from its epicenter to the rest of the world during the pandemic's four key years.
- Highlighting the role vaccines played in mitigating the pandemic's effects by analyzing data from vaccine-heavy countries.
- Analyzing death rates relative to case counts to observe mortality trends across different regions.

While the project uncovered significant trends, there were limitations. We initially intended to analyze data at more granular levels (state and district), but reliable data was not available for such an analysis.

## References

- GeoPandas Documentation. Available at: [https://geopandas.org/en/stable/](https://geopandas.org/en/stable/)
- Matplotlib Documentation. Available at: [https://matplotlib.org/](https://matplotlib.org/)
- Our World in Data. "COVID-19 Data." GitHub, accessed 2 March 2024: [https://github.com/owid/covid-19-data/tree/master/public/data](https://github.com/owid/covid-19-data/tree/master/public/data)
