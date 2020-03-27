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
    if not name.startswith("Independent"):
        continue
    group_cat_id = item['id']
    site = "https://canvas.instructure.com/api/v1/group_categories/%s/groups" % str(group_cat_id)
    groups = requests.get(site, data=data, headers=headers).json()
    for group in groups:
        group_id = group['id']
        # Just get the 9am/10am/11am part -- don't need beyond that
        group_name = group['name'].split(" ")[1]
        site = "https://canvas.instructure.com/api/v1/groups/%s/users" % str(group_id)
        users = requests.get(site, headers=headers).json()
        
        # now the user list is in python, need to remove members from that group
        site = "https://canvas.instructure.com/api/v1/groups/%s" % str(group_id)
        remove_member_data = {'members': []}
        requests.put(site, data=remove_member_data, headers=headers).json()
        
        # and now for each user, make a new group for them
        for user in users:
            new_group_data = {}
            # want '9am Test Student' to help with sorting
            new_group_data['name'] = "%s %s" % (group_name, user['name'])
            site = "https://canvas.instructure.com/api/v1/group_categories/%s/groups" % str(group_cat_id)
            new_group = requests.post(site, data=new_group_data, headers=headers).json()
            group_member_data = {}
            group_member_data['members'] = [user['id']]

            group_id = new_group['id']
            site = "https://canvas.instructure.com/api/v1/groups/%s" % str(group_id)
            new_group = requests.put(site, data=group_member_data, headers=headers).json()
            print("group for %s" % user['name'])
