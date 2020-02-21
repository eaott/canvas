# canvas
Scripts for dealing with specific group management issues on Canvas

# Known Issues
-- `canvas.py` should currently be run exactly once, and hasn't been updated to consider additional/singleton groups created by `canvas_single_groups.py`. YMMV using it later, although I will likely update this in the coming weeks (Feb 2020).

# Goals
* Allow for user-friendly reuse of group sets (easy for students to start an unambiguous new Collaboration), while allowing movement from week to week without corrupting grades or feedback/comments
* Navigate around comments not showing unless a user is in a group for group assignments

# Requirements
* A token generated for our account on Canvas (`/profile/settings`)
* python3
* the Canvas course ID for the course you care about (left as exercise to the reader, see https://canvas.instructure.com/doc/api/all_resources.html for info about the API -- note, it's not necessarily the ID in the URL)

# Assumptions
* A Group Set called `Original` that serves as the default group set, i.e., barring students being removed for absenses, these groups would be the same from week to week
* Group Sets cloned off of `Original`, each with a name where the first word is indicative of the assignment
* Absent students are moved to the "unassigned" group

# `canvas.py` (run once at start of semester)
Example. Let's say you have a `Boxplot Groups` Group Set that was cloned from `Original` with groups `Group 1`, `Group 2`, `Group 3`, etc. This script will set all the group names in the `Boxplot Groups` Group Set to `Boxplot Group 1`, `Boxplot Group 2`, etc.

This script will go through all Group Sets apart from `Original` and update the individual group names based on first word in the Group Set name.

# `canvas_single_groups.py` (run after every assignment)
This long, complicated script essentially gets the typical groups from `Original` and goes through the other Group Sets and identifies students who are unassigned. For each of those students, it creates a group in that Group set with their name.

As an example, consider the following Group Sets before running this script

`Original`
* Group 1: Michael, Pam
* Group 2: Dwight, Jim

`Boxplot Groups`
* Boxplot Group 1: Pam
* Boxplot Group 2: Dwight, Jim
* *unassigned*: Michael

`Histogram Groups`
* Histogram Group 1: Michael
* Histogram Group 2: Dwight
* *unassigned*: Jim, Pam

After the script, the group sets will be

`Original` (unchanged)
* Group 1: Michael, Pam
* Group 2: Dwight, Jim

`Boxplot Groups`
* Boxplot Group 1: Pam
* Boxplot Group 2: Dwight, Jim
* Michael: Michael

`Histogram Groups`
* Histogram Group 1: Michael
* Histogram Group 2: Dwight
* Jim: Jim
* Pam: Pam

That ensures that every unassigned person will have a group ID (and thus have comments visible), while keeping them separated in a way that is easy to judge attendance, etc.
