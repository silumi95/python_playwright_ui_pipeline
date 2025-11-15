import pytest

if __name__ == "__main__":
    pytest.main(["tests", 
                 "-v", 
                 "--json-report", 
                 "--json-report-file=results/latest.json"])
