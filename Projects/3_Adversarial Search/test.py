###############################################################################
#     YOU CAN MODIFY THIS FILE, BUT CHANGES WILL NOT APPLY DURING GRADING     #
###############################################################################
import logging
import pickle
import random

logger = logging.getLogger(__name__)


with open("data.pickle", "rb") as f:
    data = pickle.load(f)
    print(data)
