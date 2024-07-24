import matplotlib.pyplot as plt

# Define the migration times (you can replace these with your actual data)
migration_times = {
    "Migration 1": {"sync": 10, "async": 5},
    "Migration 2": {"sync": 15, "async": 7},
    "Migration 3": {"sync": 20, "async": 10},
}

# Extracting data for plotting
labels = list(migration_times.keys())
sync_times = [migration_times[label]["sync"] for label in labels]
async_times = [migration_times[label]["async"] for label in labels]

# Create the plot
x = range(len(labels))  # [0, 1, 2]

plt.figure(figsize=(10, 6))

# Plotting synchronous migration times in red
plt.bar(x, sync_times, width=0.4, label='Synchronous', color='red', align='center')

# Plotting asynchronous migration times in blue, offsetting to avoid overlap
plt.bar([p + 0.4 for p in x], async_times, width=0.4, label='Asynchronous', color='blue', align='center')

# Adding labels and title
plt.xlabel('Migration Pairs')
plt.ylabel('Time (ms)')
plt.title('Comparison of Synchronous and Asynchronous Migration Times')
plt.xticks([p + 0.2 for p in x], labels)  # Centering x-ticks
plt.legend()

# Show the plot
plt.show()
