import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    # soup은 html을 몽땅 가져옴
    pagination = soup.find("div", {"class": "pagination"})
    # pagination은 div를 찾고, class가 pagination인 것들을 soup으로 반환
    links = pagination.find_all('a')
    # 위의 soup에서 링크를 다 찾아내고 리스트를 만듦, 각 링크 안에 있는 span을 아래 코드를 이용해 추출 해 내는 것임
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
        # 여기까지 찾아낸 것들을 미리 만들어둔 빈 array에 넣은것
    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    if company:
     company_anchor = company.find("a")
     if company_anchor is not None:
         company = str(company_anchor.string)
     else:
          company = str(company.string)
     company = company.strip()
    else:
      company = None
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {
        'title': title,
        'company': company,
        'location': location,
        "link": f"https://www.indeed.com/viewjob?jk={job_id}&from=web&vjs=3"
    }


def extract_jobs(last_page):
   jobs = []
   for page in range(last_page):
     print(f"Scrapping Indeed: Page: {page}")
     result = requests.get(f"{URL}&start={page*LIMIT}")
     soup = BeautifulSoup(result.text, "html.parser")
     results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
     for result in results:
        job = extract_job(result)
        jobs.append(job)
   return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs