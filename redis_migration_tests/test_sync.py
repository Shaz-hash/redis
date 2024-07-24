import redis
import time

# Define the IP address and ports for Redis servers
REDIS_SOURCE_HOST = '127.0.0.1'
REDIS_SOURCE_PORT = 6378
REDIS_DESTINATION_HOST = '127.0.0.1'
REDIS_DESTINATION_PORT = 6384

# Function to set 1000 keys in the source Redis server
def populate_redis_source():
    client = redis.Redis(host=REDIS_SOURCE_HOST, port=REDIS_SOURCE_PORT)
    value = 'a' * (1048576)
    
    for i in range(1000):
        # response = client.set(f'kenoel{i}', f'the value{i} for the house , the price becomes {i} what a standard mode , I love this argument wohooo.')
        response = client.set(f'kenoev{i}',value)
        if not response:
            print(f"Failed to set key{i}")
        if i == 1 :
            print("Your response is ", response)
    print("Finished setting 1000 keys in the source Redis server")

# Function to send the migration command
def send_migration_command():
    client = redis.Redis(host=REDIS_SOURCE_HOST, port=REDIS_SOURCE_PORT)
    client2 = redis.Redis(host=REDIS_DESTINATION_HOST, port=REDIS_DESTINATION_PORT)
    migration_command = f'MIGRATE SYNC {REDIS_DESTINATION_HOST} {REDIS_DESTINATION_PORT} "" 0 50000000 KEYS ' + ' '.join([f'kenoev{i}' for i in range(1000)])
    response = client.execute_command(migration_command)
    print(f"Migration command response: {response}")
    get_response = client2.get('key2')
    return time.time()

# Main function to coordinate the test
def main():
    populate_redis_source()

    # Start the timer and send the migration command
    start_time = time.time()
    end_time = send_migration_command()
    # end_time = time.time()

    print(f"Time taken for migration: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
