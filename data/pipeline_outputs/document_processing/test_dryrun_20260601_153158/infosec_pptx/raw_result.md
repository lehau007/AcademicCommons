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
There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

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
To accurately extract row labels, column labels, and cell values from a given table or matrix and return them in a structured JSON format, I'll need a sample table as input. Since no specific table was provided, I'll demonstrate the process with a hypothetical example.

Let's assume we have the following table:

| **Country** | **City** | **Population (in millions)** | **Area (in km²)** |
|-------------|----------|-----------------------------|------------------|
| France      | Paris    | 2.1                          | 1054             |
| Japan       | Tokyo    | 13.9                         | 1424             |
| Brazil      | São Paulo| 22.1                         | 1221             |

The structured JSON output based on this table would look like this:

```json
{
  "schema_version": "1.0",
  "content_type": "table",
  "row_labels": ["France", "Japan", "Brazil"],
  "column_labels": ["City", "Population (in millions)", "Area (in km²)"],
  "values": [
    ["Paris", 2.1, 1054],
    ["Tokyo", 13.9, 1424],
    ["São Paulo", 22.1, 1221]
  ],
  "notes": "Population and Area values are approximate."
}
```

However, to make the JSON more detailed and clear, especially regarding which city belongs to which country, we might adjust the structure to include a unique identifier for each row (if available) or ensure the country is clearly associated with each city. Here's an alternative:

```json
{
  "schema_version": "1.0",
  "content_type": "table",
  "row_labels": ["France", "Japan", "Brazil"],
  "column_labels": ["City", "Population (in millions)", "Area (in km²)"],
  "values": [
    {
      "City": "Paris",
      "Population (in millions)": 2.1,
      "Area (in km²)": 1054
    },
    {
      "City": "Tokyo",
      "Population (in millions)": 13.9,
      "Area (in km²)": 1424
    },
    {
      "City": "São Paulo",
      "Population (in millions)": 22.1,
      "Area (in km²)": 1221
    }
  ],
  "notes": "Population and Area values are approximate."
}
```

Or, preserving the original table's structure more closely:

```json
{
  "schema_version": "1.0",
  "content_type": "table",
  "data": [
    {
      "Country": "France",
      "City": "Paris",
      "Population (in millions)": 2.1,
      "Area (in km²)": 1054
    },
    {
      "Country": "Japan",
      "City": "Tokyo",
      "Population (in millions)": 13.9,
      "Area (in km²)": 1424
    },
    {
      "Country": "Brazil",
      "City": "São Paulo",
      "Population (in millions)": 22.1,
      "Area (in km²)": 1221
    }
  ],
  "notes": "Population and Area values are approximate."
}
```

For actual implementation, you would:

1. **Read the table**: Depending on the source, use libraries like pandas in Python for data manipulation.
2. **Extract headers and data**: Use methods like `df.columns` for column labels and `df.values` or iteration for row values.
3. **Serialize to JSON**: Use JSON libraries (e.g., `json.dumps()` in Python) to convert your structured data into JSON format.

Here's a simple Python example:

```python
import pandas as pd
import json

# Sample data
data = {
    "Country": ["France", "Japan", "Brazil"],
    "City": ["Paris", "Tokyo", "São Paulo"],
    "Population (in millions)": [2.1, 13.9, 22.1],
    "Area (in km²)": [1054, 1424, 1221]
}

df = pd.DataFrame(data).set_index('Country')

# Preparing data
schema_version = "1.0"
content_type = "table"
row_labels = df.index.tolist()
column_labels = df.columns.tolist()
values = df.to_dict(orient='index')

# JSON
output = {
    "schema_version": schema_version,
    "content_type": content_type,
    "row_labels": row_labels,
    "column_labels": column_labels,
    "values": values,
    "notes": "Sample note."
}

# Convert to JSON
json_output = json.dumps(output, indent=2)

print(json_output)
```

This example assumes a pandas DataFrame but can be adapted to work with any data structure or source.

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
[LLM_ERROR] All providers failed: Gemini (timed out), Azure, Groq (Error code: 429 - {'error': {'message': 'Rate limit reached for model `meta-llama/llama-4-scout-17b-16e-instruct` in organization `org_01kkedd9pnejqr8cfvvrfp64h7` service tier `on_demand` on requests per minute (RPM): Limit 30, Used 30, Requested 1. Please try again in 2s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'requests', 'code': 'rate_limit_exceeded'}}).

## Segment 57

Biometric Accuracy *
Can plot characteristic curve (2,000,000 comparisons)
Pick threshold balancing error rates

## Segment 57

### Slide Image
There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

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
There is no visual element provided for me to describe. Please share the visual element, and I will focus on describing the content that contributes to its learning value.

## Segment 70

Kerberos v4 Dialogue

## Segment 70

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

However, a more compact and commonly used representation for graphs, especially in graph databases and algorithms, is to use an adjacency list or to directly list nodes with their neighbors. For directed graphs, you might see representations that inherently imply directionality.

### Alternative Adjacency List Representation

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

Or, even more compactly, an adjacency list:

```json
{
  "A": ["B", "C"],
  "B": ["D"],
  "C": ["E"],
  "D": ["E"],
  "E": ["B"]
}
```

The best representation depends on your specific use case, such as the graph library you're using, the operations you'll be performing, and personal or project preference. 

To **extract** node labels, edge lists, and directionality from a graph (assuming it's already in a structured format), you would typically parse the JSON and access the respective fields. For example, in Python:

```python
import json

# Assuming graph_json is your JSON string
graph_json = '''
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
'''

graph = json.loads(graph_json)

node_labels = {node['id']: node['label'] for node in graph['nodes']}
edges = [(edge['source'], edge['target'], edge['direction']) for edge in graph['edges']]

print("Node Labels:", node_labels)
print("Edges:", edges)
```

This example extracts node labels into a dictionary and edges into a list of tuples.

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
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

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

In the provided example, all edges have a clear direction specified (`out` for outgoing, but you might also see `in` for incoming if the representation includes that). If an edge is undirected, you might see a notation like `"direction": "both"` or simply omit the directionality field for undirected graphs.

### Alternative Representations

Some graph formats (like GraphJSON or Cytoscape.js) might structure the data differently. For example, consider a simple directed graph:

```json
{
  "elements": [
    {"data": {"id": "A"}},
    {"data": {"id": "B"}},
    {"data": {"id": "C"}},
    {"data": {"id": "D"}},
    {"data": {"id": "e1", "source": "A", "target": "B"}},
    {"data": {"id": "e2", "source": "B", "target": "C"}},
    {"data": {"id": "e3", "source": "C", "target": "A"}},
    {"data": {"id": "e4", "source": "D", "target": "B"}}
  ]
}
```

### Code to Generate This

If you have a graph in a different format and want to convert it to JSON, you might write a script. Here's a simple Python example to create the JSON from basic graph definitions:

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
        graph_json = {"nodes": self.nodes, "edges": self.edges}
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

This example creates a simple directed graph and converts it into a JSON string. Adjustments would be needed based on the specifics of your graph data.

## Segment 75

Kerberos v5 Dialogue

## Segment 75

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

A common way to represent a graph in JSON is to specify nodes and edges as separate lists or objects. Here is one such representation:

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

Or, if you want to emphasize the directed nature more explicitly and potentially add edge labels or other properties:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"from": "A", "to": "B", "directed": true},
    {"from": "B", "to": "C", "directed": true},
    {"from": "C", "to": "A", "directed": true},
    {"from": "D", "to": "B", "directed": true}
  ]
}
```

### Directionality

- In both representations, the directionality of edges is implied by the order of `source` and `target` (or `from` and `to`) fields in the edge definitions. 
- An edge from A to B is represented as `{"source": "A", "target": "B"}` (or `{"from": "A", "to": "B"}`), indicating a directed edge.

### Code to Generate This JSON

If you were to generate this JSON programmatically, you might do something like this in Python:

```python
def create_graph(nodes, edges):
    graph = {
        "nodes": [{"id": node} for node in nodes],
        "edges": [{"source": edge[0], "target": edge[1]} for edge in edges]
    }
    return graph

# Define the graph
nodes = ['A', 'B', 'C', 'D']
edges = [('A', 'B'), ('B', 'C'), ('C', 'A'), ('D', 'B')]

# Generate and print the graph
graph_json = create_graph(nodes, edges)
import json
print(json.dumps(graph_json, indent=2))
```

This Python snippet creates a simple directed graph from given nodes and edges and prints its JSON representation.

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

## Segment 77

### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Segment 78

Identity Federation

## Segment 78

### Slide Image
There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

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
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

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
There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

## Segment 91

### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Segment 91

### Slide Image
There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

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
[LLM_ERROR] All providers failed: Gemini (timed out), Azure, Groq (Error code: 429 - {'error': {'message': 'Rate limit reached for model `meta-llama/llama-4-scout-17b-16e-instruct` in organization `org_01kkedd9pnejqr8cfvvrfp64h7` service tier `on_demand` on requests per minute (RPM): Limit 30, Used 30, Requested 1. Please try again in 2s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'requests', 'code': 'rate_limit_exceeded'}}).

## Segment 96

### Slide Image
[LLM_ERROR] All providers failed: Gemini (timed out), Azure, Groq (Error code: 429 - {'error': {'message': 'Rate limit reached for model `meta-llama/llama-4-scout-17b-16e-instruct` in organization `org_01kkedd9pnejqr8cfvvrfp64h7` service tier `on_demand` on requests per minute (RPM): Limit 30, Used 30, Requested 1. Please try again in 2s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'requests', 'code': 'rate_limit_exceeded'}}).

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
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Segment 98

### Slide Image
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. The graph will have directionality, meaning the edges have a direction from one node to another.

### Example Graph

Suppose we have a graph with the following properties:

- **Nodes (Labels):** A, B, C, D
- **Edges (List with Directionality):** 
  - A -> B
  - B -> C
  - C -> A
  - D -> B

### JSON Representation

The JSON representation of this graph can be structured as follows:

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

- **Nodes:** Each node is represented by an object with an `id` property that corresponds to its label.
- **Edges:** Each edge is represented by an object with `from` and `to` properties, indicating the direction of the edge.

### Code to Generate This JSON

If you were to generate this JSON programmatically, you could do something like the following in Python:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, from_node, to_node):
        self.edges.append({"from": from_node, "to": to_node})

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

# Usage
graph = Graph()
graph.add_node("A")
graph.add_node("B")
graph.add_node("C")
graph.add_node("D")

graph.add_edge("A", "B")
graph.add_edge("B", "C")
graph.add_edge("C", "A")
graph.add_edge("D", "B")

print(graph.to_json())
```

This Python code defines a simple `Graph` class, adds nodes and edges to it, and then converts the graph into a JSON string. The output would match the JSON example provided above.

## Segment 98

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

However, for a more detailed and structured representation that includes directionality explicitly in the graph definition, you might see variations. For instance, if an edge's directionality isn't explicitly stated, it might be assumed to be undirected. 

### Alternative Representation with Directionality

If you want to explicitly highlight directionality (directed vs. undirected) and possibly add more details like edge weights or labels, you could structure the JSON like this:

```json
{
  "graphType": "directed", // or "undirected"
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"source": "A", "target": "B"},
    {"source": "B", "target": "C"},
    {"source": "C", "target": "A"},
    {"source": "D", "target": "B"}
  ]
}
```

Or, with additional properties like edge labels and weights:

```json
{
  "graphType": "directed",
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"source": "A", "target": "B", "label": "E1", "weight": 1.0},
    {"source": "B", "target": "C", "label": "E2", "weight": 2.0},
    {"source": "C", "target": "A", "label": "E3", "weight": 3.0},
    {"source": "D", "target": "B", "label": "E4", "weight": 4.0}
  ]
}
```

### Code to Generate This JSON

If you're working in Python, here's a simple way to construct and output such a graph representation:

```python
import json

class Graph:
    def __init__(self, directed=False):
        self.nodes = []
        self.edges = []
        self.directed = directed

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, source, target, label=None, weight=None):
        edge = {"source": source, "target": target}
        if label:
            edge["label"] = label
        if weight:
            edge["weight"] = weight
        self.edges.append(edge)

    def to_json(self):
        graph_repr = {
            "graphType": "directed" if self.directed else "undirected",
            "nodes": self.nodes,
            "edges": self.edges
        }
        return json.dumps(graph_repr, indent=2)

# Usage
g = Graph(directed=True)
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

This example constructs a directed graph and outputs its JSON representation. Adjustments can be made based on specific requirements or programming languages.

## Segment 98

### Slide Image
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. The graph will have directionality, meaning the edges have a direction from one node to another.

### Example Graph

Suppose we have a graph with the following properties:

- **Nodes (Labels):** A, B, C, D
- **Edges (List with Directionality):** 
  - A -> B
  - B -> C
  - C -> A
  - D -> B

### Structured Graph Representation in JSON

Here's how we can represent this graph in a structured JSON format:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"source": "A", "target": "B"},
    {"source": "B", "target": "C"},
    {"source": "C", "target": "A"},
    {"source": "D", "target": "B"}
  ],
  "graphProperties": {
    "directed": true
  }
}
```

### Explanation

- **nodes**: This section lists all the unique node labels in the graph. Each node is represented by an object with an `id` property that corresponds to its label.
- **edges**: This section lists all the edges in the graph. Each edge is represented by an object with `source` and `target` properties, indicating the direction of the edge. For example, the edge `{ "source": "A", "target": "B" }` represents a directed edge from node A to node B.
- **graphProperties**: This section provides additional properties about the graph. In this case, it indicates that the graph is directed (`"directed": true`).

### Code to Generate This JSON

If you're working in a programming environment and want to dynamically create this JSON from your graph data, you might do something like this in Python:

```python
import json

class Graph:
    def __init__(self, directed=False):
        self.nodes = []
        self.edges = []
        self.directed = directed

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target})

    def to_json(self):
        graph_json = {
            "nodes": self.nodes,
            "edges": self.edges,
            "graphProperties": {"directed": self.directed}
        }
        return json.dumps(graph_json, indent=2)

# Usage
graph = Graph(directed=True)
graph.add_node("A")
graph.add_node("B")
graph.add_node("C")
graph.add_node("D")

graph.add_edge("A", "B")
graph.add_edge("B", "C")
graph.add_edge("C", "A")
graph.add_edge("D", "B")

print(graph.to_json())
```

This Python code defines a simple `Graph` class and uses it to create the example graph, then converts it to a JSON string.

## Segment 98

### Slide Image
To accomplish the task of extracting surrounding explanatory text separately from formula text and returning formulas in LaTeX, we'll need to follow a step-by-step approach. This process typically involves:

1. **Input Preparation**: Preparing the input text that contains both explanatory text and formula text.
2. **Formula Identification**: Identifying the parts of the text that are formulas. This can be complex and might require regular expressions or more sophisticated Natural Language Processing (NLP) techniques, depending on the format of the input.
3. **LaTeX Conversion**: Converting the identified formula text into LaTeX format.
4. **Text Separation**: Separating the explanatory text from the formula text.

Let's consider a hypothetical example to illustrate this process. Suppose we have a string that contains explanatory text along with a formula:

`"The equation for the area of a circle is \(A = \pi r^2\), which is a fundamental concept in geometry."`

### Step 1 & 2: Input Preparation and Formula Identification

For simplicity, let's assume formulas are enclosed in specific markers like `\(formula)\)`. In real-world scenarios, you might need to use more complex methods to identify formulas.

### Step 3: LaTeX Conversion

If the formula is already in a LaTeX-like format or easily convertible, we just ensure it's properly formatted. The example formula \(A = \pi r^2\) is already LaTeX-compatible.

### Step 4: Text Separation

Here's a simple Python script to illustrate how you could achieve this:

```python
import re

def separate_text_and_formula(text):
    # Assuming formulas are enclosed in \( and \)
    pattern = r'\([^)]+\)'
    formulas = re.findall(pattern, text)
    cleaned_text = re.sub(pattern, '', text)

    # Convert found formulas to LaTeX (if not already)
    latex_formulas = [f'${formula[1:-1]}$' for formula in formulas]

    return cleaned_text.strip(), latex_formulas

# Example usage
text = "The equation for the area of a circle is \(A = \pi r^2\), which is a fundamental concept in geometry."
explanatory_text, latex_formulas = separate_text_and_formula(text)

print("Explanatory Text:")
print(explanatory_text)
print("\nLaTeX Formulas:")
for i, formula in enumerate(latex_formulas):
    print(f"Formula {i+1}: {formula}")
```

This script performs the following:

- **Identifies** potential formulas enclosed in \( and \).
- **Extracts** these formulas.
- **Converts** them into a LaTeX format (in this case, just wraps them in `$` symbols, assuming a simple conversion; real conversion might require a more sophisticated approach).
- **Separates** the explanatory text from the formulas.

**Output:**

```
Explanatory Text:
The equation for the area of a circle is , which is a fundamental concept in geometry.

LaTeX Formulas:
Formula 1: $A = \pi r^2$
```

This example provides a basic approach. Real-world text can be much more complex, requiring advanced NLP techniques for accurate identification and conversion of mathematical expressions.

## Segment 98

### Slide Image
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. The graph will have directionality, meaning the edges have a direction from one node to another.

Let's say we have a graph with the following properties:

- **Node Labels**: A, B, C, D
- **Edge List**: (A, B), (B, C), (C, D), (D, A), (A, C)
- **Directionality**: The graph is directed.

Here's how we can represent this in a structured JSON format:

```json
{
  "graph": {
    "directed": true,
    "nodes": [
      {"id": "A"},
      {"id": "B"},
      {"id": "C"},
      {"id": "D"}
    ],
    "edges": [
      {"from": "A", "to": "B"},
      {"from": "B", "to": "C"},
      {"from": "C", "to": "D"},
      {"from": "D", "to": "A"},
      {"from": "A", "to": "C"}
    ]
  }
}
```

In this JSON representation:
- The `directed` property indicates that the graph is directed.
- The `nodes` list contains objects representing each node, identified solely by their `id` in this simple example.
- The `edges` list contains objects representing each edge, with `from` and `to` properties indicating the direction of the edge.

If you were to extract this information from a specific data source (like a database, a file, or another data structure), you would replace the static definitions of `nodes` and `edges` with dynamically extracted data.

### Example in Python

If you're working in Python and want to create such a graph from scratch, then convert it into the JSON format, you could do something like this:

```python
import json

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.nodes = []
        self.edges = []

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, from_node, to_node):
        self.edges.append({"from": from_node, "to": to_node})

    def to_json(self):
        graph_repr = {
            "graph": {
                "directed": self.directed,
                "nodes": self.nodes,
                "edges": self.edges
            }
        }
        return json.dumps(graph_repr, indent=2)

# Usage
g = Graph(directed=True)
g.add_node("A")
g.add_node("B")
g.add_node("C")
g.add_node("D")

g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("C", "D")
g.add_edge("D", "A")
g.add_edge("A", "C")

print(g.to_json())
```

This Python code defines a simple `Graph` class, adds nodes and edges to it, and then outputs the graph's representation in JSON format.

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

A common JSON representation for a graph might involve specifying nodes and edges as separate lists. For edges, we can specify the source node, target node, and optionally, the directionality (though in a directed graph, all edges are by definition directed).

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"source": "A", "target": "B"},
    {"source": "B", "target": "C"},
    {"source": "C", "target": "A"},
    {"source": "D", "target": "B"}
  ],
  "directed": true
}
```

### Explanation

- **nodes**: A list of node objects, each identified by an `id`.
- **edges**: A list of edge objects, each with a `source` and a `target`, indicating a directed edge from the source node to the target node.
- **directed**: A boolean indicating whether the graph is directed. In our case, it's `true`.

### Code to Generate This JSON

If you were to generate this in Python, for example, you could do something like:

```python
class Node:
    def __init__(self, id):
        self.id = id

class Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target

class Graph:
    def __init__(self, directed=True):
        self.nodes = []
        self.edges = []
        self.directed = directed

    def add_node(self, node):
        self.nodes.append({"id": node.id})

    def add_edge(self, edge):
        self.edges.append({"source": edge.source, "target": edge.target})

    def to_json(self):
        graph_repr = {
            "nodes": self.nodes,
            "edges": self.edges,
            "directed": self.directed
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

This Python code defines simple classes for `Node`, `Edge`, and `Graph`, and then constructs a graph with the specified nodes and edges, finally outputting the graph's JSON representation.

## Segment 100

### Slide Image
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. The graph will have directionality, meaning the edges have a direction from one node to another.

### Example Graph

Suppose we have a graph with the following properties:

- **Nodes (Labels):** A, B, C, D
- **Edges (List with Directionality):** 
  - A -> B
  - B -> C
  - C -> A
  - D -> B

### Structured Graph Representation in JSON

Here's how you could represent this graph in JSON, including node labels, an edge list, and directionality:

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

- **Nodes:** Each node is represented by a unique identifier (`id`). In a more complex scenario, nodes could also have properties (or attributes) like labels, colors, sizes, etc., but for simplicity, we've only included an `id`.
- **Edges:** Each edge is defined by a `from` node and a `to` node, which clearly represents the directionality of the edge.

### Python Code to Generate This JSON

If you want to create this JSON programmatically, you could use Python with its built-in `json` module:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, from_node, to_node):
        self.edges.append({"from": from_node, "to": to_node})

    def to_json(self):
        return json.dumps(self, indent=2, default=lambda o: o.__dict__)

# Usage
graph = Graph()
graph.add_node("A")
graph.add_node("B")
graph.add_node("C")
graph.add_node("D")

graph.add_edge("A", "B")
graph.add_edge("B", "C")
graph.add_edge("C", "A")
graph.add_edge("D", "B")

print(graph.to_json())
```

This Python code defines a simple `Graph` class, adds nodes and edges to it, and then converts the graph into a JSON string. The result is the same JSON structure shown above.

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

However, a more compact and commonly used format for graph representation, especially in graph databases and algorithms libraries (like Neo4j, NetworkX), would be to imply directionality through the structure and use an adjacency list or a simple nodes and edges list:

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

Or, for an even more compact form that directly implies edges are directional from source to target:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [["A", "B"], ["A", "C"], ["B", "D"], ["C", "E"], ["D", "E"], ["E", "B"]]
}
```

### Directionality Note

- In these representations, edges are considered directional, meaning an edge from A to B does not imply the existence of an edge from B to A.
- The absence of an edge in the list does not necessarily imply a lack of connection; it simply means there's no directed edge in that specified direction.

### Code to Generate This

If you're working with Python and want to create such a graph representation programmatically:

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

# Example usage
graph = Graph()
for char in 'ABCDE':
    graph.add_node(char)

edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), ("D", "E"), ("E", "B")]
for edge in edges:
    graph.add_edge(*edge)

print(graph.to_json())
```

This Python snippet creates a simple graph, adds nodes and edges, and then dumps it into a JSON string.

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
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.
