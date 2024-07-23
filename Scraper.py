import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

def scrape_wuzzuf_jobs(url):
    # Open URL and read the HTML
    try:
        request = urlopen(url)
        html = request.read()
        request.close()
    except Exception as e:
        print(f"Failed to fetch URL: {e}")
        return []

    # Parse HTML with BeautifulSoup
    soup = bs(html, 'html.parser')
    containers = soup.find_all('div', {'class': 'css-pkv5jc'})

    jobs = []
    for container in containers:
        # Extract job title
        job_title_tag = container.find('h2', {'class': 'css-m604qf'})
        job_title = job_title_tag.text.strip() if job_title_tag else 'N/A'

        # Extract company name
        company_name_tag = container.find('a', {'class': 'css-17s97q8'})
        company_name = company_name_tag.text.strip() if company_name_tag else 'N/A'

        # Extract company location
        company_location_tag = container.find('span', {'class': 'css-5wys0k'})
        company_location = company_location_tag.text.strip() if company_location_tag else 'N/A'

        # Append extracted data to the list
        jobs.append({
            'Job Title': job_title,
            'Company Name': company_name,
            'Company Location': company_location
        })

    return jobs

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    url = 'https://wuzzuf.net/search/jobs/?q=data+analysis&a=hpb'
    jobs = scrape_wuzzuf_jobs(url)
    if jobs:
        save_to_csv(jobs, 'wuzzuf_jobs.csv')

if __name__ == "__main__":
    main()
