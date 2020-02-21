import requests

# go to /profile/settings > test to generate a new token
token = "Bearer <token goes here>"
lab_id = '<course ID goes here>'

site = "https://canvas.instructure.com/api/v1/courses/%s/group_categories" % lab_id
headers = {'Authorization': token}
data = {'per_page': 100000}
categories = requests.get(site, data=data, headers=headers).json()

group_mapping_names = {}
map_names_ids = {}

for item in categories:
    name = item['name'].split(" ")[0]
    if not name.startswith("Original"):
        continue
    print(name)
    group_cat_id = item['id']
    site = "https://canvas.instructure.com/api/v1/group_categories/%s/groups" % str(group_cat_id)
    groups = requests.get(site, data=data, headers=headers).json()
    for group in groups:
        group_id = group['id']
        group_name = group['name']
        print(group_name)
        site = "https://canvas.instructure.com/api/v1/groups/%s/users" % str(group_id)
        users = requests.get(site, headers=headers).json()
        group_mapping_names[group_name] = set([u['name'] for u in users])
        for u in users:
            map_names_ids[u['name']] = u['id']

for item in categories:
    name = item['name'].split(" ")[0]
    if name.startswith("Original"):
        continue
    print(name)
    group_cat_id = item['id']
    site = "https://canvas.instructure.com/api/v1/group_categories/%s/groups" % str(group_cat_id)
    groups = requests.get(site, data=data, headers=headers).json()
    individual_names = set()
    already_in_group = set()
    for group in groups:
        group_id = group['id']
        group_name = group['name'][group['name'].find(" "):].strip()
        site = "https://canvas.instructure.com/api/v1/groups/%s/users" % str(group_id)
        users = requests.get(site, headers=headers).json()

        # If this is a different group than normal
        if group_name not in group_mapping_names:
            # Don't want to make a new group for them
            already_in_group.update([user['name'] for user in users])
            continue

        group_usernames = set([u['name'] for u in users])

        # Otherwise, anyone in users and not original should be ignored
        already_in_group.update(group_usernames.difference(group_mapping_names[group_name]))

        # Anyone in original and not in users should be added
        individual_names.update(group_mapping_names[group_name].difference(group_usernames))

    # remove anyone who already has a group
    individual_names.difference_update(already_in_group)
    for individual in individual_names:
        new_group_data = {}
        new_group_data['name'] = individual
        site = "https://canvas.instructure.com/api/v1/group_categories/%s/groups" % str(group_cat_id)
        new_group = requests.post(site, data=new_group_data, headers=headers).json()
        group_member_data = {}
        group_member_data['members'] = [map_names_ids[individual]]

        group_id = new_group['id']
        site = "https://canvas.instructure.com/api/v1/groups/%s" % str(group_id)
        new_group = requests.put(site, data=group_member_data, headers=headers).json()
        print("group for %s" % individual)
