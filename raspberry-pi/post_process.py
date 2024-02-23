# Code for Raspberry Pi Deliverable #1
# 
# The purpose of this script is to generate a Matplotlib plot
# based on the last 30 datapoints recieved from the IoT device
#
# Authors: Ciaran Harris, Luke Canny
# Date: 23/02/24

### Library Imports
import csv
import matplotlib.pyplot as plt

### Main function
def main(file_index=0, plot_data=None):
    # Try-catch block used incase datapoints are malformed.
    try:
        # Declare file_path and data array
        file_path = 'output.csv'
        data = []

        # If plot data has not been supplied, read from the CSV file
        if plot_data:
            # If plot data has been supplied in function param, process CSV data into data array.
            for row in plot_data:
                row_split = row.split(',')
                data.append([float(value) for value in row_split])    
        else:
            # If plot data has not been supplied, read from file and process into data array
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader, None) # Discard header row (row 0)
                for row in csv_reader:
                    if row == []:
                        continue # discard empty lines
                    data.append([float(value) for value in row])

        # Set column data
        column1 = [row[0] for row in data]
        column2 = [row[1] for row in data]
        column3 = [row[2] for row in data]

        # Plot temperature
        plt.subplot(3,1,1) # 3 rows, 1 column, plot 1
        plt.plot(column1[-30:], label='Temperature (C)')
        plt.xlabel('Index')
        plt.ylabel('Temperature (C)')

        # Plot pressure
        plt.subplot(3,1,2) # 3 rows, 1 column, plot 1
        plt.plot(column2[-30:], label='Atmospheric Pressure (hPa)')
        plt.xlabel('Index')
        plt.ylabel('Atmospheric Pressure (hPa)')

        # Plot humidity
        plt.subplot(3,1,3) # 3 rows, 1 column, plot 1
        plt.plot(column3[-30:], label='Humidity (%)')
        plt.xlabel('Index')
        plt.ylabel('Humidity (%)')

        # Prevent overlapping plots
        plt.tight_layout()

        # Export Plot
        plt.savefig(f"output_plot_{str(file_index)}.png")
        print("Saving plot")
        
        if __name__ == "__main__":
            # If the script has been called manually 
            # (i.e. python ./post_processing.py is called), 
            # provide pop-up of plot
            plt.show()

    except Exception:
        print("Failed to generate plot - Exception")

if __name__ == "__main__":
    # If the script has been called manually call main function
    main()