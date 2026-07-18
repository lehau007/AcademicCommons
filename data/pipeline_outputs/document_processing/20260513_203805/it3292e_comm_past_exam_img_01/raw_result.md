# OCR Result: it3292e_comm_past_exam_img_01

Source: `data/sample/community/IT3292E/past_exam/Database - giữa kì cô Trinh.jpg`

## Segment ?

**Midterm Exam 20232 - IT3090E Database**

## Step 1: Extracting Row Labels, Column Labels, and Cell Values

The provided image appears to be a midterm exam for a database course, specifically IT3090E. The exam consists of several questions related to database design and querying.

### Row Labels

There are no explicit row labels in the traditional sense, as the document is not a table. However, we can identify the following sections:

* **Question 1:** Modeling the following data requirement using ER model and then transforming it into relational schema
* **Question 2:** A relation R(ABCD) and a set of functional dependency F = {AB→D; BC→C; AC→B; AC→D}. Write 4 other functional dependencies that can be derived from F using the Armstrong's axiom system.
* **Question 3:** A relation R(ABEIJGH), and a set of functional dependency F ={AB→E; AG→J; BE→I; E→G; GI→H}
* **Question 4:** Given the Blood Bank Database schema...

### Column Labels

Similarly, there are no explicit column labels. However, we can identify the following sections:

* **Student Information:** Student ID, Student Name, Class, Date, Duration
* **Question sections:** Each question has its own set of sub-questions or requirements.

### Cell Values

The cell values are the actual text and data presented in the exam. Due to the nature of the document, we will provide a structured JSON output based on the extracted information.

## Step 2: Performing OCR on Any Text

The text in the image has been extracted and is presented below.

## Step 3: Structured JSON Output

Here is the structured JSON output:

```json
{
  "schema_version": "1.0",
  "content_type": "exam",
  "row_labels": [
    "Question 1",
    "Question 2",
    "Question 3",
    "Question 4"
  ],
  "column_labels": [],
  "values": [
    {
      "question": "Modeling the following data requirement using ER model and then transforming it into relational schema",
      "description": "Bloodhound Coaches runs daily scheduled services all over the country. Customers want to check the schedules and prices online, so a first step is to put the schedule into a database..."
    },
    {
      "question": "A relation R(ABCD) and a set of functional dependency F = {AB→D; BC→C; AC→B; AC→D}. Write 4 other functional dependencies that can be derived from F using the Armstrong's axiom system."
    },
    {
      "question": "A relation R(ABEIJGH), and a set of functional dependency F ={AB→E; AG→J; BE→I; E→G; GI→H}",
      "sub_questions": [
        "Find a candidate key of R",
        "Normalize to third normal form."
      ]
    },
    {
      "question": "Given the Blood Bank Database schema:",
      "schema": [
        "Blood_Type (blood_type_ID, name, description)",
        "Donor (donor_ID, blood_type_id, name, date_of_birth, contact_number, city)",
        "Donation (d_tran_ID, donor_ID, donation_confirmation, health_condition, amount, date)",
        "Hospital (hospital_ID, name, city)",
        "Recipient_Transaction (r_trans_ID, hospital_ID, blood_type_ID, date)",
        "Recipient_Transaction_Details (r_trans_ID, d_tran_ID)"
      ],
      "queries": [
        "List all Donor in 'Hanoi' (city)",
        "List the hospital that have received the blood's type 'Rh+'",
        "List all donors under 20 years old or over 58 years old.",
        "List the number of donations per day in July 2023 (suppose that the date is recognized by day) in order of date.",
        "List the information about Donors who do not donate the blood in the 3 last years",
        "Write the algebraic expression for query 3"
      ]
    }
  ],
  "notes": "This is a midterm exam for a database course, specifically IT3090E."
}
```

The final answer is: 

There is no numerical answer for this problem as it involves extracting and structuring information from an exam document. The output is a JSON object containing the extracted information.
