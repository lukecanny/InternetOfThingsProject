import csv
import matplotlib.pyplot as plt


def main(file_index=0, plot_data=None):
    try:
        file_path = 'output.csv'

        data = []

        # If plot data has not been supplied, read from the CSV file
        if plot_data:
            for row in plot_data:
                row_split = row.split(',')
                data.append([float(value) for value in row_split])    
        else:
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)

                header = next(csv_reader, None)
                for row in csv_reader:
                    if row == []:
                        continue # discard empty lines
                    data.append([float(value) for value in row])

        column1 = [row[0] for row in data]
        column2 = [row[1] for row in data]
        column3 = [row[2] for row in data]

        plt.subplot(3,1,1) # 3 rows, 1 column, plot 1
        plt.plot(column1[-30:], label='Temperature (C)')
        plt.xlabel('Index')
        plt.ylabel('Temperature (C)')

        plt.subplot(3,1,2) # 3 rows, 1 column, plot 1
        plt.plot(column2[-30:], label='Atmospheric Pressure (hPa)')
        plt.xlabel('Index')
        plt.ylabel('Atmospheric Pressure (hPa)')

        plt.subplot(3,1,3) # 3 rows, 1 column, plot 1
        plt.plot(column3[-30:], label='Humidity (%)')
        plt.xlabel('Index')
        plt.ylabel('Humidity (%)')

        plt.tight_layout()

        plt.savefig(f"output_plot_{str(file_index)}.png")
        file_index = file_index + 1
        print("Saving plot")
        # plt.show()
    except Exception:
        print("Failed to generate plot - Exception")

if __name__ == "__main__":
    main()