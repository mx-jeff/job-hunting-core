

def load_jobs_in_txt(link='tests/infojobs/mock_data/infojobs.txt'):
    with open(link, 'r') as f:
        jobs = f.read().splitlines()

    return jobs
