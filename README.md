# General Clinic System by Waheed Khaled.

## Technologies:

- **Backend server side**:
  ![Python](https://img.shields.io/badge/Python%20-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white)

- **Frontend server side**:
  ![JavaScript](https://img.shields.io/badge/JavaScript%20-%23F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black)

Command to run application

First move to general_clinic folder/directory:

```bash
cd general_clinic
```

Second run django app:

```bash
python -OO manage.py runserver
```

Notes:

python -OO option will remove docstring during runtime of script to accelerate the program, for more information run:

```bash
python --help
```

# General Clinic Database Schema

This repository contains SQL statements to set up a general clinic database.

## Database Entity Relationship Diagram

Here's an entity-relationship diagram (ERD) illustrating the structure of the car hire database:

![ERD](./erd.png)

## Schema

The SQL script sets up three tables: `Patient`, `Doctor`, `Staff`, `Appointment`, `Payment` and `Medical_Record`.

### Customers Table

```sql
CREATE TABLE Patient (
    Patient_ID UUID PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Date_of_Birth DATE,
    Contact_Info VARCHAR(100),
    Address VARCHAR(100)
);

CREATE TABLE Doctor (
    Doctor_ID UUID PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Specialty VARCHAR(50),
    Contact_Info VARCHAR(100)
);

CREATE TABLE Staff (
    Staff_ID UUID PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Position VARCHAR(50),
    Contact_Info VARCHAR(100)
);

CREATE TABLE Appointment (
    Appointment_ID UUID PRIMARY KEY,
    Patient_ID UUID,
    Doctor_ID UUID,
    Staff_ID UUID,
    Appointment_DateTime TIMESTAMP,
    Status VARCHAR(20),
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
);

CREATE TABLE Medical_Record (
    Record_ID UUID PRIMARY KEY,
    Patient_ID UUID,
    Doctor_ID UUID,
    Date DATE,
    Diagnosis TEXT,
    Treatment TEXT,
    Prescription TEXT,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID)
);

CREATE TABLE Payment (
    Payment_ID UUID PRIMARY KEY,
    Patient_ID UUID,
    Amount DECIMAL(10, 2),
    Date DATE,
    Payment_Method VARCHAR(50),
    Payment_Process_Method VARCHAR(50),
    Staff_ID UUID,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
);
```
