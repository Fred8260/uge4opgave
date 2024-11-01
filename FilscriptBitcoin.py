import pandas as pd
import matplotlib.pyplot as plt

# Funktions til at analysere volatilitet
def analyze_volatility(file_path, window=30, threshold=500):
    

    volatility_data = []  # Liste til at opbevare volatilitet data fra hver chunk

    # Læs data i chunks for at undgå at indlæse hele filen i hukommelsen ad gangen
    for chunk in pd.read_csv(file_path, chunksize=10000, usecols=['Open time', 'Close']):
        # Konverter 'Open time' kolonnen til datetime-format for bedre håndtering
        chunk['Open time'] = pd.to_datetime(chunk['Open time'])
        # Konverter 'Close' kolonnen til float for at kunne udføre beregninger
        chunk['Close'] = chunk['Close'].astype(float)

        # Beregn volatilitet for hver chunk ved at anvende en glidende standardafvigelse
        chunk['volatility'] = chunk['Close'].rolling(window=window).std()
        volatility_data.append(chunk)  # Tilføj chunkens data til volatilitet_data listen

    # Saml alle data fra chunks til én DataFrame
    full_data = pd.concat(volatility_data)

    # Filtrer kun de punkter, hvor volatiliteten er over tærsklen, og fjern NaN-værdier
    filtered_data = full_data[full_data['volatility'] > threshold].dropna(subset=['volatility'])

    return filtered_data[['Open time', 'volatility']]  # Returner kun relevante kolonner

# Visualisering af volatilitet
def visualize_volatility(df):
    
    plt.figure(figsize=(12, 6))  # Definér størrelsen på plottet
    plt.plot(df['Open time'], df['volatility'], color='orange', label='Volatilitet')  # Plot volatilitet over tid
    plt.title('Bitcoin Volatilitet Over Tid')  # Titel på plottet
    plt.xlabel('Dato')  # X-akse label
    plt.ylabel('Volatilitet (USD)')  # Y-akse label
    plt.grid()  # Vis gridlinjer for bedre læsbarhed
    plt.legend()  # Vis legende for at identificere plottet
    plt.show()  # Vis plottet

# Hovedprogram
if __name__ == "__main__":
    file_path = 'C:\\Users\\A-SPAC09\\Desktop\\Python\\uge4opgave\\BTCUSD_1m_Binance.csv'
    
    # Analyser volatilitet
    volatility_df = analyze_volatility(file_path, window=30, threshold=500)  # Angiv 500 USD som tærskel

    # Tjek om der er data at visualisere, og kald visualiseringsfunktionen
    if not volatility_df.empty:
        visualize_volatility(volatility_df)
    else:
        print("Ingen volatilitet data fundet.")  # Meld hvis der ikke er data

