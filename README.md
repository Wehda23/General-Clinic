# General Clinic System by Waheed Khaled.

## Technologies:

- **Backend server side**:

  ![Python](https://img.shields.io/badge/Python%20-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white)
  ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
  ![Django Rest API Framework](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
  ![Redis](https://img.shields.io/badge/redis-CC0000.svg?&style=for-the-badge&logo=redis&logoColor=white)

- **Frontend server side**:

  ![JavaScript](https://img.shields.io/badge/JavaScript%20-%23F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black)
  ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
  ![Redux](https://img.shields.io/badge/Redux-593D88?style=for-the-badge&logo=redux&logoColor=white)
  ![React Router](https://img.shields.io/badge/React_Router-CA4245?style=for-the-badge&logo=react-router&logoColor=white)

- **Other Tools**:

  ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white)
  ![MySQL](https://img.shields.io/badge/MySQL%20-%2320232a.svg?style=for-the-badge&logo=mysql&logoColor=white&color=4479A1)
  ![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
  ![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)

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

Here's an entity-relationship diagram (ERD) illustrating the structure of General Clinic database:

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
