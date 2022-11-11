"""
    User-based collaborative filtering using combined items from user's cart and purchases
    -users are filtered by matching items from user's cart and purchases
    -users with matching items (greater than threshold) are considered similar to the current user
    -the similarity of two users is calculated using cosine distance
        smaller cosine distance means greater similarity of the two users
    -items from similar users are then recommended to the user
"""

from scipy.spatial.distance import cosine
from collections import Counter

MIN_PRODUCTS = 3
base_data = []
userID = []

def l1_normalized(v):
    total = sum(v.values())

    if total != 0:
        for id in v.keys():
            v[id] = v[id]/total

    return v

def list_to_dic(lis):
    dic = {}
    for elem in lis:
        dic[elem] = 1

    return dic

def find_sim_users(max_user_num=5):
    matches = {}
    cosine_distance = {}
    filtered = {}

    user_data = base_data[userID]
    threshold = len(user_data)/2

    if len(user_data) < MIN_PRODUCTS:
        return

    for user in base_data.keys():
        if user != userID:
            match = set(base_data[user]).intersection(user_data)
            if len(match) >= threshold:
                matches[user] = len(match)
    
    sorted_matches = sorted(matches.items(), key=lambda item: item[1], reverse=True)
    sorted_matches = dict(sorted_matches)

    for user in sorted_matches.keys():
        temp_sim_data = list_to_dic(base_data[user])
        temp_user_data = list_to_dic(user_data)

        for item in temp_sim_data.keys():
            if item not in temp_user_data.keys():
                temp_user_data[item] = 0

        for item in temp_user_data.keys():
            if item not in temp_sim_data.keys():
                temp_sim_data[item] = 0

        temp_user_data = dict(sorted(temp_user_data.items()))
        temp_sim_data = dict(sorted(temp_sim_data.items()))

        temp_user_data = l1_normalized(temp_user_data)
        temp_sim_data = l1_normalized(temp_sim_data)

        cosine_distance[user] = cosine(list(temp_user_data.values()), list(temp_sim_data.values()))

    sorted_cosine_distance = dict(sorted(cosine_distance.items(), key=lambda item: item[1], reverse=False))

    for user in sorted_cosine_distance.keys():
        if 1 > sorted_cosine_distance[user] > 0:
            filtered[user] = sorted_cosine_distance[user]

    if len(filtered) > max_user_num:
        filtered = dict(list(filtered.items())[:max_user_num])

    return filtered

def recommend_items(similar_users):
    item_difference = []

    if similar_users is None:
        return None

    for user in similar_users.keys():
        diff = set(base_data[user]).difference(base_data[userID])
        item_difference.extend(diff)

    recommended_items = Counter(item_difference).most_common()

    return list(dict(recommended_items))

def get_recommendations(data, id):
    global base_data
    global userID

    base_data = data
    userID = id

    similar_users = find_sim_users()
    items = recommend_items(similar_users)

    return items