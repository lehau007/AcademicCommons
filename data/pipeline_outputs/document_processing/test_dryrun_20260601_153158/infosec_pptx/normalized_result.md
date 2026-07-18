Identity Authentication
With extra material for further reading, indicated by symbol *

Info-Sec 2023
2
Authentication
Basics
Passwords
Challenge-Response
Biometrics
Location
Multiple Methods

## Info-Sec 2023
### 3 Basics

### Authentication
Authentication is the binding of identity to a subject. 
Identity refers to that of an external entity (e.g., my identity, Van, etc.), 
while a subject is a computer entity (e.g., a process, etc.).

### Note
Message authentication is a different topic and has already been mentioned in the applications of hash functions.

### Establishing Identity

Establishing identity can be achieved through one or more of the following methods:

- **What entity knows**: For example, a password.
- **What entity has**: For example, an identity card, smart card.
- **What entity is**: For example, fingerprints, retinal characteristics.
- **Where entity is**: For example, in front of a particular terminal.

### Info-Sec 2023
#### Authentication System

We need a formal definition, rather an abstract view, of an Authentication System (AS) as a 5-tuple:

* A – a set: information that proves identity
* C – a set: information stored on computer and used to validate authentication information
* F: a set of complementation functions; *f : A → C*, to compute complement information from identity information
* L: authentication functions that prove identity
* S: functions enabling entity to create, alter information in A or C

Info-Sec 2023
6
Example
Password system, with passwords stored on line in clear text
A set of strings making up passwords
C = A
F singleton set of identity function { I }
L single equality test function { eq }
S function to set/change password

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

## Info-Sec 2023
### 9. Example: Unix

By definition, a 5-tuple (A, C, F, L, S)

* A – a set: information that proves identity
  * A = { strings of 8 chars or less }
* C – a set: information stored on computer and used to validate authentication information
  * C = {hash values of password}
* F: a set of complementation functions; f : A → C
  * F = { versions of modified DES }
* L: authentication functions that prove identity
  * L = { login, su, … }
* S: functions enabling entity to create, alter information in A or C
  * S = { passwd, nispasswd, passwd+, … }

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

Info-Sec 2023
11
Attacking passwords
Goal: find a ∈ A such that:
For some f ∈ F, f(a) = c ∈ C 
c is associated with entity
Two ways to determine whether a meets these requirements:
By trying computing f(a) for a set of a values until succeed
By trying calling I(a) until succeed (I(a) returns true)

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

## Info-Sec 2023
### 13 Dictionary Attacks

Dictionary attacks involve trial-and-error attempts using a list of potential passwords.

There are two types of dictionary attacks:

* **Off-line dictionary attacks**: The attacker knows the functions `f` and `c's`, and repeatedly tries different guesses `g ∈ A` until the list is exhausted or the passwords are guessed. Examples of off-line dictionary attack tools include `crack` and `john-the-ripper`.
* **On-line dictionary attacks**: The attacker has access to functions in `L` and tries guesses `g` until some `l(g)` succeeds. An example of an on-line dictionary attack is trying to log in by guessing a password.

Info-Sec 2023
14
Success probability over a time period
Anderson’s formula:
P probability of guessing a password in specified period of time
G number of guesses tested in 1 time unit
T number of time units
N number of possible passwords (|A|)
Then P ≥ TG/N

## Info-Sec 2023
### Example

#### Goal
Passwords are drawn from a 96-char alphabet. The system can test $10^4$ guesses per second. The goal is to achieve a probability of success of 0.5 over a 365-day period. 

#### Solution
To find the minimum password length, we calculate:
$N \geq \frac{TG}{P} = \frac{(365 \times 24 \times 60 \times 60) \times 10^4}{0.5} = 6.31 \times 10^{11}$

We choose $s$ such that 
$\sum_{j=0}^{s} 96^j \geq N$

Therefore, $s \geq 6$, meaning passwords must be at least 6 characters long.

Exercise
X = number defined by last 2 digits of your student ID; Y = X mod 4
Assume that H is a cryptographic hash function with output size (Y+2)*16 bits. Assume that Scorpion-i (i=1-9) is a specifically designed line of hardware chips for computing H, where Scorpion-i can create 10i * 1000 hash values a second (e.g. Scorpion-2 can do 100,000 hashes/sec). This product line is the best, fastest and affordable, in the market, priced at ii/2 *$1000 (e.g $2000 for i=2, $16000 for i=4). 

An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size N=(X mod 50)+ 40. Using H, this system maintains the hash values of the passwords of all the users. An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user. Using the Scorpion chips, how much the enemy has to spend in order to finish within a month with success probability (6+Y)*10%?
16

## Info-Sec 2023
### 17. On Password Selection

### Random Selection
Any password from A equally likely to be selected.

### Pronounceable Passwords
User selection of passwords.

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

## Info-Sec 2023
### 19 - User Selection

## Problem
People pick easy-to-guess passwords based on:
- Account names
- User names
- Computer names
- Place names

Common password choices include:
- Dictionary words 
  - Reversed
  - Odd capitalizations
  - Control characters
  - “Elite-speak”
  - Conjugations or declensions
  - Swear words
  - Torah/Bible/Koran/… words

Weak passwords also include:
- Too short
- Digits only
- Letters only

Examples of easily guessable passwords:
- License plates
- Acronyms
- Social security numbers
- Personal characteristics or foibles 
  - Pet names
  - Nicknames
  - Job characteristics 
  - etc.

## Info-Sec 2023
### Picking Good Passwords

* “LlMm*2^Ap”
* Names of members of 2 families: “OoHeO/FSK”
* Second letter of each word of length 4 or more in third line of third verse of Star-Spangled Banner, followed by “/”, followed by author’s initials: 
* What’s good here may be bad there: “DMC/MHmh” bad at Dartmouth (“Dartmouth Medical Center/Mary Hitchcock memorial hospital”), ok here

## Why are these now bad passwords? ☹

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

## Info-Sec 2023
### 22 - Salting

The goal of salting is to slow dictionary attacks. The method involves perturbing the hash function so that:

* A parameter controls which hash function is used.
* The parameter differs for each password.

Therefore, given $n$ password hashes and $n$ salts, it is necessary to hash a guess $n$ times.

## Info-Sec 2023
### 23

### Examples

#### Vanilla UNIX method
Use DES to encipher a 0 message with a password as the key; iterate 25 times. 
Perturb the E table in DES in one of 4096 ways. 
A 12-bit salt flips entries 1–11 with entries 25–36.

#### Alternate methods
Use the salt as the first part of the input to a hash function.

## Info-Sec 2023
### 24

Unix actually is based on a standard hash function for UNIX systems. This function hashes a password into an 11-character string using one of 4096 hash functions.

### Authentication System Components

The authentication system consists of:
- **A**: strings of 8 characters or less
- **C**: 2-character hash id || 11-character hash
- **F**: 4096 versions of modified DES
- **L**: login, su, …
- **S**: passwd, nispasswd, passwd+, …

## Exercise

Assume that $H$ is a cryptographic hash function with output size $(Y+2)*16$ bits. Assume that Scorpion-$i$ ($i=1-9$) is a specifically designed line of hardware chips for computing $H$, where Scorpion-$i$ can create $10i * 1000$ hash values a second, priced at $i^2/2 *$1000.

### Problem 1

An authentication system requires its users to pick their passwords of length exactly 6 from an alphabet of size $N=(X \mod 50)+ 40$. Using $H$, this system maintains the hash values of the passwords of all the users. An enemy, who has gained access to this hashed password file, aims to launch an off-line attack to break the password of an important user. 

Using the Scorpion chips, how much the enemy has to spend in order to finish within a month with success probability $(6+Y)*10\%$?

### Problem 2

The owner decides to enhance the above password system by using salt so that the enemy will need to spend at least 10 times the above-mentioned amount of money to achieve the same goal. How many salt bits he/she needs to use to achieve this purpose? 

## Given Variables
- $N=(X \mod 50)+ 40$
- Password length: 6
- Output size of $H$: $(Y+2)*16$ bits
- Scorpion-$i$ performance: $10i * 1000$ hash values/second
- Scorpion-$i$ price: $i^2/2 *$1000
- Success probability: $(6+Y)*10\%$
- Timeframe: 1 month

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

## Part 2 — Access Control
### Salt with slow hash

Hash password with salt. Choose a random salt `s` and compute 
``` 
y = h(password, s) 
```
and store `(s, y)` in the password file.

Note that the salt `s` is not secret. This is analogous to an Initialization Vector (IV). 

Verifying a salted password is still easy, but it requires a lot more work for a hacker. 

### Why?

## Part 2 — Access Control
### Password Cracking: Case I 

Attack a specific password without using a dictionary, for example, the administrator's password. This requires trying 256/2 = 255 attempts on average, similar to an exhaustive key search.

Does salt help in this case?

## Part 2 — Access Control

### Password Cracking: Case II

#### Attack on a Specific Password with Dictionary

With salt:

* Expected work: $\frac{1}{4} (2^{19}) + \frac{3}{4} (2^{55}) \approx 2^{54.6}$
* In practice, try all passwords in dictionary… 
* …then work is at most $2^{20}$ and probability of success is $\frac{1}{4}$

#### Without Salt

* One-time work to compute dictionary: $2^{20}$
* Expected work is of the same order as above
* But with precomputed dictionary hashes, the “in practice” attack is essentially free…

## Part 2 — Access Control
### Password Cracking: Case III

Assume all $2^{10}$ passwords are distinct. Any of $2^{10}$ pwds in file, without dictionary.

Need $2^{55}$ comparisons before expecting to find a pwd.

#### Without Salt

If no salt is used, each computed hash yields $2^{10}$ comparisons. 
So the expected work (hashes) is $\frac{2^{55}}{2^{10}} = 2^{45}$.

#### With Salt

If salt is used, the expected work is $2^{55}$. 
Each comparison requires a hash computation.

## Part 2 — Access Control
### Password Cracking: Case IV

Any of 1024 passwords in a file, with dictionary. 
The probability of one or more passwords in the dictionary is $1 – (3/4)^{1024} ≈ 1$. 
So, we ignore the case where no password is in the dictionary.

If a salt is used, the expected work is less than $2^{22}$. 
See the book or slide notes for details. 
The work is approximately $\frac{\text{size of dictionary}}{P(\text{pwd in dictionary})}$.

What if no salt is used? 
If dictionary hashes are not precomputed, the work is about $\frac{2^{19}}{2^{10}} = 2^9$.

## Info-Sec 2023
### 32

## Guessing Through L
Cannot prevent these attacks completely. 
Otherwise, legitimate users cannot log in.

## Mitigation Strategies
Make authentication attempts slow:
- Backoff
- Disconnection
- Disabling

### Important Consideration
Be very careful with administrative accounts!

## Alternative Approach
Consider jailing:
- Allow login, but restrict activities.

## Info-Sec 2023
### 33 Password Aging

Force users to change passwords after some time has expired. 

To prevent password re-use:
- Record previous passwords
- Block changes for a period of time
- Give users time to think of good passwords
- Don’t force them to change before they can log in
- Warn them of expiration days in advance

## Info-Sec 2023
### 34

## Challenge-Response

User and system share a secret function *f* (in practice, *f* is a known function with unknown parameters, such as a cryptographic key).

The challenge-response process is as follows:

- User requests to authenticate
- System sends a random message *r* (the challenge)
- User sends *f(r)* (the response) back to the system. 

This can be represented as:

User → System: request to authenticate
System → User: random message *r* (the challenge)
User → System: *f(r)* (the response)

## Info-Sec 2023
## 35
## Pass Algorithms

Challenge-response with the function f itself a secret. 
The challenge is a random string of characters. 
The response is some function of that string. 
Usually used in conjunction with a fixed, reusable password. 

No visual element provided.

## Info-Sec 2023
### One-Time Passwords

One-Time Passwords are passwords that can be used exactly once. After use, they are immediately invalidated.

The mechanism works as a challenge-response system:
- **Challenge**: The number of authentications
- **Response**: The password for that particular number

### Problems

The implementation of One-Time Passwords faces several challenges:
- **Synchronization**: Ensuring synchronization between the user and the system.
- **Generation**: Generation of good random passwords.
- **Distribution**: The password distribution problem.

### Info-Sec 2023
#### 37. S/Key

S/Key is a one-time password scheme based on the idea of Lamport. It uses a one-way hash function, such as MD5 or SHA-1.

The process works as follows:

- The user chooses an initial seed *k*.
- The system calculates a series of hashes:
  - *h(k) = k1*
  - *h(k1) = k2*
  - *…*
  - *h(kn–1) = kn*

The passwords are generated in reverse order:
- *p1 = kn*
- *p2 = kn–1*
- *…*
- *pn–1 = k2*
- *pn = k1*

## Info-Sec 2023
### 38

## S/Key Protocol

The system stores the maximum number of authentications `n`, the number of the next authentication `i`, and the last correctly supplied password `pi–1`.

The system computes `h(pi) = h(kn–i+1) = kn–i+2 = pi–1`. If there is a match with what is stored, the system replaces `pi–1` with `pi` and increments `i`.

## Info-Sec 2023
### 39 - C-R and Dictionary Attacks

C-R and dictionary attacks are similar to those used for fixed passwords. 

An attacker knows the challenge $r$ and the response $f(r)$. If $f$ is an encryption function, the attacker can try different keys. 

The attacker may only need to know the form of the response. They can determine if their guess is correct by checking if the deciphered object is of the right form.

### Example: Kerberos Version 4

Kerberos Version 4 used DES, but the keys had only 20 bits of randomness. As a result, attackers at Purdue were able to guess the keys quickly. They did this by checking if the deciphered tickets had a fixed set of bits in specific locations.

Info-Sec 2023
40
Encrypted Key Exchange *
Defeats off-line dictionary attacks
Idea: random challenges enciphered, so attacker cannot verify correct decipherment of challenge
Assume Alice, Bob share secret password s
In what follows, Alice needs to generate a random public key p and a corresponding private key q
Also, k is a randomly generated session key, and RA and RB are random challenges

## Info-Sec 2023
### 41

## EKE Protocol

Now Alice and Bob share a randomly generated secret session key $k$.

## Part 2 — Access Control
### Something You Have

Something in your possession. Examples include:
- Car key
- Laptop computer (or MAC address)
- Password generator
- ATM card, smartcard, etc.

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

## Memory Card

A memory card is used to store but not process data. Examples include:

* Magnetic stripe card (e.g., bank card)
* Electronic memory card

Memory cards are used alone for physical access (e.g., hotel rooms) or with a password/PIN (e.g., ATMs).

### Drawbacks of Memory Cards

The drawbacks of memory cards include:
* Need special reader
* Loss of token issues
* User dissatisfaction (acceptable for ATM, not for computer access)

Smartcard
credit-card like 
has own processor, memory, I/O ports
ROM, EEPROM, RAM memory
executes protocol to authenticate with reader/computer
static: similar to memory cards
dynamic: passwords created every minute; entered manually by user or electronically
challenge-response: computer creates a random number; smart card provides its hash (similar to PK)
also have USB dongles


### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.


## Electronic Identity Cards

An important application of smart cards is a national e-identity (eID), which serves the same purpose as other national ID cards (e.g., a driver’s licence). However, an eID can provide stronger proof of identity.

### Example: German Card

A German eID card contains:
- Personal data
- Document number
- Card access number (six-digit random number)
- Machine-readable zone (MRZ): the password

### Uses

The card supports multiple uses:
- ePass (government use)
- eID (general use)
- eSign (can have private key and certificate)

## User Authentication with eID
No text to normalize. Please provide the text to be normalized. 

(If you provide the text, I can assist you further.)

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

## Part 2 — Access Control
### Why Biometrics?

Biometrics may be better than passwords. However, cheap and reliable biometrics are needed. Today, biometrics is an active area of research. 

Biometrics are used in security today, for example:
* Thumbprint mouse
* Palm print for secure entry
* Fingerprint to unlock car doors, etc.

However, biometrics has not really become popular and has not lived up to its promise/hype (yet?).

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

## Part 2 — Access Control
### Fingerprint: Enrollment

The process involves the following steps:
- Capture image of fingerprint
- Enhance image
- Identify “points”

## Part 2 — Access Control
### Fingerprint: Recognition

Extracted points are compared with information stored in a database. The question arises: Is it a statistical match?

#### Aside: Identical Twins' Fingerprints

Do identical twins' fingerprints differ?

### Info-Sec 2023
#### 53

## Other Characteristics

Several other characteristics can be used for identification. These include:

- **Eyes**: The patterns in irises are unique. Identification involves measuring these patterns and determining if the differences between them are random or correlating images using statistical tests.

- **Faces**: This can involve analyzing the image as a whole or specific characteristics, such as the distance from the nose to the chin. However, factors like lighting, the view of the face, and other noise can hinder this method.

- **Keystroke Dynamics**: Believed to be unique to individuals, keystroke dynamics involve analyzing:
  - Keystroke intervals
  - Pressure
  - Duration of the stroke
  - Where the key is struck

Statistical tests are used to analyze these characteristics.

### Biometric Authentication Methods
Authenticate user based on one of their physical characteristics:
* Facial
* Fingerprint
* Hand geometry
* Retina pattern
* Iris
* Signature
* Voice

### Table Extraction and JSON Output
To accurately extract row labels, column labels, and cell values from a given table or matrix and return them in a structured JSON format, a sample table is required as input.

#### Example Table
| **Country** | **City** | **Population (in millions)** | **Area (in km²)** |
|-------------|----------|-----------------------------|------------------|
| France      | Paris    | 2.1                          | 1054             |
| Japan       | Tokyo    | 13.9                         | 1424             |
| Brazil      | São Paulo| 22.1                         | 1221             |

#### JSON Output
The structured JSON output based on this table can be represented in several formats.

##### Format 1
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

##### Format 2
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

##### Format 3
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

### Implementation Steps
For actual implementation:

1. **Read the table**: Depending on the source, use libraries like pandas in Python for data manipulation.
2. **Extract headers and data**: Use methods like `df.columns` for column labels and `df.values` or iteration for row values.
3. **Serialize to JSON**: Use JSON libraries (e.g., `json.dumps()` in Python) to convert your structured data into JSON format.

### Python Example
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

## Operation of a Biometric System

Verification is analogous to user login via a smart card and a PIN. Identification, on the other hand, involves providing biometric information without any IDs, and the system compares it with stored templates to identify the individual.

### No Visual Element Provided

There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

## Biometric Accuracy

The system generates a matching score (a number) that quantifies similarity between the input and the stored template. Concerns include sensor noise and detection inaccuracy, which can lead to problems of false matches and false non-matches.

* Further reading: Stallings textbook.

## Biometric Accuracy

The characteristic curve can be plotted with 2,000,000 comparisons. 
This allows picking a threshold that balances error rates.

No visual element was provided for analysis.

## Info-Sec 2023
### 58. Cautions

These can be fooled! It assumes the biometric device is accurate in the environment it is being used in. The transmission of data to the validator is tamperproof, correct.

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

## Info-Sec 2023
### 60
#### Location – Just a brief

If you know where a user is, you can validate their identity by verifying if the person is where the user claims to be. This method requires special-purpose hardware to locate the user. A GPS (Global Positioning System) device provides a location signature of an entity. The host uses an LSS (Location Signature Sensor) to obtain the signature for the entity.

# Info-Sec 2023
## 61
## Multiple Methods

Multiple authentication methods can be employed. For example, "where you are" requires an entity to have Location Services (LSS) and GPS, which also implies "what you have". Different methods can be assigned to different tasks.

As users perform more sensitive tasks, they must authenticate in more ways, presumably with increasing stringency. A file describes the required authentication. This includes:

* Controls on access (e.g., time of day)
* Resource management
* Request to change passwords

## Pluggable Authentication Modules

### Info-Sec 2023
#### 62 - PAM

The idea behind PAM (Privileged Access Management) is that when a program needs to authenticate, it checks a central repository for methods to use. This is achieved through a library call: `pam_authenticate`.

The configuration for PAM is typically stored in files located in `/etc/pam.d/`, with the file name corresponding to the name of the program.

The authentication process involves modules that perform the actual authentication checking. These modules can be configured with the following control flags:

* **sufficient**: Succeed if the module succeeds.
* **required**: Fail if the module fails, but all required modules must be executed before reporting failure.
* **requisite**: Like required, but don't check all modules.
* **optional**: Invoke only if all previous modules fail.

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

## Extended Material: Kerberos Authentication Protocol

### Material Sources
- History and general information from Wiki
- Details on Kerberos versions 4 and 5 from Stallings Text and slides

### Info-Sec 2023
#### 65. Kerberos

Kerberos is a computer network authentication protocol which allows nodes communicating over a non-secure network to prove their identity to one another in a secure manner. It is aimed primarily at a client-server model, and it provides mutual authentication -- both the user and the server verify each other's identity. Messages are protected against eavesdropping and replay attacks. Kerberos builds on Symmetric Key Cryptography (SKC) and requires a trusted third party, and optionally may use public-key cryptography during certain phases of authentication.

## Sep 2009
## Information Security by Van K Nguyen, Hanoi University of Technology
## 66
## Kerberos

### History
Kerberos is named after the character Kerberos (or Cerberus), the ferocious three-headed guard dog of Hades (from Greek mythology). 
MIT developed Kerberos in 1988 to protect network services provided by Project Athena. The first version was primarily designed by Steve Miller and Clifford Neuman, based on the earlier Needham–Schroeder symmetric-key protocol. Versions 1-3 were experimental and internal.

Kerberos version 4, the first public version, was released on January 24, 1989. 
Neuman and John Kohl published version 5 in 1993, with the intention of overcoming existing limitations and security problems. 
Version 5 appeared as RFC 1510, which was then made obsolete by RFC 4120 in 2005. 
In 2005, the Internet Engineering Task Force (IETF) Kerberos working group updated the specifications.

## Information Security
### Sep 2009
### Van K Nguyen
### Hanoi University of Technology
### 67

## Idea

### Ticket
The issuer vouches for the identity of the requester of service.

### Key Distribution Center (KDC)
The KDC combines two servers: 
- Authentication Server (AS), also known as the Kerberos server
- Ticket Granting Server (TGS)

## Process

### User Authentication
1. User \( u \) authenticates to AS.
2. Obtains ticket \( T_{u,TGS} \) for ticket granting service (TGS).

### Service Request
1. User \( u \) wants to use service \( s \):
2. User sends authenticator \( A_u \), ticket \( T_{u,TGS} \) to TGS asking for ticket for service.
3. TGS sends ticket \( T_{u,s} \) to user.
4. User sends \( A_u, T_{u,s} \) to server as request to use \( s \).

## Kerberos v4 Overview

Kerberos v4 is a basic third-party authentication scheme. The scheme involves:

* An Authentication Server (AS) 
* A Ticket Granting Server (TGS)

The process works as follows:

* Users initially negotiate with the AS to identify themselves.
* The AS provides a non-corruptible authentication credential, known as a Ticket Granting Ticket (TGT).
* Users subsequently request access to other services from the TGS on the basis of the user's TGT.
* The protocol uses DES for encryption.

## Kerberos 4 Overview

No visual element provided.

# Kerberos v4 Dialogue

## Graph Representation
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

### Example Graph

* **Nodes**: A, B, C, D, E
* **Edges**: 
  * A → B
  * A → C
  * B → D
  * C → E
  * D → E
  * E → B

## JSON Representation

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

## Alternative Representations

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

### Adjacency List

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

## Extracting Node Labels, Edge Lists, and Directionality

To extract node labels, edge lists, and directionality from a graph (assuming it's already in a structured format), you would typically parse the JSON and access the respective fields. For example, in Python:

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

## Kerberos Version 5

Developed in the mid 1990's, Kerberos Version 5 was specified as Internet standard RFC 1510. It provides improvements over version 4, addressing environmental shortcomings, including:

* Encryption algorithm
* Network protocol
* Byte order
* Ticket lifetime
* Authentication forwarding
* Interrealm authentication

It also addresses technical deficiencies, such as:

* Double encryption
* Non-standard mode of use
* Session keys
* Password attacks

## Kerberos Realms

A Kerberos environment consists of:
- A Kerberos server
- A number of clients, all registered with the server
- Application servers, sharing keys with the server

This is termed a realm. Typically, a realm is a single administrative domain. If you have multiple realms, their Kerberos servers must share keys and trust each other.

## Kerberos Realms

No visual element provided.

# Protocol
[From Wiki]
## Client Authentication to the AS
## Client Service Authorization
## Client Service Request

## Representing a Graph in JSON
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges.

### Example Graph
Suppose we have a graph with the following properties:

* **Nodes (Vertices):** A, B, C, D
* **Edges:** 
  * A -> B (directed from A to B)
  * B -> C (directed from B to C)
  * C -> A (directed from C to A)
  * D -> B (directed from D to B)

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

# Kerberos v5 Dialogue

## Graph Representation in JSON

To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges.

### Example Graph

Suppose we have a graph with the following properties:

* **Nodes (Vertices):** A, B, C, D
* **Edges:** 
  * A -> B (directed from A to B)
  * B -> C (directed from B to C)
  * C -> A (directed from C to A)
  * D -> B (directed from D to B)

## JSON Representation

A common way to represent a graph in JSON is to specify nodes and edges as separate lists or objects. Here are two such representations:

### Simple Representation

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

### Explicit Directionality Representation

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

## Directionality

* In both representations, the directionality of edges is implied by the order of `source` and `target` (or `from` and `to`) fields in the edge definitions.
* An edge from A to B is represented as `{"source": "A", "target": "B"}` (or `{"from": "A", "to": "B"}`), indicating a directed edge.

## Code to Generate This JSON

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

## Federated Identity Management

The use of a common identity management scheme across multiple enterprises and numerous applications, supporting many thousands, even millions of users, involves several principal elements:

* Authentication
* Authorization
* Accounting
* Provisioning
* Workflow automation
* Delegated administration
* Password synchronization
* Self-service password reset
* Federation

Kerberos contains many of these elements.

## Identity Management

There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

## Identity Federation

There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

## Standards Used

The following standards are used:

* Security Assertion Markup Language (SAML): an XML-based language for the exchange of security information between online business partners. SAML is part of OASIS (Organization for the Advancement of Structured Information Standards) standards for federated identity management, which includes standards like WS-Federation for browser-based federation.

To enable interoperability, a few mature industry standards are required.

## Federated Identity Examples

No visual element provided.

### FIM vs. SSO

## Definitions

* **SSO**: Single Sign-On
  Allows users to access multiple web applications at once, using just one set of credentials. Beyond the workforce, companies can utilize SSO to help customers access various sections of one account.

## Relationship to FIM

As a tool, SSO fits within the broader model of FIM. The key difference between SSO and FIM is while SSO is designed to authenticate a single credential across various systems within one organization, federated identity management systems offer single access to a number of applications across various enterprises.

No change is needed for the provided text as it appears to be a simple header with a reference. However, to follow Markdown formatting guidelines, here is the text reformatted:


## Extended Material *Biometrics*
Slides borrowed from Mark Stamp’s web
https://www.cs.sjsu.edu/~stamp/infosec/powerpoint/

## Part 2 — Access Control

### Something You Are: Biometric

"You are your key" — Schneier. This concept revolves around the idea that a person's unique characteristics serve as their authentication key. These characteristics fall under three main categories:

- **Are**: Refers to biometric characteristics that are inherent to an individual.
- **Know**: Pertains to knowledge-based authentication, not a biometric method.
- **Have**: Relates to possession-based authentication, also not a biometric method.

### Biometric Examples

Biometric access control methods include:

- Fingerprint
- Handwritten signature
- Facial recognition
- Speech recognition
- Gait (walking) recognition
- "Digital doggie" (odor recognition)
- Many more!

## Part 2 — Access Control

### Ideal Biometric

The ideal biometric has several characteristics:
- **Universal**: applies to (almost) everyone. 
- **Distinguishing**: distinguish with certainty. 
- **Permanent**: physical characteristic being measured never changes.

However, in reality:
- No biometric applies to **everyone**.
- Cannot hope for **100% certainty**.
- It is acceptable if the biometric remains valid for a **long time**.

### Collectability

- **Collectable**: easy to collect required data.
  - Depends on whether subjects are **cooperative**.
  - Also, it should be **safe**, **user-friendly**, and ???

## Part 2 — Access Control
### Identification vs Authentication

Identification is the process of determining "Who goes there?" It involves comparing a given input to a large set of known identities, which is a one-to-many comparison. An example of identification is an FBI fingerprint database.

Authentication, on the other hand, verifies if a user "Are you who you say you are?" This process involves a one-to-one comparison, such as a thumbprint mouse.

The identification problem is more difficult because it involves more comparisons, leading to a higher chance of "random" matches. However, we are mostly interested in authentication.

## Part 2 — Access Control
### Enrollment vs Recognition

The enrollment phase involves putting a subject's biometric information into a database. During this phase, it is crucial to carefully measure the required information. It is acceptable if slow and repeated measurements are needed to ensure precision. However, this process may be a weak point in real-world use.

In contrast, the recognition phase, which involves biometric detection in practical use, requires quick and simple measurements. Nevertheless, it must still be reasonably accurate.

## Part 2 — Access Control

### Cooperative Subjects

We differentiate between authentication for cooperative subjects and identification for uncooperative subjects. 
For example, facial recognition is used in Las Vegas casinos to detect known cheaters, as well as for identifying terrorists in airports, etc. 
However, such systems often face less than ideal enrollment conditions. 
In contrast, when the subject is cooperative, it makes the recognition phase much easier. 
Since we are focused on authentication, we can assume that the subjects are cooperative.

## Part 2 — Access Control

### Biometric Errors

The relationship between fraud rate and insult rate can be described as follows:

* **Fraud**: Trudy mis-authenticated as Alice
* **Insult**: Alice not authenticated as Alice

For any biometric, decreasing one will increase the other. 

### Trade-off Between Fraud and Insult Rates

| Match Rate | Fraud Rate | Insult Rate |
| --- | --- | --- |
| 99% | Low | High |
| 30% | High | Low |

The **Equal Error Rate** is the rate at which **fraud == insult**, providing a way to compare different biometrics.

## Part 2 — Access Control

### Fingerprint History

The history of fingerprinting dates back to several key events:
- 1823: Professor Johannes Evangelist Purkinje discussed 9 fingerprint patterns.
- 1856: Sir William Hershel used fingerprints (in India) on contracts.
- 1880: Dr. Henry Faulds published an article in Nature about using fingerprints for identification.
- 1883: Mark Twain’s *Life on the Mississippi* featured a story where a murderer was identified by their fingerprint.

## Part 2 — Access Control
### Fingerprint History

In 1888, Sir Francis Galton developed a classification system. His system of “minutia” can be used today. It also verified that fingerprints do not change.

Some countries require a fixed number of “points” (minutia) to match in criminal cases. The requirements vary:
| Country | Minimum Points |
| --- | --- |
| Britain | 15 |
| US | No fixed number |

Part 2 ⎯ Access Control                                                                                                  91
Fingerprint Comparison
Loop (double)
Whorl
Arch
Examples of loops, whorls, and arches
Minutia extracted from these features


### Slide Image
There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.



### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.



### Slide Image
There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.


## Part 2 — Access Control
### Fingerprint: Enrollment

The process involves the following steps:
1. Capture image of fingerprint
2. Enhance image
3. Identify “points”

## Part 2 — Access Control

### Fingerprint Recognition

Extracted points are compared with information stored in a database. The question arises: Is it a statistical match?

#### Aside: Identical Twins' Fingerprints

Do identical twins' fingerprints differ?

## Part 2 — Access Control
### Hand Geometry

A popular biometric, hand geometry measures the shape of the hand, including:
- Width of hand
- Width of fingers
- Length of fingers, etc.

However, human hands are not so unique. Therefore, hand geometry is sufficient for many situations and okay for authentication, but not useful for identification (ID) problems.

## Part 2 — Access Control
### Hand Geometry

#### Advantages
* Quick — 1 minute for enrollment, 5 seconds for recognition
* Hands are symmetric — so what?

#### Disadvantages
* Cannot use on very young or very old
* Relatively high equal error rate

## Part 2 — Access Control
### Iris Patterns

Iris pattern development is “chaotic” with little or no genetic influence. Even for identical twins, the patterns are uncorrelated. The pattern is stable through lifetime.

## Part 2 — Access Control
### Iris Recognition: History

* 1936: suggested by an ophthalmologist
* 1980s: popularized in James Bond films
* 1986: first patent appeared
* 1994: John Daugman patents a new and improved technique

Patents owned by Iridian Technologies.

## Part 2 — Access Control

### Iris Scan

The iris scan process involves the following steps:
1. Scanner locates the iris.
2. Take a black and white photo.
3. Use polar coordinates.
4. Apply a 2-D wavelet transform.
5. Get a 256-byte iris code.

### Graph Representation in JSON

A simple example graph can be represented in JSON as follows:

#### Example Graph

Suppose we have a graph with the following properties:
- **Nodes (Labels):** A, B, C, D
- **Edges (List with Directionality):** 
  - A -> B
  - B -> C
  - C -> A
  - D -> B

#### JSON Representation

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

#### Explanation

*   **Nodes:** Each node is represented by an object with an `id` property that corresponds to its label.
*   **Edges:** Each edge is represented by an object with `from` and `to` properties, indicating the direction of the edge.

#### Code to Generate This JSON

Here's a simple way to construct and output such a graph representation in Python:

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
        graph_repr = {
            "nodes": self.nodes,
            "edges": self.edges
        }
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

### Separating Explanatory Text and Formulas

To separate explanatory text from formulas and return formulas in LaTeX, consider the following steps:

1.  **Input Preparation:** Prepare the input text containing both explanatory text and formula text.
2.  **Formula Identification:** Identify the parts of the text that are formulas using regular expressions or NLP techniques.
3.  **LaTeX Conversion:** Convert the identified formula text into LaTeX format.
4.  **Text Separation:** Separate the explanatory text from the formula text.

#### Example

Suppose we have a string containing explanatory text along with a formula:

`"The equation for the area of a circle is \(A = \pi r^2\), which is a fundamental concept in geometry."`

#### Python Script

Here's a simple Python script to illustrate how you could achieve this:

```python
import re

def separate_text_and_formula(text):
    pattern = r'\([^)]+\)'
    formulas = re.findall(pattern, text)
    cleaned_text = re.sub(pattern, '', text)

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

### Alternative Graph Representations

You can represent a graph in JSON with additional properties like edge labels and weights:

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

#### Python Code for Alternative Representation

Here's how you can create this JSON representation in Python:

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

## Part 2 — Access Control
### Measuring Iris Similarity

Iris similarity is based on Hamming distance, defined as:

d(x,y) = # of non-match bits / # of bits compared

Examples:
- d(0010,0101) = 3/4
- d(101111,101001) = 1/3

The Hamming distance is computed on a 2048-bit iris code. 
A perfect match is achieved when d(x,y) = 0. 
For the same iris, the expected distance is 0.08, while a random match is expected to have a distance of 0.50. 
An iris scan is accepted as a match if the distance is less than 0.32.

## Part 2 — Access Control

### Iris Scan Error Rate

* Distance
* Distance
* Fraud rate
* == Equal Error Rate

## Graph Representation in JSON

### Example Graph

Suppose we have a graph with the following properties:

* **Nodes (Vertices):** A, B, C, D
* **Edges:** 
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

* **nodes**: A list of node objects, each identified by an `id`.
* **edges**: A list of edge objects, each with a `source` and a `target`, indicating a directed edge from the source node to the target node.
* **directed**: A boolean indicating whether the graph is directed. In our case, it's `true`.

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

## Alternative Graph Representations

### Example Graph

Suppose we have a graph with the following properties:

* **Nodes (Labels):** A, B, C, D
* **Edges (List with Directionality):** 
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

* **Nodes:** Each node is represented by a unique identifier (`id`). 
* **Edges:** Each edge is defined by a `from` node and a `to` node, which clearly represents the directionality of the edge.

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

## More Complex Graph Representation

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

Or, for an even more compact form:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [["A", "B"], ["A", "C"], ["B", "D"], ["C", "E"], ["D", "E"], ["E", "B"]]
}
```

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

## Part 2 — Access Control
### Attack on Iris Scan

An attacker could use a photo of an eye to bypass an iris scan. A good photo of an eye can be scanned, and there are documented cases of this type of attack. For example, an Afghan woman was authenticated by iris scan using an old photo. The story can be found [here](link). To prevent this type of attack, a scanner could use light to verify that it is scanning a "live" iris.

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

## Part 2 — Access Control
### Biometrics: The Bottom Line

Biometrics are hard to forge. However, an attacker could:
- Steal Alice’s thumb
- Photocopy Bob’s fingerprint, eye, etc.
- Subvert software, database, “trusted path” …

And there's the issue of revoking a “broken” biometric. 
Biometrics are not foolproof. 
Biometric use is relatively limited today. 
That should change in the (near?) future.

## Thông Tin Bảo Mật
### Tổng Quan

Bảo mật thông tin là một phần quan trọng của an toàn thông tin. Nó liên quan đến việc bảo vệ thông tin khỏi các truy cập trái phép, sử dụng, tiết lộ, phá hủy, hoặc thay đổi.

## Các Khái Niệm Cơ Bản

* **An toàn thông tin**: Là việc bảo vệ thông tin khỏi các mối đe dọa và truy cập trái phép.
* **Bảo mật thông tin**: Là một phần của an toàn thông tin, tập trung vào việc bảo vệ thông tin khỏi các truy cập trái phép.

## Các Loại Hình Tấn Công

* **Tấn công thụ động**: Là loại tấn công mà kẻ tấn công chỉ quan sát và thu thập thông tin mà không can thiệp vào hệ thống.
* **Tấn công chủ động**: Là loại tấn công mà kẻ tấn công can thiệp vào hệ thống và thực hiện các hành động để phá hủy hoặc thay đổi thông tin.

## Mô Hình Bảo Mật

### Mô Hình CIA

| Thành Phần | Chức Năng |
| --- | --- |
| **Confidentiality** (Bảo mật) | Đảm bảo thông tin chỉ được truy cập bởi những người được phép. |
| **Integrity** (Toàn vẹn) | Đảm bảo thông tin không bị thay đổi hoặc phá hủy trái phép. |
| **Availability** (Sẵn sàng) | Đảm bảo thông tin luôn sẵn sàng và có thể truy cập khi cần. |

## Các Công Cụ và Kỹ Thuật Bảo Mật

* **Mật mã hóa**: Là quá trình chuyển đổi thông tin thành dạng không thể đọc được mà không có khóa giải mã.
* **Chữ ký số**: Là một kỹ thuật sử dụng mật mã hóa để đảm bảo tính toàn vẹn và xác thực của thông tin.

## Các Vấn Đề Bảo Mật

* **Malware**: Là các chương trình độc hại được thiết kế để gây hại cho hệ thống hoặc đánh cắp thông tin.
* **Phishing**: Là loại tấn công mà kẻ tấn công giả mạo thông tin để đánh cắp thông tin cá nhân.

## Công Thức và Phương Trình

Không có công thức hoặc phương trình cụ thể trong tài liệu này.

## Bảng và Biểu Đồ

Không có bảng hoặc biểu đồ cụ thể trong tài liệu này ngoài bảng trong mô hình CIA.