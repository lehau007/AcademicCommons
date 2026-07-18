# OCR Result: infosec_pptx

Source: `src/experiments/document_processing/test_data/SoICT - 4010E IntroInfoSec - C6- VanNK -extra.pptx`

## Segment 1

Identity Authentication
With extra material for further reading, indicated by symbol *

## Segment 2

Info-Sec 2023
2
Authentication
Basics
Passwords
Challenge-Response
Biometrics
Location
Multiple Methods

## Segment 3

Info-Sec 2023
3
Basics
Authentication: binding of identity to subject
Identity is that of external entity (my identity, Van, etc.)
Subject is computer entity (process, etc.)
Note: 
message authentication is a different topic and already mentioned in the applications of hash functions

## Segment 4

4
Establishing Identity
One or more of the following
What entity knows (eg. password)
What entity has (eg. Identity card, smart card)
What entity is (eg. fingerprints, retinal characteristics)
Where entity is (eg. In front of a particular terminal)

## Segment 5

Info-Sec 2023
5
Authentication System
We need a formal definition, rather abstract view, of an AS 
A 5-tuple (A, C, F, L, S)
A – a set: information that proves identity
C – a set: information stored on computer and used to validate authentication information
F: a set of complementation functions; f : A → C
To compute complement information from identity information
L: authentication functions that prove identity
S: functions enabling entity to create, alter information in A or C

## Segment 6

Info-Sec 2023
6
Example
Password system, with passwords stored on line in clear text
A set of strings making up passwords
C = A
F singleton set of identity function { I }
L single equality test function { eq }
S function to set/change password

## Segment 7

Info-Sec 2023
7
Passwords
Sequence of characters
Examples: 10 digits, a string of letters, etc.
Generated randomly, by user, by computer with user input
Sequence of words
Examples: pass-phrases
Algorithms
Examples: challenge-response, one-time passwords

## Segment 8

Info-Sec 2023
8
Storage
Store as cleartext
If password file compromised, all passwords revealed
Encipher file
Need to have decipherment, encipherment keys in memory
Reduces to previous problem 🡺 need something else
Solution: Instead store one-way hash of password
Got the file, attacker must still guess passwords or invert the hash values

## Segment 9

Info-Sec 2023
9
Example: Unix
By definition, a 5-tuple (A, C, F, L, S)
A – a set: information that proves identity
A = { strings of 8 chars or less }
C – a set: information stored on computer and used to validate authentication information
C = {hash values of password}
F: a set of complementation functions; f : A → C
F = { versions of modified DES }
L: authentication functions that prove identity
L = { login, su, … }
S: functions enabling entity to create, alter information in A or C
S = { passwd, nispasswd, passwd+, … }

## Segment 10

Info-Sec 2023
10
Example: Unix
By definition, a 5-tuple (A, C, F, L, S)
A – a set: information that proves identity
A = { strings of 8 chars or less }
C – a set: information stored on computer and used to validate authentication information
C = {hash values of password}
F: a set of complementation functions; f : A → C
F = { versions of modified DES }
L: authentication functions that prove identity
L = { login, su, … }
S: functions enabling entity to create, alter information in A or C
S = { passwd, nispasswd, passwd+, … }

## Segment 11

Info-Sec 2023
11
Attacking passwords
Goal: find a ∈ A such that:
For some f ∈ F, f(a) = c ∈ C 
c is associated with entity
Two ways to determine whether a meets these requirements:
By trying computing f(a) for a set of a values until succeed
By trying calling I(a) until succeed (I(a) returns true)

## Segment 12

Info-Sec 2023
12
Preventing Attacks
How to prevent this:
Hide at least one of a, f, or c 
Prevents obvious attack from above
Example: UNIX/Linux shadow password files
Hides the c’s
Block access to all l ∈ L or result of l(a)
Prevents attacker from knowing if guess succeeded
Example: preventing any logins to an account from a network
Prevents knowing results of l (or accessing l)

## Segment 13

Info-Sec 2023
13
Dictionary Attacks
Trial-and-error from a list of potential passwords
Off-line: know f and c’s, and repeatedly try different guesses g ∈ A until the list is done or passwords guessed
Examples: crack, john-the-ripper
On-line: have access to functions in L and try guesses g until some l(g) succeeds
Examples: trying to log in by guessing a password

## Segment 14

Info-Sec 2023
14
Success probability over a time period
Anderson’s formula:
P probability of guessing a password in specified period of time
G number of guesses tested in 1 time unit
T number of time units
N number of possible passwords (|A|)
Then P ≥ TG/N

## Segment 15

Info-Sec 2023
15
Example
Goal
Passwords drawn from a 96-char alphabet
Can test 104 guesses per second
Probability of a success to be 0.5 over a 365 day period
What is minimum password length?
Solution
N ≥ TG/P = (365×24×60×60)×104/0.5 = 6.31×1011
Choose s such that Σsj=0 96j ≥ N
So s ≥ 6, meaning passwords must be at least 6 chars long

## Segment 16

Exercise
X = number defined by last 2 digits of your student ID; Y = X mod 4
Assume that H is a cryptographic hash function with output size (Y+2)*16 bits. Assume that Scorpion-i (i=1-9) is a specifically designed line of hardware chips for computing H, where Scorpion-i can create 10i * 1000 hash values a second (e.g. Scorpion-2 can do 100,000 hashes/sec). This product line is the best, fastest and affordable, in the market, priced at ii/2 *$1000 (e.g $2000 for i=2, $16000 for i=4). 

An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size N=(X mod 50)+ 40. Using H, this system maintains the hash values of the passwords of all the users. An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user. Using the Scorpion chips, how much the enemy has to spend in order to finish within a month with success probability (6+Y)*10%?
16

## Segment 17

Info-Sec 2023
17
On password selection
Random selection
Any password from A equally likely to be selected
Pronounceable passwords
User selection of passwords

## Segment 18

Info-Sec 2023
18
Pronounceable Passwords
Generate phonemes randomly
Phoneme is unit of sound, eg. cv, vc, cvc, vcv
Examples: helgoret, juttelon are; przbqxdfl, zxrptglfn are not
Problem: too few
Solution: key crunching
Run long key through hash function and convert to printable sequence
Use this sequence as password

## Segment 19

Info-Sec 2023
19
User Selection
Problem: people pick easy to guess passwords
Based on account names, user names, computer names, place names
Dictionary words (also reversed, odd capitalizations, control characters, “elite-speak”, conjugations or declensions, swear words, Torah/Bible/Koran/… words)
Too short, digits only, letters only
License plates, acronyms, social security numbers
Personal characteristics or foibles (pet names, nicknames, job characteristics, etc.

## Segment 20

Info-Sec 2023
20
Picking Good Passwords
“LlMm*2^Ap”
Names of members of 2 families
“OoHeO/FSK”
Second letter of each word of length 4 or more in third line of third verse of Star-Spangled Banner, followed by “/”, followed by author’s initials 
What’s good here may be bad there
“DMC/MHmh” bad at Dartmouth (“Dartmouth Medical Center/Mary Hitchcock memorial hospital”), ok here
Why are these now bad passwords? ☹

## Segment 21

Info-Sec 2023
21
Proactive Password Checking
Analyze proposed password for “goodness”
Always invoked
Can detect, reject bad passwords for an appropriate definition of “bad”
Discriminate on per-user, per-site basis
Needs to do pattern matching  on words
Needs to execute subprograms and use results
Spell checker, for example
Easy to set up and integrate into password selection system

## Segment 22

Info-Sec 2023
22
Salting
Goal: slow dictionary attacks
Method: perturb hash function so that:
Parameter controls which hash function is used
Parameter differs for each password
So given n password hashes, and therefore n salts, need to hash guess n

## Segment 23

Info-Sec 2023
23
Examples
Vanilla UNIX method
Use DES to encipher 0 message with password as key; iterate 25 times
Perturb E table in DES in one of 4096 ways
12 bit salt flips entries 1–11 with entries 25–36
Alternate methods
Use salt as first part of input to hash function

## Segment 24

Info-Sec 2023
24
Unix actually is …
UNIX system standard hash function
Hashes password into 11 char string using one of 4096 hash functions
As authentication system:
A = { strings of 8 chars or less }
C = { 2 char hash id || 11 char hash }
F = { 4096 versions of modified DES }
L = { login, su, … }
S = { passwd, nispasswd, passwd+, … }

## Segment 25

Exercise
Assume that H is a cryptographic hash function with output size (Y+2)*16 bits. Assume that Scorpion-i (i=1-9) is a specifically designed line of hardware chips for computing H, where Scorpion-i can create 10i * 1000 hash values a second, priced at ii/2 *$1000.
1. An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size N=(X mod 50)+ 40. Using H, this system maintains the hash values of the passwords of all the users. An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user. Using the Scorpion chips, how much the enemy has to spend in order to finish within a month with success probability (6+Y)*10%?
2. The owner decides to enhance the above password system by using salt so that the enemy will need to spend at least 10 times the above mentioned amount of money to achieve the same goal. How many salt bits he/she need to use to achieve this purpose ?
25

## Segment 26

Part 2 ⎯ Access Control                                                                                                  26
Password Cracking: Do the Math*
* Further reading
Assumptions:
Pwds are 8 chars, 128 choices per character
Then 1288 = 256 possible passwords
There is a password file with 210 pwds
Attacker has dictionary of 220 common pwds
Probability 1/4 that password is in dictionary
Work is measured by number of hashes

## Segment 27

Part 2 ⎯ Access Control                                                                                                  27
Salt with slow hash *
Hash password with salt
Choose random salt s and compute 
			y = h(password, s) 
	and store (s,y) in the password file
Note that the salt s is not secret
Analogous to IV 
Still easy to verify salted password
But lots more work for Hacker
Why?

## Segment 28

Part 2 ⎯ Access Control                                                                                                  28
Password Cracking: Case I *
Attack 1 specific password without using a dictionary
E.g., administrator’s password
Must try 256/2 = 255 on average
Like exhaustive key search
Does salt help in this case?

## Segment 29

Part 2 ⎯ Access Control                                                                                                  29
Password Cracking: Case II *
Attack 1 specific password with dictionary
With salt
Expected work: 1/4 (219) + 3/4 (255) ≈ 254.6
In practice, try all pwds in dictionary…
…then work is at most 220 and probability of success is 1/4 
What if no salt is used?
One-time work to compute dictionary: 220
Expected work is of same order as above
But with precomputed dictionary hashes, the  “in practice” attack is essentially free…

## Segment 30

Part 2 ⎯ Access Control                                                                                                  30
Password Cracking: Case III *
Any of 1024 pwds in file, without dictionary
Assume all 210 passwords are distinct 
Need 255 comparisons before expect to find pwd
If no salt is used
Each computed hash yields 210 comparisons
So expected work (hashes) is 255/210 = 245
If salt is used
Expected work is 255 
Each comparison requires a hash computation

## Segment 31

Part 2 ⎯ Access Control                                                                                                  31
Password Cracking: Case IV *
Any of 1024 pwds in file, with dictionary
Prob. one or more pwd in dict.: 1 – (3/4)1024 ≈ 1
So, we ignore case where no pwd is in dictionary
If salt is used, expected work less than 222
See book, or slide notes for details
Work ≈ size of dictionary / P(pwd in dictionary)
What if no salt is used? 
If dictionary hashes not precomputed, work is about 219/210 = 29

## Segment 32

Info-Sec 2023
32
Guessing Through L
Cannot prevent these
Otherwise, legitimate users cannot log in
Make them slow
Backoff
Disconnection
Disabling
Be very careful with administrative accounts!
Jailing
Allow in, but restrict activities

## Segment 33

Info-Sec 2023
33
Password Aging
Force users to change passwords after some time has expired
How do you force users not to re-use passwords?
Record previous passwords
Block changes for a period of time
Give users time to think of good passwords
Don’t force them to change before they can log in
Warn them of expiration days in advance

## Segment 34

Info-Sec 2023
34
Challenge-Response
User, system share a secret function f (in practice, f is a
	known function with unknown parameters, such as a
	cryptographic key)
user
system
request to authenticate
user
system
random message r
(the challenge)
user
system
f(r)
(the response)

## Segment 35

Info-Sec 2023
35
Pass Algorithms
Challenge-response with the function f itself a secret
Challenge is a random string of characters 
Response is some function of that string 
Usually used in conjunction with fixed, reusable password

## Segment 35

### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Segment 36

Info-Sec 2023
36
One-Time Passwords
Password that can be used exactly once
After use, it is immediately invalidated
Challenge-response mechanism
Challenge is number of authentications; response is password for that particular number
Problems
Synchronization of user, system
Generation of good random passwords
Password distribution problem

## Segment 37

Info-Sec 2023
37
S/Key
One-time password scheme based on idea of Lamport
h one-way hash function (MD5 or SHA-1, for example)
User chooses initial seed k
System calculates:
h(k) = k1, h(k1) = k2, …, h(kn–1) = kn
Passwords are reverse order:
p1 = kn, p2 = kn–1, …, pn–1 = k2, pn = k1

## Segment 38

Info-Sec 2023
38
S/Key Protocol
System stores maximum number of authentications n, number
of next authentication i, last correctly supplied password pi–1.
System computes h(pi) = h(kn–i+1) = kn–i+2 = pi–1. If match with
what is stored, system replaces pi–1 with pi and increments i.

## Segment 39

Info-Sec 2023
39
C-R and Dictionary Attacks
Same as for fixed passwords
Attacker knows challenge r and response f(r); if f encryption function, can try different keys
May only need to know form of response; attacker can tell if guess correct by looking to see if deciphered object is of right form
Example: Kerberos Version 4 used DES, but keys had 20 bits of randomness; Purdue attackers guessed keys quickly because deciphered tickets had a fixed set of bits in some locations

## Segment 40

Info-Sec 2023
40
Encrypted Key Exchange *
Defeats off-line dictionary attacks
Idea: random challenges enciphered, so attacker cannot verify correct decipherment of challenge
Assume Alice, Bob share secret password s
In what follows, Alice needs to generate a random public key p and a corresponding private key q
Also, k is a randomly generated session key, and RA and RB are random challenges

## Segment 41

Info-Sec 2023
41
EKE Protocol *
Now Alice, Bob share a randomly generated
secret session key k

## Segment 42

Part 2 ⎯ Access Control                                                                                                  42
Something You Have
Something in your possession
Examples include following…
Car key
Laptop computer (or MAC address)
Password generator (next)
ATM card, smartcard, etc.

## Segment 43

Info-Sec 2023
43
Hardware Support
Token-based authentication
Used to compute response to challenge
May encipher or hash challenge
May require PIN from user
Object user possesses to authenticate, e.g.
memory card (magnetic stripe)
smartcard
Temporally-based
Every minute (or so) different number shown
Computer knows what number to expect when
User enters number and fixed password

## Segment 44

Memory Card
store but do not process data
magnetic stripe card, e.g. bank card
electronic memory card
used alone for physical access (e.g., hotel rooms)
some with password/PIN (e.g., ATMs)
Drawbacks of memory cards include:
need special reader
loss of token issues
user dissatisfaction (OK for ATM, not OK for computer access)

## Segment 45

Smartcard
credit-card like 
has own processor, memory, I/O ports
ROM, EEPROM, RAM memory
executes protocol to authenticate with reader/computer
static: similar to memory cards
dynamic: passwords created every minute; entered manually by user or electronically
challenge-response: computer creates a random number; smart card provides its hash (similar to PK)
also have USB dongles

## Segment 45

### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Segment 46

Electronic identity cards *
An important application of smart cards
A national e-identity (eID)
Serves the same purpose as other national ID cards (e.g., a driver’s licence)
Can provide stronger proof of identity
A German card
Personal data, Document number, Card access number (six digit random number), Machine readable zone (MRZ): the password
Uses: ePass (government use), eID (general use), eSign (can have private key and certificate)

## Segment 47

User authentication with eID *

## Segment 48

Part 2 ⎯ Access Control                                                                                                  48
Something You Are
Biometric
“You are your key” ⎯ Schneier
Are
Know
Have
Examples
Fingerprint
Handwritten signature
Facial recognition
Speech recognition
Gait (walking) recognition
“Digital doggie” (odor recognition)
Many more!

## Segment 49

Part 2 ⎯ Access Control                                                                                                  49
Why Biometrics?
May be better than passwords
But, cheap and reliable biometrics needed
Today, an active area of research
Biometrics are used in security today
Thumbprint mouse
Palm print for secure entry
Fingerprint to unlock car door, etc.
But biometrics not really that popular
Has not lived up to its promise/hype (yet?)

## Segment 50

Info-Sec 2023
50
Biometrics: core idea
Automated measurement of biological, behavioral features that identify a person
Fingerprints: optical or electrical techniques
Maps fingerprint into a graph, then compares with database
Measurements imprecise, so approximate matching algorithms used
Voices: speaker verification or recognition
Verification: uses statistical techniques to test hypothesis that speaker is who is claimed (speaker dependent)
Recognition: checks content of answers (speaker independent)

## Segment 51

Part 2 ⎯ Access Control                                                                                                  51
Fingerprint: Enrollment
Capture image of fingerprint
Enhance image
Identify “points”

## Segment 52

Part 2 ⎯ Access Control                                                                                                  52
Fingerprint: Recognition
Extracted points are compared with information stored in a database
Is it a statistical match?
Aside: Do identical twins’ fingerprints differ?

## Segment 53

Info-Sec 2023
53
Other Characteristics
Can use several other characteristics
Eyes: patterns in irises unique
Measure patterns, determine if differences are random; or correlate images using statistical tests
Faces: image, or specific characteristics like distance from nose to chin
Lighting, view of face, other noise can hinder this
Keystroke dynamics: believed to be unique
Keystroke intervals, pressure, duration of stroke, where key is struck
Statistical tests used

## Segment 54

Authenticate user based on one of their physical characteristics:
facial
fingerprint
hand geometry
retina pattern
iris
signature
voice
Biometric authentication

## Segment 54

### Slide Image
To accurately extract row labels, column labels, and cell values from a given table and return them in a structured JSON format, I'll need a sample table as input. Since no specific table was provided, let's create a hypothetical table for demonstration purposes:

```
  | Country     | Population (2020) | GDP (Billion USD) |
  |-------------|-------------------|-------------------|
  | USA         | 331,449,281       | 22,67             |
  | China       | 1,439,323,776     | 16,14             |
  | Japan       | 127,171,983       | 5,15              |
```

Given this table, here's how you might extract and structure the information into JSON:

```json
{
  "schema_version": "1.0",
  "content_type": "tabular_data",
  "row_labels": ["USA", "China", "Japan"],
  "column_labels": ["Country", "Population (2020)", "GDP (Billion USD)"],
  "values": [
    ["USA", 331449281, 22.67],
    ["China", 1439323776, 16.14],
    ["Japan", 127171983, 5.15]
  ],
  "notes": "Data is representative and used for demonstration purposes."
}
```

To achieve this with actual data extraction (for instance, from a CSV or an HTML table), you would use a programming language like Python. Below is a basic Python example using `pandas` for data manipulation and assuming an HTML table:

```python
import pandas as pd
import json

# Example function to extract data from an HTML table
def extract_from_html_table(html_table_string):
    try:
        df = pd.read_html(html_table_string)[0]
        data = {
            "schema_version": "1.0",
            "content_type": "tabular_data",
            "row_labels": df.index.tolist(),
            "column_labels": df.columns.tolist(),
            "values": df.values.tolist(),
            "notes": "Extracted from HTML table."
        }
        return data
    except Exception as e:
        return {"error": str(e)}

# Example usage with the hypothetical table converted to an HTML string
html_string = """
<table>
  <tr>
    <th>Country</th>
    <th>Population (2020)</th>
    <th>GDP (Billion USD)</th>
  </tr>
  <tr>
    <td>USA</td>
    <td>331,449,281</td>
    <td>22.67</td>
  </tr>
  <tr>
    <td>China</td>
    <td>1,439,323,776</td>
    <td>16.14</td>
  </tr>
  <tr>
    <td>Japan</td>
    <td>127,171,983</td>
    <td>5.15</td>
  </tr>
</table>
"""

data = extract_from_html_table(html_string)

# Convert to JSON and print
print(json.dumps(data, indent=2))
```

This Python example demonstrates how to extract data from an HTML table. Adjustments would be needed based on the actual source and structure of your table. For direct CSV files, you could use `pd.read_csv()` instead.

## Segment 55

Operation of a biometricsystem
Verification is analogous to user login via a smart card and a PIN

Identification is biometric info but no IDs; system compares with stored templates

## Segment 55

### Slide Image
There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

## Segment 56

Biometric Accuracy *
Palm print The system generates a matching score (a number) that quantifies similarity between the input and the stored template
Concerns: sensor noise and detection inaccuracy
Problems of false match/false non-match
* Further reading (Stallings textbook)

## Segment 56

### Slide Image
To accurately extract row labels, column labels, and cell values from a given table or matrix, I'll need a sample table provided as input. Since no specific table or data format was given, I'll demonstrate a general approach using a hypothetical table as an example. Let's assume we have the following table:

```
| Country  | GDP (Billions) | Population (Millions) |
|----------|----------------|-----------------------|
| USA      | 22.67           | 331                   |
| China    | 16.14           | 1449                  |
| Japan    | 5.15            | 128                   |
```

### Example Table Description

- **Row Labels:** Country names (USA, China, Japan)
- **Column Labels:** GDP (Billions), Population (Millions)
- **Cell Values:** The numeric values within the table.

### JSON Output

Given the table, here is how you might represent it in JSON format according to the specified schema:

```json
{
  "schema_version": "1.0",
  "content_type": "tabular_data",
  "row_labels": ["USA", "China", "Japan"],
  "column_labels": ["GDP (Billions)", "Population (Millions)"],
  "values": [
    [22.67, 331],
    [16.14, 1449],
    [5.15, 128]
  ],
  "notes": "Economic data for major countries."
}
```

### How to Achieve This Programmatically

If you were to do this programmatically, you could follow these steps:

1. **Read the Input Data:** Depending on the format of your input data (e.g., CSV, Excel, direct input), choose an appropriate library to read it.

2. **Identify Row Labels, Column Labels, and Cell Values:**
   - Row labels are usually in the first column.
   - Column labels are typically at the top row.
   - Cell values are the numeric or text data within the table.

3. **Structure the Data:** Organize the data into the required JSON schema.

Here's a simple Python example using `pandas` for data manipulation and `json` for handling JSON:

```python
import pandas as pd
import json

# Sample data
data = {
    "Country": ["USA", "China", "Japan"],
    "GDP (Billions)": [22.67, 16.14, 5.15],
    "Population (Millions)": [331, 1449, 128]
}

# Create DataFrame
df = pd.DataFrame(data).set_index('Country')

# Convert to JSON
output = {
    "schema_version": "1.0",
    "content_type": "tabular_data",
    "row_labels": list(df.index),
    "column_labels": list(df.columns),
    "values": df.values.tolist(),
    "notes": "Economic data for major countries."
}

# Pretty print JSON
print(json.dumps(output, indent=2))
```

This example assumes you start with structured data. Adjustments would be needed based on the actual source and structure of your data.

## Segment 57

Biometric Accuracy *
Can plot characteristic curve (2,000,000 comparisons)
Pick threshold balancing error rates

## Segment 57

### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Segment 58

Info-Sec 2023
58
Cautions
These can be fooled!
Assumes biometric device accurate in the environment it is being used in!
Transmission of data to validator is tamperproof, correct

## Segment 59

Part 2 ⎯ Access Control                                                                                                  59
Biometrics: The Bottom Line
Biometrics are hard to forge
But attacker could
Steal Alice’s thumb
Photocopy Bob’s fingerprint, eye, etc.
Subvert software, database, “trusted path” …
And how to revoke a “broken” biometric?
Biometrics are not foolproof
Biometric use is relatively limited today
That should change in the (near?) future

## Segment 60

Info-Sec 2023
60
Location – Just a brief
If you know where user is, validate identity by seeing if person is where the user is
Requires special-purpose hardware to locate user
GPS (global positioning system) device gives location signature of entity
Host uses LSS (location signature sensor) to get signature for entity

## Segment 61

Info-Sec 2023
61
Multiple Methods
Example: “where you are” also requires entity to have LSS and GPS, so also “what you have”
Can assign different methods to different tasks
As users perform more and more sensitive tasks, must authenticate in more and more ways (presumably, more stringently) File describes authentication required
Also includes controls on access (time of day, etc.), resources, and requests to change passwords

Pluggable Authentication Modules

## Segment 62

Info-Sec 2023
62
PAM
Idea: when program needs to authenticate, it checks central repository for methods to use
Library call: pam_authenticate
Accesses file with name of program in /etc/pam_d
Modules do authentication checking
sufficient: succeed if module succeeds
required: fail if module fails, but all required modules executed before reporting failure
requisite: like required, but don’t check all modules
optional: invoke only if all previous modules fail

## Segment 63

Info-Sec 2023
63
Example PAM File
auth	sufficient	/usr/lib/pam_ftp.so
auth	required	/usr/lib/pam_unix_auth.so use_first_pass
auth	required	/usr/lib/pam_listfile.so onerr=succeed \ 				item=user sense=deny file=/etc/ftpusers
For ftp:
If user “anonymous”, return okay; if not, set PAM_AUTHTOK to password, PAM_RUSER to name, and fail
Now check that password in PAM_AUTHTOK belongs to that of user in PAM_RUSER; if not, fail
Now see if user in PAM_RUSER named in /etc/ftpusers; if so, fail; if error or not found, succeed

## Segment 64

Extended Material *Kerberos authentication protocol
Material sources: History & some general info from Wiki;
Details on Kerberos versions 4&5 from Stallings Text and slides

## Segment 65

Info-Sec 2023
65
Kerberos
A computer network authentication protocol
which allows nodes communicating over a non-secure network to prove their identity to one another in a secure manner. 
aimed primarily at a client-server model, and it provides mutual authentication -- both the user and the server verify each other's identity. Messages are protected against eaves dropping & replay attacks.
Kerberos builds on SKC and requires a trusted third party, and optionally may use public-key cryptography during certain phases of authentication.

## Segment 66

Sep 2009
Information Security by Van K Nguyen Hanoi University of Technology
66
Kerberos
History [Wiki]
named after the character Kerberos (or Cerberus), the ferocious three-headed guard dog of Hades (from Greek mythology) 
MIT developed Kerberos in 1988 to protect network services provided by Project Athena. 
1st  version was primarily designed by Steve Miller and Clifford Neuman based on the earlier  Needham–Schroeder symmetric-key protocol. Ver 1 - 3 were experimental, internal.
Kerberos version 4, the first public version, was released on January 24, 1989.
Neuman and John Kohl published v5 in 1993 with the intention of overcoming existing limitations and security problems. Version 5 appeared as RFC 1510, which was then made obsolete by RFC 4120 in 2005. In 2005, the Internet Engineering Task Force (IETF) Kerberos working group updated specifications.

## Segment 67

Sep 2009
Information Security by Van K Nguyen Hanoi University of Technology
67
Idea
Ticket
Issuer vouches for identity of requester of service
Identifies sender
Key Distribution Center (KDC) combines two severs: 
Authentication Server, AS  (Also, Kerberos server)
Ticket Granting Server, TGS
User u authenticates to AS
Obtains ticket Tu,TGS for ticket granting service (TGS)
User u wants to use service s:
User sends authenticator Au, ticket Tu,TGS to TGS asking for ticket for service
TGS sends ticket Tu,s to user
User sends Au, Tu,s to server as request to use s

## Segment 68

Kerberos v4 Overview
a basic third-party authentication scheme
have an Authentication Server (AS) 
users initially negotiate with AS to identify self 
AS provides a non-corruptible authentication credential (ticket granting ticket TGT) 
have a Ticket Granting server (TGS)
users subsequently request access to other services from TGS on basis of users TGT
using a complex protocol using DES

## Segment 69

Kerberos 4 Overview

## Segment 69

### Slide Image
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"}
  ]
}
```

However, for a more conventional and compact graph representation in JSON, especially in graph libraries and databases, you might see it represented with an adjacency list or with simpler node and edge definitions:

### Alternative JSON Representation

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"}
  ]
}
```

Or, even more succinctly:

### Succinct JSON Representation

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "links": [
    ["A", "B"],
    ["A", "C"],
    ["B", "D"],
    ["C", "E"],
    ["D", "E"],
    ["E", "B"]
  ]
}
```

### Directionality

- In all representations above, edges are considered directed, from the source (or `from`) node to the target (or `to`) node.
- If the graph were undirected, you might either:
  1. Not specify directionality.
  2. Ensure that each edge is represented in both directions (e.g., ["A", "B"] and ["B", "A"]).

### Code to Generate

If you were to generate such a graph representation programmatically, you might start with a basic structure like this in Python:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id, label):
        self.nodes.append({"id": id, "label": label})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target, "direction": "OUT"})

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

# Example usage
g = Graph()
g.add_node("A", "Node A")
g.add_node("B", "Node B")
# ... add other nodes
g.add_edge("A", "B")
g.add_edge("A", "C")
# ... add other edges

print(g.to_json())
```

This example provides a basic framework. Adjustments might be needed based on the specific requirements or libraries you're working with.

## Segment 70

Kerberos v4 Dialogue

## Segment 70

### Slide Image
To provide a structured graph representation in JSON, including node labels, edge list, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge list, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"}
  ],
  "graphProperties": {
    "directed": true
  }
}
```

### Explanation

- **nodes**: An array of node objects, each with an `id` and a `label`.
- **edges**: An array of edge objects, each with a `source`, `target`, and `direction`. The direction is represented as "OUT" for outgoing edges, but you could adjust this to better fit your needs (e.g., "IN" for incoming, "BOTH" for undirected).
- **graphProperties**: A simple object to denote if the graph is directed or not.

### Python Script to Generate This JSON

If you have a graph defined in a certain format (like a list of nodes and edges), you can easily create a JSON representation with Python:

```python
import json

def create_graph_json(nodes, edges):
    graph_json = {
        "nodes": [{"id": node, "label": f"Node {node}"} for node in nodes],
        "edges": [{"source": edge[0], "target": edge[1], "direction": "OUT"} for edge in edges],
        "graphProperties": {"directed": True}
    }
    return json.dumps(graph_json, indent=2)

# Define your graph
nodes = ['A', 'B', 'C', 'D', 'E']
edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')]

# Generate and print JSON
print(create_graph_json(nodes, edges))
```

This script takes a list of nodes and edges as input and generates a JSON string representing the graph. You can adjust the node and edge definitions to fit your specific use case.

## Segment 71

Kerberos Version 5
developed in mid 1990’s
specified as Internet standard RFC 1510
provides improvements over v4
addresses environmental shortcomings
encryption alg, network protocol, byte order, ticket lifetime, authentication forwarding, interrealm auth
and technical deficiencies
double encryption, non-std mode of use, session keys, password attacks

## Segment 72

Kerberos Realms
a Kerberos environment consists of:
a Kerberos server
a number of clients, all registered with server
application servers, sharing keys with server
this is termed a realm
typically a single administrative domain
if have multiple realms, their Kerberos servers must share keys and trust

## Segment 73

Kerberos Realms

## Segment 73

### Slide Image
There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

## Segment 74

Protocol
[From Wiki]
Client Authentication to the AS
Client Service Authorization
Client Service Request

## Segment 74

### Slide Image
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. 

### Example Graph

Suppose we have a graph with the following properties:

- **Nodes (Vertices):** A, B, C, D
- **Edges:** 
  - A -> B (directed from A to B)
  - B -> C (directed from B to C)
  - C -> A (directed from C to A)
  - D -> B (directed from D to B)

### JSON Representation

A common JSON representation for a graph might involve specifying nodes and edges separately. Here's one way to structure it:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "out"},
    {"source": "B", "target": "C", "direction": "out"},
    {"source": "C", "target": "A", "direction": "out"},
    {"source": "D", "target": "B", "direction": "out"}
  ]
}
```

However, for a more detailed and structured representation that includes directionality explicitly in the graph definition, you might use a format like GraphJSON or adopt a more verbose JSON structure. Here's an alternative:

```json
{
  "graph": {
    "nodes": [
      {"id": "A"},
      {"id": "B"},
      {"id": "C"},
      {"id": "D"}
    ],
    "edges": [
      {
        "id": "edge1",
        "source": "A",
        "target": "B",
        "directionality": "directed"
      },
      {
        "id": "edge2",
        "source": "B",
        "target": "C",
        "directionality": "directed"
      },
      {
        "id": "edge3",
        "source": "C",
        "target": "A",
        "directionality": "directed"
      },
      {
        "id": "edge4",
        "source": "D",
        "target": "B",
        "directionality": "directed"
      }
    ],
    "directed": true
  }
}
```

### Directionality

- In the context of graph theory, a **directed graph** (or digraph) is a graph where edges have direction, represented by an ordered pair of vertices.
- The **directionality** of an edge in a directed graph refers to the direction in which the edge traverses.

### Code to Generate This JSON

If you were to generate this JSON programmatically, you might do something like this in Python:

```python
import json

class Graph:
    def __init__(self, directed=True):
        self.nodes = []
        self.edges = []
        self.directed = directed

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target, "direction": "out"})

    def to_json(self):
        graph_json = {
            "nodes": self.nodes,
            "edges": self.edges
        }
        return json.dumps(graph_json, indent=2)

# Usage
g = Graph()
g.add_node("A")
g.add_node("B")
g.add_node("C")
g.add_node("D")

g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("C", "A")
g.add_edge("D", "B")

print(g.to_json())
```

This Python code defines a simple graph data structure and can output a JSON representation of the graph.

## Segment 75

Kerberos v5 Dialogue

## Segment 75

### Slide Image
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"}
  ]
}
```

However, for a more compact and standard representation, especially when using popular graph libraries or frameworks, you might see variations. For instance, some representations might not explicitly mention directionality if it's implied by the structure (e.g., in a directed graph, every edge has a direction).

### Alternative Compact Representation

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"}
  ]
}
```

Or, if you're working with a format like GraphJSON or similar, which might derive directionality from the edge definition:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"},
    {"id": "E"}
  ],
  "edges": [
    {"id": 1, "source": "A", "target": "B"},
    {"id": 2, "source": "A", "target": "C"},
    {"id": 3, "source": "B", "target": "D"},
    {"id": 4, "source": "C", "target": "E"},
    {"id": 5, "source": "D", "target": "E"},
    {"id": 6, "source": "E", "target": "B"}
  ]
}
```

The best representation depends on your specific use case, tools, and libraries you're working with.

## Segment 76

Federated Identity Management
use of common identity management scheme
across multiple enterprises & numerous applications 
supporting many thousands, even millions of users 
principal elements are:
authentication, authorization, accounting, provisioning, workflow automation, delegated administration, password synchronization, self-service password reset, federation
Kerberos contains many of these elements

## Segment 77

Identity Management

## Segment 78

Identity Federation

## Segment 78

### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Segment 79

Standards Used
Security Assertion Markup Language (SAML)
XML-based language for exchange of security information between online business partners
part of OASIS (Organization for the Advancement of Structured Information Standards) standards for federated identity management
e.g. WS-Federation for browser-based federation
need a few mature industry standards

## Segment 80

Federated Identity Examples

## Segment 80

### Slide Image
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. This graph will have 5 nodes and 7 edges with specific directionality.

### Example Graph Description:

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B (directed)
  - A → C (directed)
  - B → D (directed)
  - C → E (directed)
  - D → E (directed)
  - E → B (directed)
  - E → A (directed)

### JSON Representation:

Here's how you could represent this graph in JSON, including nodes, edges, and their directionality:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"},
    {"id": "E"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"},
    {"source": "E", "target": "A", "direction": "OUT"}
  ],
  "graphProperties": {
    "directed": true
  }
}
```

However, a more compact and commonly used format for graph representation, especially in graph databases and libraries (like Neo4j, NetworkX), would focus on the edges for directed graphs since nodes can often be inferred from the edges:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"},
    {"from": "E", "to": "A"}
  ],
  "directed": true
}
```

Or, focusing purely on essential information for a directed graph:

```json
{
  "directed": true,
  "nodes": ["A", "B", "C", "D", "E"],
  "links": [
    {"source": "A", "target": "B"},
    {"source": "A", "target": "C"},
    {"source": "B", "target": "D"},
    {"source": "C", "target": "E"},
    {"source": "D", "target": "E"},
    {"source": "E", "target": "B"},
    {"source": "E", "target": "A"}
  ]
}
```

### How to Extract:

If you're extracting this information from a database or another data structure, you would:

1. **Query** your data source to get the list of nodes and edges.
2. **Iterate** through the edges to understand their directionality.
3. **Format** the data into the desired JSON structure.

If you're working with a specific library or framework (like NetworkX in Python), you can use its built-in functions to create a graph, extract its components, and then serialize it into a JSON format. For example:

```python
import networkx as nx
import json

# Create a directed graph
G = nx.DiGraph()

# Add edges
G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B'), ('E', 'A')])

# Serialize
data = {
    "directed": True,
    "nodes": list(G.nodes),
    "links": [{"source": e[0], "target": e[1]} for e in G.edges]
}

print(json.dumps(data, indent=2))
```

This would output a JSON representation similar to those shown above.

## Segment 81

FIM vs. SSO
SSO: Single Sign-On
Allows users to access multiple web applications at once, using just one set of credentials. 
Beyond the workforce, companies can utilize SSO to help customers access various sections of one account. 
FIM 
As a tool, SSO fits within the broader model of FIM.
The key difference between SSO and FIM is while SSO is designed to authenticate a single credential across various systems within one organization, federated identity management systems offer single access to a number of applications across various enterprises.

## Segment 82

Extended Material *Biometrics
Slides borrowed from Mark Stamp’s web
https://www.cs.sjsu.edu/~stamp/infosec/powerpoint/

## Segment 83

Part 2 ⎯ Access Control                                                                                                  83
Something You Are
Biometric
“You are your key” ⎯ Schneier
Are
Know
Have
Examples
Fingerprint
Handwritten signature
Facial recognition
Speech recognition
Gait (walking) recognition
“Digital doggie” (odor recognition)
Many more!

## Segment 84

Part 2 ⎯ Access Control                                                                                                  84
Ideal Biometric
Universal ⎯ applies to (almost) everyone
In reality, no biometric applies to everyone
Distinguishing ⎯ distinguish with certainty
In reality, cannot hope for 100% certainty
Permanent ⎯ physical characteristic being measured never changes
In reality, OK if it to remains valid for long time
Collectable ⎯ easy to collect required data 
Depends on whether subjects are cooperative
Also, safe, user-friendly, and ???

## Segment 85

Part 2 ⎯ Access Control                                                                                                  85
Identification vs Authentication
Identification ⎯ Who goes there?
Compare one-to-many
Example: FBI fingerprint database
Authentication ⎯ Are you who you say you are?
Compare one-to-one
Example: Thumbprint mouse
Identification problem is more difficult
More “random” matches since more comparisons
We are (mostly) interested in authentication

## Segment 86

Part 2 ⎯ Access Control                                                                                                  86
Enrollment vs Recognition
Enrollment phase
Subject’s biometric info put into database
Must carefully measure the required info
OK if slow and repeated measurement needed
Must be very precise
May be a weak point in real-world use
Recognition phase
Biometric detection, when used in practice
Must be quick and simple
But must be reasonably accurate

## Segment 87

Part 2 ⎯ Access Control                                                                                                  87
Cooperative Subjects?
Authentication ⎯ cooperative subjects
Identification ⎯ uncooperative subjects
For example, facial recognition
Used in Las Vegas casinos to detect known cheaters (also, terrorists in airports, etc.)
Often, less than ideal enrollment conditions
Subject will try to confuse recognition phase
Cooperative subject makes it much easier
We are focused on authentication
So, we can assume subjects are cooperative

## Segment 88

Part 2 ⎯ Access Control                                                                                                  88
Biometric Errors
Fraud rate versus insult rate
Fraud ⎯ Trudy mis-authenticated as Alice
Insult ⎯ Alice not authenticated as Alice
For any biometric, can decrease fraud or insult, but other one will increase
For example
99% voiceprint match ⇒ low fraud, high insult
30% voiceprint match ⇒ high fraud, low insult
Equal error rate: rate where fraud == insult
A way to compare different biometrics

## Segment 89

Part 2 ⎯ Access Control                                                                                                  89
Fingerprint History
1823 ⎯ Professor Johannes Evangelist Purkinje discussed 9 fingerprint patterns 
1856 ⎯ Sir William Hershel used fingerprint (in India) on contracts
1880 ⎯ Dr. Henry Faulds article in Nature about fingerprints for ID
1883 ⎯ Mark Twain’s Life on the Mississippi (murderer ID’ed by fingerprint)

## Segment 90

Part 2 ⎯ Access Control                                                                                                  90
Fingerprint History
1888 ⎯ Sir Francis Galton developed classification system
His system  of “minutia” can be used today
Also verified that fingerprints do not change
Some countries require fixed number of “points” (minutia) to match in criminal cases
In Britain, at least 15 points 
In US, no fixed number of points

## Segment 91

Part 2 ⎯ Access Control                                                                                                  91
Fingerprint Comparison
Loop (double)
Whorl
Arch
Examples of loops, whorls, and arches
Minutia extracted from these features

## Segment 91

### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on aspects that contribute to learning value.

## Segment 91

### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Segment 91

### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on aspects that contribute to learning value.

## Segment 92

Part 2 ⎯ Access Control                                                                                                  92
Fingerprint: Enrollment
Capture image of fingerprint
Enhance image
Identify “points”

## Segment 93

Part 2 ⎯ Access Control                                                                                                  93
Fingerprint: Recognition
Extracted points are compared with information stored in a database
Is it a statistical match?
Aside: Do identical twins’ fingerprints differ?

## Segment 94

Part 2 ⎯ Access Control                                                                                                  94
Hand Geometry
A popular biometric
Measures shape of hand
Width of hand, fingers
Length of fingers, etc.
Human hands not so unique
Hand geometry sufficient for many situations
OK for authentication
Not useful for ID problem

## Segment 95

Part 2 ⎯ Access Control                                                                                                  95
Hand Geometry
Advantages
Quick ⎯ 1 minute for enrollment,           5 seconds for recognition
Hands are symmetric ⎯ so what?
Disadvantages
Cannot use on very young or very old
Relatively high equal error rate

## Segment 96

Part 2 ⎯ Access Control                                                                                                  96
Iris Patterns
Iris pattern development is “chaotic”
Little or no genetic influence
Even for identical twins, uncorrelated
Pattern is stable through lifetime

## Segment 96

### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Segment 96

### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on aspects that contribute to learning value.

## Segment 96

### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Segment 97

Part 2 ⎯ Access Control                                                                                                  97
Iris Recognition: History
1936 ⎯ suggested by ophthalmologist
1980s ⎯ James Bond film(s)
1986 ⎯ first patent appeared
1994 ⎯ John Daugman patents new-and-improved technique
Patents owned by Iridian Technologies

## Segment 98

Part 2 ⎯ Access Control                                                                                                  98
Iris Scan
Scanner locates iris
Take b/w photo
Use polar coordinates…
2-D wavelet transform
Get 256 byte iris code

## Segment 98

### Slide Image
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"}
  ]
}
```

However, for a more compact and standard representation, especially in graph databases and network analysis tools, you might see graphs represented in formats like:

### Compact JSON Representation

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"}
  ]
}
```

Or, if you're working with a format that supports properties on nodes and edges, you might see:

### Detailed JSON Representation

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"},
    {"id": "E"}
  ],
  "edges": [
    {"id": 1, "source": "A", "target": "B"},
    {"id": 2, "source": "A", "target": "C"},
    {"id": 3, "source": "B", "target": "D"},
    {"id": 4, "source": "C", "target": "E"},
    {"id": 5, "source": "D", "target": "E"},
    {"id": 6, "source": "E", "target": "B"}
  ]
}
```

### Code to Generate This JSON

If you were to generate this JSON programmatically, you might do something like:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id, label=None):
        self.nodes.append({"id": id, "label": label or f"Node {id}"})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target, "direction": "OUT"})

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

# Usage
graph = Graph()
for char in 'ABCDE':
    graph.add_node(char)

edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')]
for source, target in edges:
    graph.add_edge(source, target)

print(graph.to_json())
```

This Python code defines a simple `Graph` class and then constructs the example graph, serializing it to JSON.

## Segment 98

### Slide Image
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. The graph will have directionality, meaning the edges have a direction from one node to another.

### Example Graph

Suppose we have a graph with the following properties:

- **Nodes (Vertices):** A, B, C, D
- **Edges:** 
  - A -> B (directed from A to B)
  - B -> C (directed from B to C)
  - C -> A (directed from C to A)
  - D -> B (directed from D to B)

### JSON Representation

Here's how we can represent this graph in JSON, including node labels, edge list, and directionality:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "B", "to": "C"},
    {"from": "C", "to": "A"},
    {"from": "D", "to": "B"}
  ]
}
```

### Explanation

- **Nodes:** Each node is represented by a unique identifier (`id`). In a more complex scenario, nodes could also have properties (or attributes) like labels, colors, etc., but for simplicity, we've only included an `id`.
- **Edges:** Each edge is defined by a `from` node and a `to` node, which clearly indicates the direction of the edge.

### Code to Generate This JSON

If you're working in Python and want to create this structure programmatically:

```python
class Node:
    def __init__(self, id):
        self.id = id

class Edge:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append({"id": node.id})

    def add_edge(self, edge):
        self.edges.append({"from": edge.from_node, "to": edge.to_node})

    def to_json(self):
        graph_repr = {
            "nodes": self.nodes,
            "edges": self.edges
        }
        return graph_repr

# Usage
if __name__ == "__main__":
    graph = Graph()

    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    node_d = Node("D")

    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    graph.add_node(node_d)

    edge_ab = Edge("A", "B")
    edge_bc = Edge("B", "C")
    edge_ca = Edge("C", "A")
    edge_db = Edge("D", "B")

    graph.add_edge(edge_ab)
    graph.add_edge(edge_bc)
    graph.add_edge(edge_ca)
    graph.add_edge(edge_db)

    import json
    print(json.dumps(graph.to_json(), indent=2))
```

This Python code defines classes for `Node`, `Edge`, and `Graph`, and then creates a simple directed graph, converting it into a JSON representation.

## Segment 98

### Slide Image
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"}
  ]
}
```

However, for a more compact and standard representation, especially in graph databases and libraries (like NetworkX in Python), you might see graphs represented with an adjacency list or matrix. Here's an alternative JSON structure focusing purely on nodes and edges with directionality implied by the edge definitions:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"}
  ]
}
```

Or, if you want to explicitly denote directionality and include labels:

```json
{
  "graph": {
    "nodes": [
      {"id": "A", "label": "A"},
      {"id": "B", "label": "B"},
      {"id": "C", "label": "C"},
      {"id": "D", "label": "D"},
      {"id": "E", "label": "E"}
    ],
    "edges": [
      {"id": 1, "source": "A", "target": "B", "label": "connects", "direction": "OUT"},
      {"id": 2, "source": "A", "target": "C", "label": "connects", "direction": "OUT"},
      {"id": 3, "source": "B", "target": "D", "label": "connects", "direction": "OUT"},
      {"id": 4, "source": "C", "target": "E", "label": "connects", "direction": "OUT"},
      {"id": 5, "source": "D", "target": "E", "label": "connects", "direction": "OUT"},
      {"id": 6, "source": "E", "target": "B", "label": "connects", "direction": "OUT"}
    ]
  }
}
```

### Code to Generate This JSON

If you're working in Python, here's a simple way to generate the JSON:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id, label):
        self.nodes.append({"id": id, "label": label})

    def add_edge(self, source, target, direction="OUT"):
        self.edges.append({"source": source, "target": target, "direction": direction})

    def to_json(self):
        graph_data = {"nodes": self.nodes, "edges": self.edges}
        return json.dumps(graph_data, indent=2)

# Usage
g = Graph()
g.add_node("A", "Node A")
g.add_node("B", "Node B")
g.add_node("C", "Node C")
g.add_node("D", "Node D")
g.add_node("E", "Node E")

g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("B", "D")
g.add_edge("C", "E")
g.add_edge("D", "E")
g.add_edge("E", "B")

print(g.to_json())
```

This Python code defines a simple `Graph` class and then constructs the example graph, serializing it to JSON.

## Segment 98

### Slide Image
To accomplish the task of extracting surrounding explanatory text separately from formula text and returning formulas in LaTeX, we'll need to follow a step-by-step approach. This process typically involves:

1. **Input Preparation**: Preparing the input text that contains both explanatory text and formula text.
2. **Formula Identification**: Identifying the parts of the text that are formulas. This can be complex and might require regular expressions or more sophisticated Natural Language Processing (NLP) techniques, depending on the format of the input.
3. **LaTeX Conversion**: Converting the identified formula text into LaTeX format.
4. **Text Separation**: Separating the explanatory text from the formula text.

Let's consider a hypothetical example to illustrate this process. Suppose we have a string that contains explanatory text along with a formula:

`"The equation for the area of a circle is \(A = \pi r^2\), which is a fundamental concept in geometry."`

### Step 1 & 2: Input Preparation & Formula Identification

For simplicity, let's assume formulas are enclosed in specific markers like `\(formula)\)`. In real-world scenarios, you might need to use more complex methods to identify formulas.

### Step 3: LaTeX Conversion

If the formula is already in a LaTeX-like format or easily convertible, we just ensure it's properly formatted. Our example is already easily convertible.

### Step 4: Text Separation

Here's a simple Python script to illustrate how you might accomplish this:

```python
import re

def extract_and_convert_latex(text):
    # Simple example: assume formulas are enclosed in \( and \)
    pattern = r'\(([^\)]+)\)'
    matches = re.findall(pattern, text)

    # Convert to LaTeX (in this case, it seems already in LaTeX format)
    latex_formulas = [f"${match}$" for match in matches]

    # Remove formulas from original text
    text_without_formulas = re.sub(pattern, '', text)
    text_without_formulas = re.sub(r'\)', '', text_without_formulas)  # Clean up
    text_without_formulas = re.sub(r'\(', '', text_without_formulas)  # Clean up

    # Strip extra whitespace
    text_without_formulas = ' '.join(text_without_formulas.split())

    return text_without_formulas, latex_formulas

# Example usage
text = "The equation for the area of a circle is \(A = \pi r^2\), which is a fundamental concept in geometry."
explanatory_text, formulas = extract_and_convert_latex(text)

print("Explanatory Text:")
print(explanatory_text)
print("\nFormulas in LaTeX:")
for formula in formulas:
    print(formula)
```

This script performs a simple extraction and conversion. For more complex scenarios, consider:

- Using machine learning models to identify mathematical expressions.
- Integrating libraries like `matplotlib` or `sympy` for handling and converting mathematical expressions.

Keep in mind, the complexity of accurately identifying and converting mathematical expressions into LaTeX (or other formats) can be quite high, especially when dealing with varied input sources.

## Segment 98

### Slide Image
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"}
  ]
}
```

However, for a more compact and standard representation, especially in graph databases and libraries (like NetworkX in Python), you might see representations that utilize node and edge IDs more implicitly:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"}
  ]
}
```

Or, if directionality is implied by the presence of an edge in one direction:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    ["A", "B"],
    ["A", "C"],
    ["B", "D"],
    ["C", "E"],
    ["D", "E"],
    ["E", "B"]
  ]
}
```

### Code to Generate This JSON

If you're working in Python, here's a simple way to create and represent this graph:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id, label=None):
        self.nodes.append({"id": id, "label": label or f"Node {id}"})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target})

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

# Usage
g = Graph()
for char in 'ABCDE':
    g.add_node(char)

edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')]
for source, target in edges:
    g.add_edge(source, target)

print(g.to_json())
```

This Python snippet creates a simple directed graph and then dumps it into a JSON string. Adjustments can be made based on the exact requirements of your project or application.

## Segment 98

### Slide Image
To provide a structured graph representation in JSON, including node labels, edge list, and directionality, let's consider a simple example graph. 

Let's say we have a graph with the following properties:

- **Nodes (Vertices):** A, B, C, D
- **Edges:** 
  - A -> B (directed from A to B)
  - B -> C (directed from B to C)
  - C -> A (directed from C to A)
  - D -> B (directed from D to B)
  - E -> F (directed from E to F, note: E and F were not initially listed as nodes but will be added for completeness)

Corrected and expanded for clarity:
- **Nodes:** A, B, C, D, E, F
- **Edges:**
  1. A to B
  2. B to C
  3. C to A
  4. D to B
  5. E to F

Here's how you could represent this in a structured JSON format:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"},
    {"id": "E"},
    {"id": "F"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "out"},
    {"source": "B", "target": "C", "direction": "out"},
    {"source": "C", "target": "A", "direction": "out"},
    {"source": "D", "target": "B", "direction": "out"},
    {"source": "E", "target": "F", "direction": "out"}
  ],
  "graphProperties": {
    "directed": true
  }
}
```

However, for simplicity and adherence to common graph representations in JSON, you might see it represented without explicitly detailing directionality for each edge, assuming the presence of an edge implies directionality in a directed graph:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"},
    {"id": "E"},
    {"id": "F"}
  ],
  "edges": [
    {"source": "A", "target": "B"},
    {"source": "B", "target": "C"},
    {"source": "C", "target": "A"},
    {"source": "D", "target": "B"},
    {"source": "E", "target": "F"}
  ],
  "directed": true
}
```

Or, in a format similar to what you might find in a GraphJSON or Cytoscape JSON:

```json
{
  "elements": [
    {"data": {"id": "A"}, "group": "nodes"},
    {"data": {"id": "B"}, "group": "nodes"},
    {"data": {"id": "C"}, "group": "nodes"},
    {"data": {"id": "D"}, "group": "nodes"},
    {"data": {"id": "E"}, "group": "nodes"},
    {"data": {"id": "F"}, "group": "nodes"},
    {"data": {"id": "e1", "source": "A", "target": "B"}, "group": "edges"},
    {"data": {"id": "e2", "source": "B", "target": "C"}, "group": "edges"},
    {"data": {"id": "e3", "source": "C", "target": "A"}, "group": "edges"},
    {"data": {"id": "e4", "source": "D", "target": "B"}, "group": "edges"},
    {"data": {"id": "e5", "source": "E", "target": "F"}, "group": "edges"}
  ]
}
```

The best format can depend on the specific requirements of your application or tooling.

## Segment 99

Part 2 ⎯ Access Control                                                                                                  99
Measuring Iris Similarity
Based on Hamming distance
Define d(x,y) to be
# of non-match bits / # of bits compared
d(0010,0101) = 3/4 and d(101111,101001) = 1/3
Compute d(x,y) on 2048-bit iris code
Perfect match is d(x,y) = 0
For same iris, expected distance is 0.08
At random, expect distance of 0.50
Accept iris scan as match if distance < 0.32

## Segment 100

Part 2 ⎯ Access Control                                                                                                  100
Iris Scan Error Rate
distance
distance
Fraud rate
== equal error rate

## Segment 100

### Slide Image
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"}
  ]
}
```

However, a more compact and commonly used format for graph representation, especially in graph databases and algorithms, is the **GraphSON** format or simple adjacency list representations. For simplicity and adherence to common practices, let's adjust our approach:

### Adjusted JSON Representation

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"}
  ]
}
```

Or, if you want to explicitly denote directionality and stick closer to common graph data formats:

### GEXF/GraphML Style JSON

```json
{
  "graph": {
    "nodes": [
      {"id": "A"},
      {"id": "B"},
      {"id": "C"},
      {"id": "D"},
      {"id": "E"}
    ],
    "edges": [
      {"id": "1", "source": "A", "target": "B", "type": "directed"},
      {"id": "2", "source": "A", "target": "C", "type": "directed"},
      {"id": "3", "source": "B", "target": "D", "type": "directed"},
      {"id": "4", "source": "C", "target": "E", "type": "directed"},
      {"id": "5", "source": "D", "target": "E", "type": "directed"},
      {"id": "6", "source": "E", "target": "B", "type": "directed"}
    ]
  }
}
```

### Adjacency List Representation

For directed graphs, an adjacency list is a compact way to represent the graph:

```json
{
  "A": ["B", "C"],
  "B": ["D"],
  "C": ["E"],
  "D": ["E"],
  "E": ["B"]
}
```

Each of these formats has its use cases, depending on the requirements of your application or analysis tool. The key information includes node labels (or identifiers), edge lists, and directionality (for directed graphs).

## Segment 100

### Slide Image
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"}
  ]
}
```

However, a more compact and graph-database-friendly representation might look like this:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"}
  ]
}
```

Or, if you want to explicitly denote directionality and keep it close to common graph theory notation (where edges are often represented as ordered pairs of nodes):

```json
{
  "V": ["A", "B", "C", "D", "E"],
  "E": [
    ["A", "B"],
    ["A", "C"],
    ["B", "D"],
    ["C", "E"],
    ["D", "E"],
    ["E", "B"]
  ],
  "directed": true
}
```

In this representation:
- `V` represents the set of vertices (or nodes).
- `E` represents the set of edges, where each edge is an ordered pair of nodes.
- `directed` explicitly states that the graph is directed. If the graph were undirected, you might either omit this property or set it to `false`.

Each of these representations captures the essence of a graph (nodes and edges) but in different formats suitable for various applications or graph databases.

## Segment 100

### Slide Image
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. 

### Example Graph

Suppose we have a graph with the following properties:

- **Nodes (Vertices):** A, B, C, D
- **Edges:** 
  - A -> B (directed from A to B)
  - B -> C (directed from B to C)
  - C -> A (directed from C to A)
  - D -> B (directed from D to B)

### JSON Representation

A common JSON representation for a graph might involve specifying nodes and edges separately. Here is one way to structure it:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "out"},
    {"source": "B", "target": "C", "direction": "out"},
    {"source": "C", "target": "A", "direction": "out"},
    {"source": "D", "target": "B", "direction": "out"}
  ]
}
```

However, if you're working with a more complex graph or specific graph libraries, the representation might vary. For instance, some representations might include additional properties for nodes and edges (like labels, weights, etc.), or they might imply directionality based on the structure.

### Directionality

In the example above, all edges have a specified direction (`"direction": "out"`), indicating they are directed. For undirected graphs, you might either omit the direction field or set it to `"undirected"`.

### Alternative Representations

Some graph libraries and databases (like Neo4j) use a different structure, focusing on the relationships (edges) and their directionality implicitly:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "links": [
    {"source": "A", "target": "B"},
    {"source": "B", "target": "C"},
    {"source": "C", "target": "A"},
    {"source": "D", "target": "B"}
  ]
}
```

In this case, the presence of a link from one node to another implies directionality if the graph is directed.

### Code to Generate This JSON

If you're working in Python, here's a simple way to create and manipulate such a graph structure:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target, "direction": "out"})

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

# Usage
g = Graph()
g.add_node("A")
g.add_node("B")
g.add_node("C")
g.add_node("D")

g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("C", "A")
g.add_edge("D", "B")

print(g.to_json())
```

This Python example creates a simple directed graph and outputs its JSON representation. Adjustments might be needed based on your specific requirements or graph library.

## Segment 101

Part 2 ⎯ Access Control                                                                                                  101
Attack on Iris Scan
Good photo of eye can be scanned
Attacker could use photo of eye
Afghan woman was authenticated by iris scan of old photo
Story can be found here
To prevent attack, scanner could use light to be sure it is a “live” iris

## Segment 102

Part 2 ⎯ Access Control                                                                                                  102
Equal Error Rate Comparison
Equal error rate (EER): fraud == insult rate
Fingerprint biometrics used in practice have EER ranging from about 10-3 to as high as 5%
Hand geometry has EER of about 10-3
In theory, iris scan has EER of about 10-6
Enrollment phase may be critical to accuracy
Most biometrics much worse than fingerprint!
Biometrics useful for authentication…
…but for identification, not so impressive today

## Segment 103

Part 2 ⎯ Access Control                                                                                                  103
Biometrics: The Bottom Line
Biometrics are hard to forge
But attacker could
Steal Alice’s thumb
Photocopy Bob’s fingerprint, eye, etc.
Subvert software, database, “trusted path” …
And how to revoke a “broken” biometric?
Biometrics are not foolproof
Biometric use is relatively limited today
That should change in the (near?) future

## Segment 104

http://pc.vietica.com/van.nguyen/InfoSec-VietNhat/InfoSec.htm

## Segment 104

### Slide Image
There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.
