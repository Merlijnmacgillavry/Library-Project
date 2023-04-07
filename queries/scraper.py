from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
        
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# URL of the search page
url = "https://repository.tudelft.nl/islandora/search/?collection=education"

# Load the search page
driver.get(url)

# Open the file for reading
with open("C:\\Users\\joeyn\\Desktop\\TUDelft\\CS Master\\Information Retrieval\\queries_filtered.txt", "r") as file:
    # Open the output file for writing
    with open("C:\\Users\\joeyn\\Desktop\\TUDelft\\CS Master\\Information Retrieval\\queries_filtered_documents.txt", "w") as output_file:
    
        # Read each line of the file
        for query in file:
            # Find the input tag with name 'islandora_simple_search_query'
            search_input = driver.find_element(By.ID, "edit-islandora-simple-search-query")

            # Set the value of the input tag to the query
            search_input.send_keys(query)

            # Submit the form by finding and clicking the submit button
            submit_button = driver.find_element(By.ID, "edit-submit")
            submit_button.click()

            # Find the element that displays the number of search results
            result_count_elem = driver.find_element(By.CLASS_NAME, "search-results-count").text

            # Write the number of search results to a file
            output_file.write(result_count_elem + "\n")
            # print(result_count_elem)

            driver.find_element(By.ID, "edit-islandora-simple-search-query").clear()

# Quit the WebDriver
driver.quit()