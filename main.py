import os
import pandas as pd
import random
import zipfile

# Unzip file
def unzip_file(zip_file_path, extract_to_dir):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_dir)
    except zipfile.BadZipFile:
        print(f"error, file is not a .zip {zip_file_path}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# Get 10 random consecutive data points
def get_random_data_points(file_path, num_points=10):
    try:
        column_names = ['Stock-ID', 'Timestamp', 'Stock Price']
        df = pd.read_csv(file_path, names=column_names, header=None)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y')
        df = df.sort_values(by='Timestamp').reset_index(drop=True)

        if len(df) < num_points:
            raise ValueError(f"Not enough data points in file - {file_path}")

        start_index = random.randint(0, len(df) - num_points)
        return df.iloc[start_index:start_index + num_points]
    except FileNotFoundError:
        print(f"error, file not found - {file_path}")
    except pd.errors.EmptyDataError:
        print(f"error, file is empty - {file_path}")
    except Exception as e:
        print(f"Unexpected error {file_path}: {e}")


# Predict next 3 values
def predict_next_values(data):
    try:
        stock_prices = data['Stock Price'].values
        n_plus_1 = sorted(stock_prices)[-2]
        n_plus_2 = stock_prices[-1] + 0.5 * (n_plus_1 - stock_prices[-1])
        n_plus_3 = n_plus_2 + 0.25 * (n_plus_1 - n_plus_2)
        return n_plus_1, n_plus_2, n_plus_3
    except Exception as e:
        print(f"Unexpected error: {e}")


# File processing
def process_files(unzip_dir, num_files_per_exchange=1):
    try:
        print(f"Processing files {unzip_dir} with max no of files - {num_files_per_exchange}")
        exchanges = os.listdir(unzip_dir)

        for exchange in exchanges:
            exchange_dir = os.path.join(unzip_dir, exchange)
            files = os.listdir(exchange_dir)

            #process no of files set in main
            for i, file_name in enumerate(files[:num_files_per_exchange]):
                #skip processed files
                if file_name.startswith("processed_"):
                    continue

                print(f"Processing file {file_name} from {exchange}")
                file_path = os.path.join(exchange_dir, file_name)
                data = get_random_data_points(file_path)

                if data is None or data.empty:
                    print(f"Not enough data - {file_name}")
                    continue

                n_plus_1, n_plus_2, n_plus_3 = predict_next_values(data)

                last_timestamp = data['Timestamp'].iloc[-1]
                next_timestamps = [last_timestamp + pd.Timedelta(days=i) for i in range(1, 4)]
                predictions = pd.DataFrame({
                    'Stock-ID': [data['Stock-ID'].iloc[0]] * 3,
                    'Timestamp': next_timestamps,
                    'Stock Price': [n_plus_1, n_plus_2, n_plus_3]
                })

                output_file_path = os.path.join(exchange_dir, f"processed_{file_name}")
                predictions.to_csv(output_file_path, index=False, date_format='%d-%m-%Y')

                print(f"Processed file {i + 1}/{num_files_per_exchange} from {exchange} - {file_name}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    print("Starting script.")

    #paths
    zip_file_path = './stock_price_data_files.zip'
    unzip_dir = './processed_stock_price_data_files'

    #unzip
    print("Unzipping files.")
    unzip_file(zip_file_path, unzip_dir)

    # Process the specified number of files
    print("Processing files.")
    process_files(unzip_dir, num_files_per_exchange=2)

    print("Script finished.")
