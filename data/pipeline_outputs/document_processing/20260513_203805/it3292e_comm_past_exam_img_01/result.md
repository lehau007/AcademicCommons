# Midterm Exam 20232 - IT3090E Database

## Step 1: Extracting Row Labels, Column Labels, and Cell Values

The provided document appears to be a midterm exam for a database course, specifically IT3090E. The exam consists of several questions related to database design and querying.

## Questions

### Question 1
Modeling the following data requirement using ER model and then transforming it into relational schema:

Bloodhound Coaches runs daily scheduled services all over the country. Customers want to check the schedules and prices online, so a first step is to put the schedule into a database...

### Question 2
A relation R(ABCD) and a set of functional dependency F = {AB→D; BC→C; AC→B; AC→D}. Write 4 other functional dependencies that can be derived from F using the Armstrong's axiom system.

### Question 3
A relation R(ABEIJGH), and a set of functional dependency F ={AB→E; AG→J; BE→I; E→G; GI→H}

* Find a candidate key of R
* Normalize to third normal form.

### Question 4
Given the Blood Bank Database schema:

| Table Name | Attributes |
| --- | --- |
| Blood_Type | blood_type_ID, name, description |
| Donor | donor_ID, blood_type_id, name, date_of_birth, contact_number, city |
| Donation | d_tran_ID, donor_ID, donation_confirmation, health_condition, amount, date |
| Hospital | hospital_ID, name, city |
| Recipient_Transaction | r_trans_ID, hospital_ID, blood_type_ID, date |
| Recipient_Transaction_Details | r_trans_ID, d_tran_ID |

Write SQL queries for the following:

* List all Donor in 'Hanoi' (city)
* List the hospital that have received the blood's type 'Rh+'
* List all donors under 20 years old or over 58 years old.
* List the number of donations per day in July 2023 (suppose that the date is recognized by day) in order of date.
* List the information about Donors who do not donate the blood in the 3 last years
* Write the algebraic expression for query 3.