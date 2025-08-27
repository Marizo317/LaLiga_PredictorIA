# **🏆 La Liga Predictor IA (Fantasy Consensus Model)**

**La Liga Predictor IA** is a desktop application developed in Python that provides intelligent predictions for Spanish La Liga football matches. The algorithm employs a sophisticated hybrid approach, integrating official match statistics with the market consensus from leading Fantasy platforms (e.g., Biwenger, Fantasy Marca, Futmondo) to generate robust and realistic forecasts.

## **✨ Core Features**

* **Modern User Interface:** Features an elegant and professional design inspired by GitHub's dark mode, developed using the tkinter framework for an optimal user experience.  
* **Dynamic Data Visualization:** Displays an updated league table alongside each team's **"Fantasy Power,"** a key metric representing the consensus market value and public expectation.  
* **Hybrid Prediction Algorithm (50/50 Weighting):** The model's predictive power is derived from a balanced combination of two core data sources:  
  * **50% Official Statistics:** Incorporates points, goals for, and goals against to reflect historical performance.  
  * **50% Fantasy Consensus:** Leverages a simulated market value that represents the collective sentiment and expectations of the Fantasy sports community.  
* **Detailed Forecasts:** Generates predictions for the eight most significant matches of the upcoming matchday. Each forecast is presented in an individual card containing the predicted score, the probable winner, and a dynamically calculated confidence percentage.  
* **Market Fluctuation Simulation:** The UPDATE function simulates market volatility by adjusting team Fantasy Power values, reflecting how real-world news and recent performance can influence market perception.  
* **Self-Contained Codebase:** The application is developed entirely in Python, utilizing only standard libraries, which obviates the need for external dependencies or complex installation procedures.

## **🧠 Algorithmic Methodology**

The prediction engine quantifies the "strength" of each team prior to a match by applying a weighted formula:

1. **Statistical Strength (50% Weight):** A baseline value is calculated from each team's current points total and goal difference. This component represents the team's demonstrated, tangible performance in the league.  
2. **Fantasy Power Strength (50% Weight):** The "Fantasy Power" metric is utilized as a proxy for public and expert sentiment, representing the collective wisdom of thousands of users on prominent Fantasy platforms.  
3. **Home-Field Advantage:** A performance bonus of ten percent (+10%) is applied to the home team to account for the well-documented advantage of playing in a familiar environment.

The aggregation of these factors produces a conservative goal prediction and a dynamic confidence calculation for each fixture.

## **🚀 Installation and Execution**

The project requires no external library installations as it relies exclusively on standard Python modules.

1. **Clone the repository:**  
   git clone https://github.com/YourUsername/LaLigaPredictorIA.git

2. **Navigate to the project directory:**  
   cd LaLigaPredictorIA

3. **Execute the application:**  
   python laliga\_predictor.py

## **📜 License**

This project is distributed under the **MIT License**. This license permits the free use, modification, and distribution of the software. For complete details, please refer to the LICENSE file.