# HostName=CiaranAndLukeIoTHub.azure-devices.net;DeviceId=laptop_test;SharedAccessKey=BbPENAGBd/2FR75UH7IAMZ8VSpsGuLPS4AIoTCAnq4w=
# import csv

# file_path = 'sample_data.csv'

# csv_reader = None
# csv_file = open(file_path, 'r')
# csv_reader = csv.reader(csv_file)
        
# try:
    # while True:
        # row = next(csv_reader)
        # print(row)
# except StopIteration:
    # csv_file.seek(0)
    # print(next(csv_reader))


# csv_file.close()

import csv
import matplotlib.pyplot as plt

# Replace 'your_file.csv' with the actual file path
file_path = 'Output.csv'

# Read the last 30 rows from the CSV file
data = []
with open(file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Skip the header if present
    header = next(csv_reader, None)
    for row in csv_reader:
        data.append([float(value) for value in row])

# Extract columns
column1 = [row[0] for row in data]
column2 = [row[1] for row in data]
column3 = [row[2] for row in data]

# Plot the last 30 rows
plt.plot(column1[-30:], label='Column 1')
plt.plot(column2[-30:], label='Column 2')
plt.plot(column3[-30:], label='Column 3')

# Add labels and legend
plt.xlabel('Index')
plt.ylabel('Values')
plt.legend()

# Save plot as a PNG file
plt.savefig("output_plot.png")

# Show the plot
plt.show()
