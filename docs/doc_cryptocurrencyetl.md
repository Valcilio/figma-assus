# Diagram (Resume)

![ETL Diagram](https://i.ibb.co/cTbx75Z/Diagrama-em-branco-1.png)

# Data Source

All the data is extracted from Alpha Vantage's API free version, see the documentation clicking [here](https://www.alphavantage.co/documentation), how give this permissions:

1. Max of 5 calls per minute;
2. Max of 500 calls per day.

To acquire a upgrade version of this API click [here](https://www.alphavantage.co/premium/), the upgraded versions of this API give a much more calls per minute and unlimited calls per day.

# Project

## Goal

This ETL was made to obtain data to create interactive dashboards with the amount of cryptocurrencies  and following these requirements below: 

- Be possible to extract data in real time to update the dashboard daily;
- Be possible to use these data directly in any model to make predictions and understand tendencies;
- Validate the reliability of these data automatically to guarantee the utility of this ETL.

## Process

To achieve the goal of this project with security, supervision and monitoring was structured a some process:

- Selected the Alpha Vantage API to be the datasource where is extracted new data in every new call;
- Automatic transform and load data prepared for data analysis and ML Modeling;
- Automatic alerts of errors and information indicating the start and end of the ETL;
- Automatic tests to validate the data of the ETL and guarantee the maximum security.
