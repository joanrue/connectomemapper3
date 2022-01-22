# Copyright (C) 2009-2022, Ecole Polytechnique Federale de Lausanne (EPFL) and
# Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland, and CMP3 contributors
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

"""Module that defines CMTK functions for converting C02 emissions estimated with `codecarbon`."""

import pandas as pd

from cmp.info import __version__


def get_emission_car_miles_equivalent(emissions):
    """Return the equivalent of CO2 emissions [Kg] in terms of kms traveled by an average car.

    References
    ----------
    https://github.com/mlco2/codecarbon/blob/c6aebb9681186a71573748e381b6a3c9731de2d3/codecarbon/viz/data.py#L53

    """
    return "{:.0f}".format((emissions / 0.409) * 1.60934)


def get_emission_tv_time_equivalent(emissions):
    """Return the equivalent of CO2 emissions [Kg] in terms of kms traveled by an average car.

    References
    ----------
    https://github.com/mlco2/codecarbon/blob/c6aebb9681186a71573748e381b6a3c9731de2d3/codecarbon/viz/data.py#L66

    """
    tv_time_in_minutes = emissions * (1 / 0.097) * 60
    tv_time = "{:.0f} minutes".format(tv_time_in_minutes)
    if tv_time_in_minutes >= 60:
        time_in_hours = tv_time_in_minutes / 60
        tv_time = "{:.0f} hours".format(time_in_hours)
        if time_in_hours >= 24:
            time_in_days = time_in_hours / 24
            tv_time = "{:.0f} days".format(time_in_days)
    return tv_time


def create_html_carbon_footprint_report(emissions_csv_file, nb_of_subjects_processed):
    """Return a string containing the content of html report to be passed to traits `Str` with `HTMLEditor`.
    
    Parameters
    ----------
    emissions_csv_file : string
        Path to the `emissions.csv` file generated by `Codecarbon`.

    nb_of_subjects_processed : int
        Number of subject processed.
    """
    emissions_df = pd.read_csv(emissions_csv_file)
    last_index = len(emissions_df) - 1
    duration = emissions_df['duration'][last_index]
    energy_consumed = emissions_df['energy_consumed'][last_index]
    emissions = emissions_df['emissions'][last_index]
    country_name = emissions_df['country_name'][last_index]
    region_name = emissions_df['region'][last_index]
    del emissions_df

    country_emissions_per_kwh = float(emissions / energy_consumed)
    car_kms = get_emission_car_miles_equivalent(emissions)
    tv_time = get_emission_tv_time_equivalent(emissions)
    pred_emissions = 100 * emissions / nb_of_subjects_processed
    pred_car_kms = get_emission_car_miles_equivalent(pred_emissions)
    pred_tv_time = get_emission_tv_time_equivalent(pred_emissions)

    return f"""
<!DOCTYPE html>
<html>
<head>
  <title>Footer</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.no-icons.min.css" rel="stylesheet">
  <script src="https://kit.fontawesome.com/d2ef6e0082.js" crossorigin="anonymous"></script>

  <style>
    div {{
      border: 1px solid gray;
      padding: 8px;
    }}

    h1 {{
      text-align: center;
      text-transform: uppercase;
      color: #4CAF50;
    }}

    p {{
      margin: 0px 10px 0px 10px;
      padding: 10px 10px 10px 10px;
      text-indent: 0px;
      text-align: justify;
      background-color: #EEEEEE;
    }}

    a {{
      text-decoration: none;
      color: #008CBA;
    }}
    
    #footer {{
      border: 0px solid gray;
      padding: 8px;
    }}

    #GFG {{
      border: 0px solid gray;
      padding: 8px;
      height: 60px;
      text-align: center;
      padding: 3px;
      color: white;
      background-image: url(https://ohbm-environment.org/wp-content/uploads/slider/cache/aceabfbee23a7b3e8e9fed910c639555/Borneo_rainforest-3.jpg);
      background-position: center center;
      background-repeat: no-repeat;
      background-size: cover;
    }}
    .fa-brain{{
      color: pink;
      font-size: 1em;
      margin: 0px 10px 0px 10px;
      vertical-align: middle;
      horizontal-align: left;
    }}
  </style>
</head>
<body>
    <div id="GFG">
    </div>
    <div>
      <h4>
          Carbon footprint results
      </h4>
      <p>
          Connectome Mapper ({__version__}) was run on {nb_of_subjects_processed} subject(s)
          in {region_name} ({country_name}) (Mean CO<sub>2</sub> kg / kWH: {country_emissions_per_kwh}), having
          the following estimated carbon footprint:
      </p>
      <ul>
          <li>Total run time: {duration}s </li>
          <li>Total estimated CO<sub>2</sub> emissions: {emissions} kg </li>
          <li>Equivalent in distance travelled by avg <i class="fas fa-car"></i>: {car_kms} kms</li>
          <li>Equivalent in amount of time watching a 32-inch LCD flat screen <i class="fas fa-tv"></i>: {tv_time}</li>
      </ul>
      <p>
        <em>
            Estimations were conducted using the
            <a href="https://github.com/mlco2/codecarbon">CodeCarbon emissions tracker</a>.
        </em>
      </p>
      <h4>
          Carbon footprint prediction for 100 subjects
      </h4>
      <p>
          In the same conditions, this would have resulted in:
      </p>
      <ul>
          <li>Co2 emissions: {pred_emissions} kg</li>
          <li>Equivalent in distance travelled by avg <i class="fas fa-car"></i>: {pred_car_kms} kms</li>
          <li>Equivalent in amount of time watching a 32-inch LCD flat screen <i class="fas fa-tv"></i>: {pred_tv_time}</li>
      </ul>
    </div>
</body>
<footer>
  <div id="footer">
    <p>
        Actively part of the initiative created by the
        <a href="https://neuropipelines.github.io/20pipelines">
            Sustainability and Environment Action Special Interest Group</a>,
        the CMP developers hope that by providing you with such metrics it can allow you to be more aware about
        the carbon footprint of your<i class="fas fa-brain" aria-hidden= "true"></i>research. &#127757; &#10024;
    </p>
  </div>
</footer>
<html>

    """
