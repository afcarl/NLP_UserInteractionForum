import numpy as np
import matplotlib.pyplot as plt
import projectUtil

def getMostActiveUsers(ts, numActiveUsers):
    pass

def main():
    ts = projectUtil.loadData();
    # First: find 100 most active users (counting the number of comments)
    mostActiveUsers = getMostActiveUsers(ts, 100);


if __name__ == "__main__":
    main();