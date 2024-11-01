import csv
import pandas as pd
import matplotlib.pyplot as plt

# Generator til at læse CSV-data
def read_suicide_data(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row

# Filtrer data for Danmark
def filter_data_for_denmark(data_generator):
    for row in data_generator:
        if row['country'].strip() == 'Denmark':
            yield row

# Analyser data
def analyze_data(denmark_data):
    # Konverter data til en DataFrame
    df = pd.DataFrame(denmark_data)
    # Konverter str til float for statistisk analyse
    df[['SuicideRate_BothSexes_RatePer100k_2021', 'SuicideRate_Male_RatePer100k_2021', 'SuicideRate_Female_RatePer100k_2021']] = df[['SuicideRate_BothSexes_RatePer100k_2021', 'SuicideRate_Male_RatePer100k_2021', 'SuicideRate_Female_RatePer100k_2021']].astype(float)

    # Beregn gennemsnit, median og standardafvigelse
    average_suicide_rate = df['SuicideRate_BothSexes_RatePer100k_2021'].mean()
    median_suicide_rate = df['SuicideRate_BothSexes_RatePer100k_2021'].median()
    std_dev_suicide_rate = df['SuicideRate_BothSexes_RatePer100k_2021'].std()

    return average_suicide_rate, median_suicide_rate, std_dev_suicide_rate, df

# Visualisering
def visualize_data(df):
    years = ['2019', '2020', '2021']  # Rækkefølge af årstal
    rates = [
        float(df['SuicideRate_BothSexes_RatePer100k_2019'].values[0]),  # Henter værdien og konverterer til float
        float(df['SuicideRate_BothSexes_RatePer100k_2020'].values[0]),
        float(df['SuicideRate_BothSexes_RatePer100k_2021'].values[0])
    ]
    
    # Debug output for rates
    print("Selvmordsrater:", rates)

    plt.figure(figsize=(10, 6))
    plt.plot(years, rates, marker='o')
    plt.title('Selvmordsrate i Danmark')
    plt.xlabel('År')
    plt.ylabel('Selvmordsrate per 100k')
    plt.grid()
    
    # Juster y-aksens grænser, så højere værdier vises øverst
    plt.ylim(max(rates) + 1, min(rates) - 1)  # Juster for at få den rigtige rækkefølge
    plt.gca().invert_yaxis()  # Inverter y-aksen
    plt.show()




# Hovedprogram
if __name__ == "__main__":
    file_path = 'C:\\Users\\A-SPAC09\\Desktop\\Python\\uge4opgave\\suicideglobal2024.csv'  # Angiver stien til CSV-fil

    # Læs data
    data_generator = read_suicide_data(file_path)
    denmark_data = list(filter_data_for_denmark(data_generator))

    if denmark_data:
        # Analyser data
        average, median, std_dev, df = analyze_data(denmark_data)
        print(f"Gennemsnitlig selvmordsrate: {average}")
        print(f"Median selvmordsrate: {median}")
        print(f"Standardafvigelse: {std_dev}")

        # Visualiser data
        visualize_data(df)
    else:
        print("Ingen data for Danmark fundet.")
