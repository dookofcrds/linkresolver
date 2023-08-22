import requests
import concurrent.futures
import threading

def is_url_alive(url):
    try:
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def process_url(link):
    if link.startswith("*"):
        return link

def main():
    input_filename = "your-file.txt" #run the tool in the directory with your *test.com links 
    
    with open(input_filename, "r") as input_file:
        input_links = input_file.read().splitlines()

    starred_links = []
    total_links = len(input_links)

    progress_lock = threading.Lock()
    processed_counter = 0

    def update_progress():
        nonlocal processed_counter
        with progress_lock:
            processed_counter += 1
            print(f"Processing link {processed_counter}/{total_links}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(process_url, link) for link in input_links]

        for future in concurrent.futures.as_completed(futures):
            link = future.result()
            update_progress()

            if link is not None:
                starred_links.append(link)

    with open("starred_links.txt", "w") as starred_file:
        for link in starred_links:
            starred_file.write(link + "\n")

    print("Links starting with '*':")
    print("\n".join(starred_links))

if __name__ == "__main__":
    main()

