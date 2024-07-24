import redis
import threading
import time
import socket

# Define the IP address and ports for Redis servers
REDIS_SOURCE_HOST = '127.0.0.1'
REDIS_SOURCE_PORT = 6378
REDIS_DESTINATION_HOST = '127.0.0.1'
REDIS_DESTINATION_PORT = 6384

# Define the IP address and port for the listener socket
LISTENER_HOST = '127.0.0.1'
LISTENER_PORT = 6484

# Function to set 1000 keys in the source Redis server
def populate_redis_source():
    client = redis.Redis(host=REDIS_SOURCE_HOST, port=REDIS_SOURCE_PORT)
    value = 'a' * (1024)
    for i in range(10, 20):
        response = client.set(f'lkevllt{i}', value)
        if not response:
            print(f"Failed to set key{i}")
    print("Finished setting 1000 keys in the source Redis server")

# Function to start the listener socket in a separate thread
def start_listener():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((LISTENER_HOST, LISTENER_PORT))
    server_socket.listen(5)
    print(f"Listener started on {LISTENER_HOST}:{LISTENER_PORT}")

    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    data = client_socket.recv(1024)
    print(f"Received message: {data.decode('utf-8')}")

    client_socket.close()
    print(f"Connection closed with {client_address}")
    server_socket.close()

# Function to send the migration command
def send_migration_command():
    client = redis.Redis(host=REDIS_SOURCE_HOST, port=REDIS_SOURCE_PORT)
    # client2 = redis.Redis(host=REDIS_DESTINATION_HOST, port=REDIS_DESTINATION_PORT)
    migration_command = f'MIGRATE ASYNC {REDIS_DESTINATION_HOST} {REDIS_DESTINATION_PORT} {LISTENER_HOST} {LISTENER_PORT} "" 0 500000000 KEYS ' + ' '.join([f'lkevllt{i}' for i in range(10, 20)])
    response = client.execute_command(migration_command)
    print(f"Migration command response: {response}")
    # Send the Get Command here :
    # get_response = client.get('key2')
    end_time = time.time()
    return end_time


# Main function to coordinate the test
def main():
    populate_redis_source()

    # Start the listener thread
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()

    # Give some time for the listener to start
    time.sleep(1)

    # Start the timer and send the migration command
    start_time = time.time()
    # send_migration_command()
    end_time = send_migration_command()

    # Wait for the listener thread to finish
    listener_thread.join()

    end_time = time.time()
    print(f"Time taken for migration: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
