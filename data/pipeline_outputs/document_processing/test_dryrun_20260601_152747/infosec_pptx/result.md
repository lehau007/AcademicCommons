## Identity Authentication
### With extra material for further reading, indicated by symbol *

<!-- No content to normalize, awaiting subsequent text segments -->

## Info-Sec 2023
### 2. Authentication Basics
#### Methods
- Passwords
- Challenge-Response
- Biometrics
- Location
- Multiple Methods

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

We need a formal definition, rather abstract view, of an Authentication System (AS) as a 5-tuple:

* A – a set: information that proves identity
* C – a set: information stored on computer and used to validate authentication information
* F: a set of complementation functions; *f : A → C*, to compute complement information from identity information
* L: authentication functions that prove identity
* S: functions enabling entity to create, alter information in *A* or *C*

## Info-Sec 2023
### 6. Example: Password System

### Overview
The example describes a password system with passwords stored online in clear text.

### Components
- **A**: A set of strings making up passwords.
- **C**: Equal to **A**.
- **F**: A singleton set of the identity function { **I** }.
- **L**: A single equality test function { **eq** }.
- **S**: A function to set/change a password.

## Info-Sec 2023
### 7. Passwords

A password is a sequence of characters. Examples include:

* 10 digits
* A string of letters

Passwords can be generated in various ways:
* Randomly
* By a user
* By a computer with user input

Alternatively, a password can be a sequence of words, such as pass-phrases.

There are also different types of password algorithms, including:
* Challenge-response
* One-time passwords

## Info-Sec 2023
### 8. Storage

### Storing Passwords Securely

Storing passwords as cleartext poses a significant risk. 
If the password file is compromised, all passwords are revealed.

A better approach is to encipher the file. 
However, this requires having both decipherment and encipherment keys in memory. 
This reduces to the previous problem, as the keys are vulnerable.

### One-Way Hash Solution

A solution to this problem is to store a one-way hash of the password instead. 
If an attacker obtains the file, they must still guess the passwords or invert the hash values.

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

## Info-Sec 2023
### 10
### Example: Unix

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

## Info-Sec 2023
### 11 - Attacking Passwords

The goal is to find a value $a$ in set $A$ such that:

For some function $f$ in set $F$, $f(a) = c$ in set $C$, 
where $c$ is associated with an entity.

There are two ways to determine whether $a$ meets these requirements:

* By trying to compute $f(a)$ for a set of $a$ values until successful
* By trying to call $I(a)$ until successful (i.e., $I(a)$ returns `true`)

## Info-Sec 2023
### 12. Preventing Attacks

To prevent attacks, consider the following measures:

* Hide at least one of $a$, $f$, or $c$. This prevents an obvious attack from above, as seen in the example of UNIX/Linux shadow password files, which hides the $c$'s.
* Block access to all $l \in L$ or the result of $l(a)$. This prevents an attacker from knowing if a guess succeeded. Examples include:
  + Preventing any logins to an account from a network.
  + Preventing knowledge of the results of $l$ (or accessing $l$).

## Info-Sec 2023
### 13 Dictionary Attacks

Dictionary attacks involve trial-and-error attempts using a list of potential passwords.

There are two types of dictionary attacks:

* **Off-line dictionary attacks**: The attacker knows the functions `f` and `c's`, and repeatedly tries different guesses `g ∈ A` until the list is exhausted or the passwords are guessed. Examples of off-line dictionary attack tools include `crack` and `john-the-ripper`.
* **On-line dictionary attacks**: The attacker has access to functions in `L` and tries guesses `g` until some `l(g)` succeeds. An example of an on-line dictionary attack is trying to log in by guessing a password.

## Info-Sec 2023
### Success Probability over a Time Period

Anderson's formula:

* $P$: probability of guessing a password in specified period of time
* $G$: number of guesses tested in 1 time unit
* $T$: number of time units
* $N$: number of possible passwords ($|A|$)

Then $P \geq \frac{TG}{N}$

## Info-Sec 2023
### Example

#### Goal
Passwords are drawn from a 96-char alphabet. The goal is to find the minimum password length given that:
- The system can test $10^4$ guesses per second.
- The probability of a success is to be $0.5$ over a $365$ day period.

#### Solution
The minimum number of possible passwords $N$ is given by:
$N ≥ \frac{TG}{P}$

where:
- $T = 365 \times 24 \times 60 \times 60$ (total seconds in a year)
- $G = 10^4$ (guesses per second)
- $P = 0.5$ (probability of success)

Substituting the values:
$N ≥ \frac{(365×24×60×60)×10^4}{0.5} = 6.31×10^{11}$

To ensure $N$ possible combinations:
$\sum_{j=0}^{s} 96^j ≥ N$

It follows that $s ≥ 6$, meaning passwords must be at least **6 chars long**.

## Exercise

### Given Values
X = number defined by last 2 digits of your student ID;  
Y = X mod 4

### Assumptions
- H is a cryptographic hash function with output size (Y+2)*16 bits.
- Scorpion-i (i=1-9) is a line of hardware chips for computing H, with the following specifications:
  | Model    | Hash Values per Second | Price    |
  |----------|------------------------|----------|
  | Scorpion-1| 10 * 1000               | $1000/2  |
  | Scorpion-2| 100 * 1000              | $2000/2  |
  | ...      | ...                    | ...      |
  | Scorpion-i| 10i * 1000             | $ii/2 * 1000 |

### Authentication System Requirements
- Password length: exactly 6 characters
- Alphabet size: N = (X mod 50) + 40

### Objective
An enemy aims to break a user's password with a success probability of (6+Y)*10% within a month using Scorpion chips.

### Task
Determine how much the enemy has to spend to achieve this within a month.

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

## Info-Sec 2023
### 21. Proactive Password Checking

Proactive password checking involves analyzing a proposed password for its "goodness". This process is always invoked and can detect and reject bad passwords based on an appropriate definition of "bad". The analysis can be done on a per-user, per-site basis.

The checking process requires:
- Pattern matching on words
- Execution of subprograms and use of their results
  - Examples include a spell checker

This approach is easy to set up and integrate into a password selection system.

Info-Sec 2023
22
Salting
Goal: slow dictionary attacks
Method: perturb hash function so that:
Parameter controls which hash function is used
Parameter differs for each password
So given n password hashes, and therefore n salts, need to hash guess n

# Info-Sec 2023
## 23
## Examples

### Vanilla UNIX method
Use DES to encipher a 0 message with a password as the key, iterating 25 times. 
Perturb the E table in DES in one of 4096 ways. 
A 12-bit salt flips entries 1–11 with entries 25–36.

### Alternate methods
Use the salt as the first part of the input to a hash function.

## Info-Sec 2023
### 24

Unix actually is based on a standard hash function for UNIX systems. This function hashes a password into an 11-character string using one of 4096 hash functions.

### Authentication System Components

The authentication system consists of the following components:
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

The owner decides to enhance the above password system by using salt so that the enemy will need to spend at least 10 times the above-mentioned amount of money to achieve the same goal. 

How many salt bits are needed to achieve this purpose? 

## Given Variables
- $N=(X \mod 50)+ 40$
- Output size of $H$ = $(Y+2)*16$ bits
- Scorpion-$i$ performance: $10i * 1000$ hash values/second
- Scorpion-$i$ price: $i^2/2 *$1000
- Password length: 6
- Success probability: $(6+Y)*10\%$
- Timeframe: 1 month

## Part 2 — Access Control
### Password Cracking: Do the Math

#### Assumptions
* Passwords are 8 characters, with 128 choices per character.
* Then, there are $128^8 = 2^{56}$ possible passwords.
* There is a password file with $2^{10}$ passwords.
* The attacker has a dictionary of $2^{20}$ common passwords.
* The probability is $1/4$ that a password is in the dictionary.

#### Work Measurement
Work is measured by the number of hashes.

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

## Part 2 — Access Control
### Password Cracking: Case I 

Attack 1 specific password without using a dictionary, e.g., the administrator’s password. 
This requires trying $256/2 = 255$ combinations on average, similar to an exhaustive key search.

Does salt help in this case?

## Part 2 — Access Control
### Password Cracking: Case II

#### Attack on a Specific Password with Dictionary

With salt:
- Expected work: $\frac{1}{4} (2^{19}) + \frac{3}{4} (2^{55}) \approx 2^{54.6}$
- In practice, try all passwords in dictionary… 
- …then work is at most $2^{20}$ and probability of success is $\frac{1}{4}$.

#### Without Salt

- One-time work to compute dictionary: $2^{20}$
- Expected work is of the same order as above.
- But with precomputed dictionary hashes, the “in practice” attack is essentially free…

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

## Part 2 — Access Control
### Password Cracking: Case IV

Any of 1024 passwords in a file, with a dictionary. The probability of one or more passwords being in the dictionary is $1 – (3/4)^{1024} ≈ 1$. Therefore, we can ignore the case where no password is in the dictionary.

If a salt is used, the expected work is less than $2^{22}$. 

See the book or slide notes for details.

The work is approximately equal to the size of the dictionary divided by the probability of a password being in the dictionary: 
$Work ≈ \frac{size\ of\ dictionary}{P(pwd\ in\ dictionary)}$

What if no salt is used? If dictionary hashes are not precomputed, the work is about $\frac{2^{19}}{2^{10}} = 2^9$.

## Info-Sec 2023
### 32

## Guessing Through L
Cannot prevent these attacks completely. 
Otherwise, legitimate users cannot log in.

## Mitigation Strategies
Make authentication attempts slow through:
- Backoff
- Disconnection
- Disabling

### Important Consideration
Be very careful with administrative accounts!

## Alternative Approach
Consider jailing:
- Allow login, but restrict activities.

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

## Info-Sec 2023
### 34

## Challenge-Response

User and system share a secret function *f* (in practice, *f* is a known function with unknown parameters, such as a cryptographic key).

The challenge-response process is as follows:

- User requests to authenticate
- System sends a random message *r* (the challenge)
- User responds with *f(r)* (the response) 

User and system interact as follows:

| Step | User | System |
|------|-------|---------|
| 1    | Request to authenticate |  |
| 2    |  | Random message *r* (the challenge) |
| 3    | *f(r)* (the response) |  |

# Info-Sec 2023
## 35
## Pass Algorithms

Challenge-response with the function f itself a secret. The challenge is a random string of characters. The response is some function of that string. Usually used in conjunction with fixed, reusable password. 

No visual element provided.

## Info-Sec 2023
### One-Time Passwords

One-Time Passwords are passwords that can be used exactly once. After use, they are immediately invalidated. They operate on a challenge-response mechanism, where:

* The challenge is the number of authentications.
* The response is the password for that particular number.

### Problems

The following problems are associated with One-Time Passwords:

* Synchronization of user and system
* Generation of good random passwords
* Password distribution problem

## Info-Sec 2023
### 37. S/Key

S/Key is a one-time password scheme based on the idea of Lamport. It uses a one-way hash function, such as MD5 or SHA-1.

The process works as follows:

* The user chooses an initial seed $k$.
* The system calculates a series of hashes:
  $h(k) = k_1$, $h(k_1) = k_2$, …, $h(k_{n-1}) = k_n$

The passwords are generated in reverse order:
| Password  | Value  |
|-----------|--------|
| $p_1$     | $k_n$  |
| $p_2$     | $k_{n-1}$|
| …         | …      |
| $p_{n-1}$ | $k_2$  |
| $p_n$     | $k_1$  |

## Info-Sec 2023
### 38
### S/Key Protocol

The system stores the maximum number of authentications `n`, the number of the next authentication `i`, and the last correctly supplied password `pi–1`.

The system computes `h(pi) = h(kn–i+1) = kn–i+2 = pi–1`. If there is a match with what is stored, the system replaces `pi–1` with `pi` and increments `i`.

## Info-Sec 2023
### 39 - C-R and Dictionary Attacks

C-R and dictionary attacks are similar to those used for fixed passwords. 

An attacker knows the challenge $r$ and the response $f(r)$. If $f$ is an encryption function, the attacker can try different keys. 

The attacker may only need to know the form of the response. They can determine if their guess is correct by checking if the deciphered object is of the right form.

### Example: Kerberos Version 4

Kerberos Version 4 used DES, but the keys had only 20 bits of randomness. As a result, attackers at Purdue were able to quickly guess the keys. They did this by checking if the deciphered tickets had a fixed set of bits in specific locations.

## Info-Sec 2023
### 40 - Encrypted Key Exchange

The Encrypted Key Exchange defeats off-line dictionary attacks. The idea is to use random challenges that are enciphered, making it impossible for an attacker to verify the correct decipherment of the challenge.

### Overview

Assume Alice and Bob share a secret password $s$. 

### Key Generation

In what follows, Alice needs to generate:
* A random public key $p$ 
* A corresponding private key $q$

Also, $k$ is a randomly generated session key, and $R_A$ and $R_B$ are random challenges.

Info-Sec 2023
41
EKE Protocol *
Now Alice, Bob share a randomly generated
secret session key k

## Part 2 — Access Control
### Something You Have

Something in your possession. Examples include:
- Car key
- Laptop computer (or MAC address)
- Password generator
- ATM card, smartcard, etc.

### Info-Sec 2023
#### 43. Hardware Support

## Token-based Authentication

Token-based authentication is used to compute a response to a challenge. This may involve enciphering or hashing the challenge. In some cases, it may require a PIN from the user.

### Examples of Objects for Authentication

The object a user possesses to authenticate can be, for example:
- A memory card (magnetic stripe)
- A smartcard

## Temporally-based Authentication

In temporally-based authentication, a different number is shown every minute or so. The computer knows what number to expect when the user enters it along with a fixed password.

## Memory Card

A memory card is used to store but not process data. Examples include:

* Magnetic stripe card (e.g., bank card)
* Electronic memory card

Memory cards are used alone for physical access (e.g., hotel rooms) and some require a password/PIN (e.g., ATMs).

### Drawbacks of Memory Cards

The drawbacks of memory cards include:
* Need special reader
* Loss of token issues
* User dissatisfaction (acceptable for ATM, not for computer access)

## Smartcard

A smartcard is credit-card like, with its own processor, memory, and I/O ports. It has ROM, EEPROM, and RAM memory. The smartcard executes a protocol to authenticate with a reader or computer.

There are different types of authentication:

* **Static**: similar to memory cards
* **Dynamic**: 
  + passwords created every minute
  + entered manually by user or electronically
* **Challenge-response**: 
  + computer creates a random number
  + smart card provides its hash (similar to Public Key)

Additionally, there are also USB dongles.

## Electronic Identity Cards

An important application of smart cards is a national e-identity (eID), which serves the same purpose as other national ID cards (e.g., a driver’s licence). However, an eID can provide stronger proof of identity.

### Example: German Card

The German card contains:
- Personal data
- Document number
- Card access number (six-digit random number)
- Machine-readable zone (MRZ): the password

### Uses

The card has multiple uses:
- ePass (government use)
- eID (general use)
- eSign (can have private key and certificate)

## User Authentication with eID

(No changes needed, as the text is already concise and coherent)

User authentication with eID * remains the same. 

If there were more texts to be normalized I would be happy to help.

## Part 2 — Access Control
### Something You Are
Biometric authentication operates on the principle "You are your key" (Schneier). This method verifies identity based on inherent personal characteristics. 

The three main categories of access control are:
- Something you **Are**
- Something you **Know**
- Something you **Have**

### Examples of Biometric Authentication
- Fingerprint
- Handwritten signature
- Facial recognition
- Speech recognition
- Gait (walking) recognition
- "Digital doggie" (odor recognition)
- Many more!

## Part 2 — Access Control
### Why Biometrics?

Biometrics may be better than passwords. However, cheap and reliable biometrics are needed. Today, biometrics is an active area of research. 

Biometrics are used in security today, for example:
* Thumbprint mouse
* Palm print for secure entry
* Fingerprint to unlock car doors, etc.

However, biometrics has not really become popular and has not lived up to its promise/hype (yet?).

## Info-Sec 2023
### Biometrics: Core Idea

Automated measurement of biological, behavioral features that identify a person.

### Types of Biometrics

#### Fingerprints
Uses optical or electrical techniques. Maps fingerprint into a graph, then compares with database. Measurements are imprecise, so approximate matching algorithms are used.

#### Voices
There are two types: 
- **Speaker Verification**: uses statistical techniques to test the hypothesis that the speaker is who is claimed (speaker dependent).
- **Speaker Recognition**: checks the content of answers (speaker independent).

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

### Biometric Authentication Methods
Authenticate user based on one of their physical characteristics:
* facial
* fingerprint
* hand geometry
* retina pattern
* iris
* signature
* voice

### Extracting Table Information
To accurately extract row labels, column labels, and cell values from a given table or matrix, a sample table is required as input. 

#### Hypothetical Table
| Column A | Column B | Column C
|----------|----------|----------
| 10       | 20       | 30
| 40       | 50       | 60
| 70       | 80       | 90

The extracted information can be structured into JSON as follows:

```json
{
  "schema_version": "1.0",
  "content_type": "table",
  "row_labels": ["Row 1", "Row 2", "Row 3"],
  "column_labels": ["Column A", "Column B", "Column C"],
  "values": [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
  ],
  "notes": "Example table for demonstration purposes."
}
```

### Handling CSV Files
If the table is in a CSV format:

```csv
"Row Labels","Column A","Column B","Column C"
"Row 1",10,20,30
"Row 2",40,50,60
"Row 3",70,80,90
```

The JSON output remains the same.

### Implementing in Python
To achieve this in Python using a pandas DataFrame:

```python
import pandas as pd
import json

# Sample DataFrame
data = {
    "Column A": [10, 40, 70],
    "Column B": [20, 50, 80],
    "Column C": [30, 60, 90]
}
df = pd.DataFrame(data, index=["Row 1", "Row 2", "Row 3"])

# Extract information
schema_version = "1.0"
content_type = "table"
row_labels = list(df.index)
column_labels = list(df.columns)
values = df.values.tolist()
notes = "Example DataFrame."

# Create JSON
output = {
    "schema_version": schema_version,
    "content_type": content_type,
    "row_labels": row_labels,
    "column_labels": column_labels,
    "values": values,
    "notes": notes
}

# Convert to JSON and print
print(json.dumps(output, indent=2))
```

This Python snippet creates a DataFrame similar to the hypothetical table, extracts the necessary components, and structures them into a JSON object.

## Operation of a Biometric System

Verification is analogous to user login via a smart card and a PIN. Identification, on the other hand, involves providing biometric information without any IDs, and the system compares it with stored templates to identify the user.

### No Visual Element Provided

There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

# Biometric Accuracy
## Palm Print
The system generates a matching score (a number) that quantifies similarity between the input and the stored template. Concerns include sensor noise and detection inaccuracy, which can lead to problems of false matches and false non-matches. 
* Further reading (Stallings textbook)

## Table Extraction and JSON Output
To accurately extract row labels, column labels, and cell values from a given table or matrix, and then structure this information into a JSON object with a specified schema, consider the following example.

### Example Table
| Country  | Population | Area (km²) |
|----------|------------|-------------|
| USA      | 331002651  | 9833520     |
| Canada   | 37742154   | 9984670     |
| Mexico   | 127575529  | 1964375     |

### JSON Schema Components
* **schema_version**: 1.0
* **content_type**: Table
* **row_labels**: Not explicitly provided; assume row numbers (1, 2, 3) or use actual row labels if available.
* **column_labels**: The headers of the table (Country, Population, Area (km²))
* **values**: The cell values, preserving exact numeric values
* **notes**: Any additional notes (empty in this case)

### Example JSON Output
```json
{
  "schema_version": 1.0,
  "content_type": "Table",
  "row_labels": [1, 2, 3],
  "column_labels": ["Country", "Population", "Area (km²)"],
  "values": [
    ["USA", 331002651, 9833520],
    ["Canada", 37742154, 9984670],
    ["Mexico", 127575529, 1964375]
  ],
  "notes": ""
}
```

## Implementation Details
### How It Works
1. **schema_version**: Specified as 1.0, indicating the version of the schema used.
2. **content_type**: Identified as "Table" to signify that the content represents a table.
3. **row_labels**: Extracted from the provided table or assumed if not directly available.
4. **column_labels**: Directly taken from the table headers.
5. **values**: A 2D array where each sub-array represents a row in the table. Numeric values are preserved exactly as provided.
6. **notes**: Left empty due to the absence of any additional information.

### Python Implementation
```python
import json

def extract_table_info(table):
    column_labels = table[0]
    data = table[1:]
    row_labels = list(range(1, len(data) + 1))  # Assuming row numbers as labels
    
    return {
        "schema_version": 1.0,
        "content_type": "Table",
        "row_labels": row_labels,
        "column_labels": column_labels,
        "values": data,
        "notes": ""
    }

# Example table
table = [
    ["Country", "Population", "Area (km²)"],
    ["USA", 331002651, 9833520],
    ["Canada", 37742154, 9984670],
    ["Mexico", 127575529, 1964375]
]

info = extract_table_info(table)

# Generating JSON
json_output = json.dumps(info)
print(json_output)
```

## Biometric Accuracy

### Characteristic Curve and Threshold Selection

The characteristic curve can be plotted with 2,000,000 comparisons. This curve is used to pick a threshold that balances error rates. 

### Note on Visual Elements

There is no visual element provided.

## Info-Sec 2023
### 58. Cautions

These can be fooled! It assumes the biometric device is accurate in the environment it is being used in. The transmission of data to the validator is tamperproof, correct.

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

## Info-Sec 2023
### 60
#### Location – Just a brief

If you know where a user is, you can validate their identity by verifying if the person is actually where the user claims to be. This method requires special-purpose hardware to locate the user. A GPS (Global Positioning System) device provides a location signature of an entity. The host uses an LSS (Location Signature Sensor) to obtain the signature for the entity.

# Info-Sec 2023
## 61 - Multiple Methods

Multiple authentication methods can be employed. For example, "where you are" requires an entity to have Location Services (LSS) and GPS, which also implies "what you have". 

Different methods can be assigned to different tasks. As users perform more sensitive tasks, they must authenticate in more ways, presumably with increasing stringency. 

The system file describes the required authentication. It also includes controls on:

* Access (e.g., time of day)
* Resources
* Requests to change passwords

## Pluggable Authentication Modules

### Info-Sec 2023
#### 62 - PAM

The idea behind PAM (Privileged Access Management) is that when a program needs to authenticate, it checks a central repository for methods to use. This is achieved through a library call: `pam_authenticate`.

The configuration for PAM is typically stored in files located in `/etc/pam.d/`, with the file name corresponding to the name of the program.

The authentication process involves modules that perform the actual authentication checking. These modules can be configured with different control flags:

* **sufficient**: Succeed if the module succeeds.
* **required**: Fail if the module fails, but all required modules must be executed before reporting failure.
* **requisite**: Like required, but don't check all modules.
* **optional**: Invoke only if all previous modules fail.

### Info-Sec 2023
#### 63

##### Example PAM File
```markdown
auth    sufficient    /usr/lib/pam_ftp.so
auth    required    /usr/lib/pam_unix_auth.so use_first_pass
auth    required    /usr/lib/pam_listfile.so onerr=succeed \
                    item=user sense=deny file=/etc/ftpusers
```

##### For ftp:

* If user “anonymous”, return okay; if not, set PAM_AUTHTOK to password, PAM_RUSER to name, and fail
* Now check that password in PAM_AUTHTOK belongs to that of user in PAM_RUSER; if not, fail
* Now see if user in PAM_RUSER named in /etc/ftpusers; if so, fail; if error or not found, succeed

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

Kerberos v4 Overview
a basic third-party authentication scheme
have an Authentication Server (AS) 
users initially negotiate with AS to identify self 
AS provides a non-corruptible authentication credential (ticket granting ticket TGT) 
have a Ticket Granting server (TGS)
users subsequently request access to other services from TGS on basis of users TGT
using a complex protocol using DES

# Kerberos 4 Overview

## Graph Representation in JSON

To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. 

### Example Graph

The graph has the following properties:
- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representations

There are multiple ways to represent this graph in JSON.

#### Detailed Representation

Here's a detailed representation including node labels, edge lists, and directionality:

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

#### Compact Representation

For a more compact and standard representation:

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

#### Adjacency List Representation

Or, if directionality is implied by the presence of an edge:

```json
{
  "A": ["B", "C"],
  "B": ["D"],
  "C": ["E"],
  "D": ["E"],
  "E": ["B"]
}
```

## Code to Generate Graph JSON

If you were starting from a graph defined in code (for example, using NetworkX in Python), you could generate such a JSON like this:

```python
import networkx as nx
import json

# Create a directed graph
G = nx.DiGraph()

# Add nodes
G.add_nodes_from(['A', 'B', 'C', 'D', 'E'])

# Add edges
G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')])

# Convert to JSON
nodes = [{"id": node} for node in G.nodes]
edges = [{"source": edge[0], "target": edge[1]} for edge in G.edges]

graph_json = {"nodes": nodes, "edges": edges}

print(json.dumps(graph_json, indent=2))
```

This Python snippet creates a directed graph with NetworkX and then converts it into a JSON representation.

# Kerberos v4 Dialogue

## Graph Representation in JSON

To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. 

### Example Graph

* **Nodes**: A, B, C, D, E
* **Edges**:
  * A → B
  * A → C
  * B → D
  * C → E
  * D → E
  * E → B

## JSON Representations

### Standard JSON Representation

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

### Compact JSON Representation

For a more compact and standard representation, especially in graph databases and network analysis tools:

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

### Directed Graph JSON

If directionality is implied (e.g., in directed graphs):

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

## Generating the Graph Structure

If you have a graph in a different format or need to dynamically generate this structure, you could use Python with NetworkX library to handle graphs and then convert to JSON:

```python
import networkx as nx
import json

# Create a directed graph
G = nx.DiGraph()

# Add nodes
G.add_nodes_from(['A', 'B', 'C', 'D', 'E'])

# Add edges
G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')])

# Convert to compact JSON
data = {
    "nodes": list(G.nodes),
    "edges": [{"from": edge[0], "to": edge[1]} for edge in G.edges]
}

print(json.dumps(data, indent=2))
```

This example creates a directed graph with specified nodes and edges and then converts it into a JSON object.

## Kerberos Version 5

Developed in the mid-1990s, Kerberos Version 5 was specified as Internet standard RFC 1510. It provides improvements over version 4, addressing both environmental shortcomings and technical deficiencies.

### Improvements

The improvements include:

* Encryption algorithm
* Network protocol
* Byte order
* Ticket lifetime
* Authentication forwarding
* Interrealm authentication

### Addressed Deficiencies

The addressed deficiencies include:

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
## Overview
The protocol involves the following steps:
- Client Authentication to the AS
- Client Service Authorization
- Client Service Request

## Representing a Graph in JSON
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph.

### Example Graph
- **Nodes**: A, B, C, D, E
- **Edges**: 
  - A -> B
  - A -> C
  - B -> D
  - C -> E
  - D -> E
  - E -> B

### JSON Representations

#### Detailed Representation
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

#### Compact Representation
However, for a more conventional and compact graph representation in JSON, especially in graph libraries and databases, you might see it represented with an adjacency list or directly with nodes and edges without explicit directionality labels, assuming the directionality is implied by the source and target:

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

#### Detailed Representation with Edge Properties
Or, with more detailed node information and edge properties:

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
    {"id": 1, "source": "A", "target": "B", "type": "directed"},
    {"id": 2, "source": "A", "target": "C", "type": "directed"},
    {"id": 3, "source": "B", "target": "D", "type": "directed"},
    {"id": 4, "source": "C", "target": "E", "type": "directed"},
    {"id": 5, "source": "D", "target": "E", "type": "directed"},
    {"id": 6, "source": "E", "target": "B", "type": "directed"}
  ]
}
```

## Generating the JSON Programmatically

### Python Code

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id, label):
        self.nodes.append({"id": id, "label": label})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target})

    def to_json(self):
        return json.dumps({"nodes": self.nodes, "edges": self.edges}, indent=2)

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

This example creates a simple graph, adds nodes and edges, and then outputs the graph as a JSON string.

### Kerberos v5 Dialogue

## Graph Representation in JSON

To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. This graph will have 5 nodes and 7 edges. The graph is directed.

### Graph Details

* **Nodes (Vertices):** A, B, C, D, E
* **Edges:** 
  - A → B
  - A → C
  - B → D
  - C → B
  - C → E
  - D → E
  - E → B

## JSON Representations

### Standard Representation

Here's how you could represent this directed graph in JSON:

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
      {"source": "A", "target": "B", "direction": "out"},
      {"source": "A", "target": "C", "direction": "out"},
      {"source": "B", "target": "D", "direction": "out"},
      {"source": "C", "target": "B", "direction": "out"},
      {"source": "C", "target": "E", "direction": "out"},
      {"source": "D", "target": "E", "direction": "out"},
      {"source": "E", "target": "B", "direction": "out"}
    ]
  }
}
```

### Explanation

* **Nodes:** Each node is represented by a unique `id`.
* **Edges:** Each edge has a `source` (the node it originates from), a `target` (the node it points to), and a `direction` (which in this case is always "out" for directed edges).

### Alternative Representation

If the directionality is implied by the presence of `source` and `target` fields (with the edge direction being from `source` to `target`), you might see a more compact form:

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
      {"source": "A", "target": "B"},
      {"source": "A", "target": "C"},
      {"source": "B", "target": "D"},
      {"source": "C", "target": "B"},
      {"source": "C", "target": "E"},
      {"source": "D", "target": "E"},
      {"source": "E", "target": "B"}
    ]
  }
}
```

This representation assumes that all edges are directed from `source` to `target`. The choice between these representations depends on your specific use case and the requirements of the systems or algorithms you're working with.

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

Identity Management


### Slide Image
There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.


## Identity Federation

There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

## Standards Used

The following standards are used:

* Security Assertion Markup Language (SAML): an XML-based language for the exchange of security information between online business partners. SAML is part of OASIS (Organization for the Advancement of Structured Information Standards) standards for federated identity management, which includes standards like WS-Federation for browser-based federation.

To achieve the desired outcome, a few mature industry standards are needed.

Federated Identity Examples


### Slide Image
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.


FIM vs. SSO
SSO: Single Sign-On
Allows users to access multiple web applications at once, using just one set of credentials. 
Beyond the workforce, companies can utilize SSO to help customers access various sections of one account. 
FIM 
As a tool, SSO fits within the broader model of FIM.
The key difference between SSO and FIM is while SSO is designed to authenticate a single credential across various systems within one organization, federated identity management systems offer single access to a number of applications across various enterprises.

No change is needed for the provided text as it appears to be a simple header with a reference. Here is the normalized text in Markdown:

*Extended Material: Biometrics*
Slides borrowed from Mark Stamp’s web: https://www.cs.sjsu.edu/~stamp/infosec/powerpoint/

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

## Part 2 — Access Control
### Identification vs Authentication

Identification is the process of determining "Who goes there?" It involves comparing a given input to a large set of known identities, which is a one-to-many comparison. An example of identification is the FBI fingerprint database.

Authentication, on the other hand, verifies if the person is "who you say you are?" This process involves a one-to-one comparison. An example of authentication is a thumbprint mouse.

The identification problem is more difficult because it involves more comparisons, leading to a higher chance of "random" matches. However, we are mostly interested in authentication.

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

## Part 2 — Access Control

### Cooperative Subjects

We differentiate between authentication for cooperative subjects and identification for uncooperative subjects. 
For example, facial recognition is used in Las Vegas casinos to detect known cheaters, and also in airports to detect terrorists. 
Often, less than ideal enrollment conditions are present. 
In such cases, the subject may try to confuse the recognition phase. 

However, when the subject is cooperative, it makes the process much easier. 
Since we are focused on authentication, we can assume that the subjects are cooperative.

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

## Part 2 — Access Control

### Fingerprint History

The history of fingerprinting dates back to several key events:
* 1823: Professor Johannes Evangelist Purkinje discussed 9 fingerprint patterns.
* 1856: Sir William Hershel used fingerprints (in India) on contracts.
* 1880: Dr. Henry Faulds published an article in Nature about using fingerprints for identification.
* 1883: Mark Twain's *Life on the Mississippi* featured a story where a murderer was identified by their fingerprint.

## Part 2 — Access Control

### Fingerprint History

In 1888, Sir Francis Galton developed a classification system for fingerprints based on the study of "minutia." His system remains usable today and also verified that fingerprints do not change over time. 

Some countries require a fixed number of matching "points" (minutia) for identification in criminal cases. The requirements vary:
- In Britain, at least 15 points are required.
- In the US, there is no fixed number of points required.

## Part 2 — Access Control
### Fingerprint Comparison

Fingerprint patterns are classified into three main types:
- Loop (double)
- Whorl
- Arch

These patterns are further illustrated through examples:
- Examples of loops, whorls, and arches

From these patterns, specific details are extracted:
- Minutia extracted from these features

### Note on Visual Elements
There are no visual elements provided for the following slides. Please share the images to allow for descriptions focusing on their learning value.

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

A popular biometric measures the shape of the hand, including:
- Width of hand
- Width of fingers
- Length of fingers, etc.

However, human hands are not so unique. Therefore, hand geometry is sufficient for many situations and okay for authentication but not useful for identification problems.

## Part 2 — Access Control
### Hand Geometry

#### Advantages
- Quick — 1 minute for enrollment, 5 seconds for recognition
- Hands are symmetric — so what?

#### Disadvantages
- Cannot use on very young or very old
- Relatively high equal error rate

## Part 2 — Access Control
### Iris Patterns

Iris pattern development is “chaotic” with little or no genetic influence. Even for identical twins, the patterns are uncorrelated. The pattern is stable through a person's lifetime.

## Part 2 — Access Control
### Iris Recognition: History

* 1936: suggested by ophthalmologist
* 1980s: popularized in James Bond film(s)
* 1986: first patent appeared
* 1994: John Daugman patents new-and-improved technique

Patents owned by Iridian Technologies.

Part 2 ⎯ Access Control                                                                                                  98
Iris Scan
Scanner locates iris
Take b/w photo
Use polar coordinates…
2-D wavelet transform
Get 256 byte iris code


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


However, for a more detailed and structured representation that includes directionality explicitly in the graph definition, you might see it defined differently, especially if you're working with a specific graph database or library that has its own format:


{
  "graph": {
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
    ],
    "directionality": "directed"
  }
}


### Directionality

In both examples above, the directionality of the graph is implied by the "edges" section where each edge is listed with a source (or "from") and a target (or "to"). The direction of an edge from node A to node B implies that the edge goes "out" of A and "in" to B.

### Code to Generate This JSON

If you're working in Python and want to generate a similar JSON structure from your own data, here's a simple example:

python
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


This Python example creates a simple directed graph and outputs it as a JSON string. You can expand on this by adding more features such as edge weights, node properties, etc., depending on your requirements.



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


However, for a more detailed and structured representation that also captures directed/undirected nature explicitly and potentially other graph attributes, you might see representations like this:


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
      {"source": "A", "target": "B"},
      {"source": "B", "target": "C"},
      {"source": "C", "target": "A"},
      {"source": "D", "target": "B"}
    ]
  }
}


In this representation:
- The `directed` property indicates if the graph is directed or not. A value of `true` means the graph is directed, and `false` would mean it's undirected.
- The `nodes` list contains all the unique node labels.
- The `edges` list contains all the edges represented by their source and target nodes.

### Code to Generate This JSON

If you're working in Python, here's a simple way to create and represent such a graph:

python
import json

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.nodes = []
        self.edges = []

    def add_node(self, id):
        if id not in [node['id'] for node in self.nodes]:
            self.nodes.append({"id": id})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target})

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
g.add_edge("C", "A")
g.add_edge("D", "B")

print(g.to_json())


This Python code defines a simple `Graph` class and then creates a directed graph with nodes A, B, C, D and specified edges, finally outputting the graph in a structured JSON format.



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


However, a more compact and commonly used format for graph representation, especially in graph databases and libraries, would be to use an adjacency list or to directly list nodes and edges without repetitive information like labels for nodes if they are just identifiers.

### Alternative JSON Representation


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


Or, if you want to explicitly denote directionality and assume edges are directed unless otherwise specified:


{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"source": "A", "target": "B", "directed": true},
    {"source": "A", "target": "C", "directed": true},
    {"source": "B", "target": "D", "directed": true},
    {"source": "C", "target": "E", "directed": true},
    {"source": "D", "target": "E", "directed": true},
    {"source": "E", "target": "B", "directed": true}
  ]
}


### Code to Generate This

If you were to generate this JSON programmatically, you might start with a graph represented in a language-specific data structure (like a dictionary of adjacency lists for a simple implementation) and then serialize it to JSON.

python
import json

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = []

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target})

    def to_json(self):
        graph_json = {
            "nodes": list(self.nodes),
            "edges": self.edges
        }
        return json.dumps(graph_json, indent=2)

# Usage
graph = Graph()
for node in ["A", "B", "C", "D", "E"]:
    graph.add_node(node)

graph.add_edge("A", "B")
graph.add_edge("A", "C")
graph.add_edge("B", "D")
graph.add_edge("C", "E")
graph.add_edge("D", "E")
graph.add_edge("E", "B")

print(graph.to_json())


This Python example creates a simple graph and then converts it into a JSON string. The resulting JSON string would look similar to one of the representations provided above.



### Slide Image
To accomplish the task of extracting surrounding explanatory text separately from formula text and returning formulas in LaTeX, we'll need to follow a step-by-step approach. This process typically involves:

1. **Input Preparation**: Preparing the input text that contains both explanatory text and formulas.
2. **Formula Identification**: Identifying the parts of the text that are formulas. This can be complex as it depends on the format and structure of the input text.
3. **LaTeX Conversion**: Converting the identified formulas into LaTeX format.
4. **Text Separation**: Separating the explanatory text from the formulas.

For simplicity, let's assume we are working with a basic example where formulas are clearly distinguishable from text, possibly marked by specific characters or keywords.

### Example Input

Let's consider an example input:

"The equation for the area of a circle is $A = \pi r^2$. This is a fundamental concept in geometry. Another important formula is $E = mc^2$, which relates energy and mass."

### Step-by-Step Solution

#### Step 1: Input Preparation

Ensure the input text is properly formatted and accessible. For this example, we'll assume it's a string in Python.

#### Step 2: Formula Identification

We'll use a simple approach to identify formulas, assuming they are enclosed in dollar signs `$`.

#### Step 3: LaTeX Conversion

The identified formulas might already be in a LaTeX-compatible format or very close to it. 

#### Step 4: Text Separation

Here's a Python script to perform these steps:

python
import re

def extract_and_convert_latex(text):
    # Regular expression to find formulas enclosed in dollar signs
    pattern = r'\$(.*?)\$'
    
    # Find all formulas
    formulas = re.findall(pattern, text)
    
    # Convert to LaTeX (simple example, assumes input is close to LaTeX)
    latex_formulas = [f"${formula}$" for formula in formulas]
    
    # Remove formulas from text
    text_without_formulas = re.sub(pattern, '', text)
    
    # Clean up text (remove extra whitespace)
    explanatory_text = re.sub(' +', ' ', text_without_formulas)
    
    return explanatory_text.strip(), latex_formulas

# Example usage
input_text = "The equation for the area of a circle is $A = \pi r^2$. This is a fundamental concept in geometry. Another important formula is $E = mc^2$, which relates energy and mass."

explanatory_text, latex_formulas = extract_and_convert_latex(input_text)

print("Explanatory Text:")
print(explanatory_text)
print("\nLaTeX Formulas:")
for i, formula in enumerate(latex_formulas):
    print(f"Formula {i+1}: {formula}")


### Output


Explanatory Text:
The equation for the area of a circle is . This is a fundamental concept in geometry. Another important formula is , which relates energy and mass.

LaTeX Formulas:
Formula 1: $A = \pi r^2$
Formula 2: $E = mc^2$


This example provides a basic framework. Real-world applications might require more sophisticated Natural Language Processing (NLP) techniques, especially for more complex or varied input formats.



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


However, for a more compact and conventional representation, especially in graph theory and network analysis, you might see graphs represented in formats like GraphML, GEXF, or simple adjacency lists. The above JSON format is straightforward but let's adjust it to be more compact and useful:

### Compact JSON Representation


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


Or, if you want to make it explicitly clear that it's a directed graph:

### Directed Graph JSON


{
  "graph": {
    "directed": true,
    "nodes": ["A", "B", "C", "D", "E"],
    "edges": [
      {"source": "A", "target": "B"},
      {"source": "A", "target": "C"},
      {"source": "B", "target": "D"},
      {"source": "C", "target": "E"},
      {"source": "D", "target": "E"},
      {"source": "E", "target": "B"}
    ]
  }
}


These representations can easily be parsed and manipulated in most programming languages, making them suitable for software applications working with graph data structures.



### Slide Image
To accomplish the task of extracting surrounding explanatory text separately from formula text and returning formulas in LaTeX, we'll need to follow a step-by-step approach. This process typically involves:

1. **Input Preparation**: Preparing the input text that contains both explanatory text and formulas.
2. **Formula Identification**: Identifying the parts of the text that are formulas. This can be complex as it depends on the format and structure of the input text.
3. **LaTeX Conversion**: Converting the identified formulas into LaTeX format.
4. **Text Separation**: Separating the explanatory text from the formula text.

Let's consider a hypothetical example to illustrate this process. Assume we have a string that contains a mixture of explanatory text and a formula:

`"The equation for the area of a circle is \(A = \pi r^2\), which is a fundamental concept in geometry. Another key equation is \(E = mc^2\)."`

### Step 1 & 2: Input Preparation and Formula Identification

For simplicity, let's assume formulas are enclosed in parentheses and start with a letter or a number.

### Step 3 & 4: LaTeX Conversion and Text Separation

We'll use Python with regular expressions for this task:

python
import re

def extract_and_convert_latex(text):
    # Regular expression pattern to match formulas
    pattern = r'\([A-Za-z0-9\s\+\-\*\/\^=]+?\)'
    formulas = re.findall(pattern, text)

    # Convert matched formulas to LaTeX and remove from text
    for formula in formulas:
        latex_formula = formula.strip('()')  # Simple conversion, assuming no complex LaTeX needed
        text = text.replace(formula, f"[{latex_formula}]")  # Placeholder for now

    # Refine LaTeX conversion
    def refine_latex(match):
        formula = match.group(0).strip('[]')
        return f"${formula}$"

    text = re.sub(r'\[([A-Za-z0-9\s\+\-\*\/\^=]+?)\]', refine_latex, text)

    # Separate formulas from text
    formulas = re.findall(r'\$([A-Za-z0-9\s\+\-\*\/\^=]+?)\$', text)

    return text, formulas

# Example usage
input_text = "The equation for the area of a circle is (A = \pi r^2), which is a fundamental concept in geometry. Another key equation is (E = mc^2)."
cleaned_text, latex_formulas = extract_and_convert_latex(input_text)

print("Cleaned Text:", cleaned_text)
print("LaTeX Formulas:", latex_formulas)


### Output


Cleaned Text: The equation for the area of a circle is $[A = \pi r^2]$, which is a fundamental concept in geometry. Another key equation is $[E = mc^2]$.
LaTeX Formulas: ['A = \\pi r^2', 'E = mc^2']


This example demonstrates a basic approach. Real-world applications might require more sophisticated Natural Language Processing (NLP) techniques, especially for accurately identifying and converting complex mathematical expressions into LaTeX format. Libraries such as `sympy` for symbolic mathematics and more advanced NLP techniques can be integrated for more complex scenarios.


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

## Part 2 — Access Control

### Iris Scan Error Rate

* Distance
* Distance
* Fraud rate
* == Equal Error Rate

### Graph Representation in JSON

To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

#### Example Graph

* **Nodes**: A, B, C, D, E
* **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

#### JSON Representation

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

#### Alternative JSON Representations

For a more compact and standard representation, especially in graph databases and libraries (like Neo4j, NetworkX), you might see it represented with an adjacency list or directly through node and edge definitions without explicit direction properties:

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
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"}
  ]
}
```

Or even more succinctly, with directionality implied by the edge definition:

```json
{
  "graph": {
    "nodes": ["A", "B", "C", "D", "E"],
    "edges": [["A", "B"], ["A", "C"], ["B", "D"], ["C", "E"], ["D", "E"], ["E", "B"]]
  }
}
```

### Code to Generate JSON

If you were to generate this JSON programmatically from a graph data structure, you might do something like this in Python:

```python
import json
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes
G.add_nodes_from(['A', 'B', 'C', 'D', 'E'])

# Add edges
G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')])

# Prepare JSON
nodes = [{"id": node, "label": f"Node {node}"} for node in G.nodes]
edges = [{"source": edge[0], "target": edge[1], "direction": "OUT"} for edge in G.edges]

# Convert to JSON
graph_json = {"nodes": nodes, "edges": edges}

print(json.dumps(graph_json, indent=2))
```

Or using a custom Graph class:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = []

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, source, target):
        self.edges.append((source, target))

    def to_json(self):
        data = {
            "nodes": [{"id": node, "label": f"Node {node}"} for node in self.nodes],
            "edges": [{"source": source, "target": target, "direction": "OUT"} for source, target in self.edges]
        }
        return json.dumps(data, indent=2)

# Example usage
graph = Graph()
for node in ['A', 'B', 'C', 'D', 'E']:
    graph.add_node(node)

edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')]
for source, target in edges:
    graph.add_edge(source, target)

print(graph.to_json())
```

## Part 2 — Access Control
### Attack on Iris Scan

An attacker could use a good photo of an eye to bypass an iris scan. For example, an Afghan woman was authenticated by an iris scan using an old photo. 
The story can be found [here](link). 
To prevent such an attack, a scanner could use light to verify that it is scanning a "live" iris.

## Part 2 — Access Control

### Equal Error Rate Comparison

The equal error rate (EER) is where the fraud rate equals the insult rate. 
Fingerprint biometrics used in practice have EERs ranging from about $10^{-3}$ to as high as 5%. 
Hand geometry has an EER of about $10^{-3}$. 
In theory, iris scan has an EER of about $10^{-6}$. 

The enrollment phase may be critical to accuracy. 
Most biometrics perform much worse than fingerprint. 
Biometrics are useful for authentication, but for identification, they are not so impressive today.

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
### Giới Thiệu

Bảo mật thông tin là một phần quan trọng của an toàn thông tin. Nó liên quan đến việc bảo vệ thông tin khỏi các truy cập trái phép, sử dụng sai, tiết lộ hoặc phá hủy.

## Các Khái Niệm Cơ Bản

* **An toàn thông tin**: Là việc bảo vệ thông tin khỏi các mối đe dọa và đảm bảo tính bảo mật, toàn vẹn và sẵn sàng của thông tin.
* **Bảo mật thông tin**: Là một phần của an toàn thông tin, tập trung vào việc bảo vệ thông tin khỏi các truy cập trái phép.

## Các Mối Đe Dọa

* **Malware**: Phần mềm độc hại, bao gồm virus, worm, trojan, ransomware, ...
* **Phishing**: Hình thức tấn công mạng bằng cách giả mạo thông tin để đánh cắp thông tin cá nhân.

## Các Biện Pháp Bảo Mật

* **Mã hóa**: Quá trình biến đổi thông tin thành dạng không thể đọc được nếu không có khóa giải mã.
* **Tường lửa**: Hệ thống bảo mật mạng ngăn chặn các truy cập trái phép.

## Công Cụ Bảo Mật

| Công Cụ | Chức Năng |
| --- | --- |
| Firewall | Ngăn chặn truy cập trái phép |
| Antivirus | Phát hiện và loại bỏ malware |
| VPN | Mã hóa và bảo vệ thông tin truyền qua mạng |

## Các Kỹ Thuật Mã Hóa

* **Mã hóa đối xứng**: Sử dụng cùng một khóa để mã hóa và giải mã.
* **Mã hóa bất đối xứng**: Sử dụng cặp khóa công khai và riêng tư để mã hóa và giải mã.

## Công Thức Mã Hóa

* **AES**: Advanced Encryption Standard, sử dụng mã hóa đối xứng.
* **RSA**: Rivest-Shamir-Adleman, sử dụng mã hóa bất đối xứng.

## Chuẩn Bảo Mật

* **ISO 27001**: Chuẩn quốc tế về hệ thống quản lý bảo mật thông tin.

## Best Practice

* **Sao lưu dữ liệu**: Thực hiện sao lưu dữ liệu thường xuyên để phòng tránh mất mát dữ liệu.
* **Cập nhật phần mềm**: Cập nhật phần mềm thường xuyên để vá các lỗi bảo mật.