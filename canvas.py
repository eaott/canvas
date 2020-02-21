import requests

# Token is expired, go to /profile/settings > test to generate a new one
token = "Bearer <token goes here>"
lab_id = '<course ID goes here>'

site = "https://canvas.instructure.com/api/v1/courses/%s/group_categories" % lab_id
headers = {'Authorization': token}
data = {'per_page': 100000}
categories = requests.get(site, data=data, headers=headers).json()

for item in categories:
    name = item['name'].split(" ")[0]
    if name.startswith("Original"):
        continue
    print(name)
    group_cat_id = item['id']
    site = "https://canvas.instructure.com/api/v1/group_categories/%s/groups" % str(group_cat_id)
    groups = requests.get(site, data=data, headers=headers).json()
    for group in groups:
        if group['name'].startswith(name):
            continue
        group_id = group['id']
        group_name = group['name']
        new_group_name = name + " " + group_name
        print(new_group_name)
        site = "https://canvas.instructure.com/api/v1/groups/%s" % str(group_id)
        update_name = {'name': new_group_name}
        requests.put(site, data=update_name, headers=headers).json()
