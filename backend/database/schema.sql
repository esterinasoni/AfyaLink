-- ============================================================
-- AfyaLink Database Schema
-- Run this file once to create all tables
-- ============================================================

-- Enable UUID generation in PostgreSQL
CREATE EXTENSION IF NOT EXISTS "pgcrypto";


-- ============================================================
-- TABLE 1: patients
-- national_id links to patients' Kenya National ID
-- ============================================================
CREATE TABLE patients (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    national_id     VARCHAR(10) UNIQUE NOT NULL,
    full_name       VARCHAR(200) NOT NULL,
    date_of_birth   DATE NOT NULL,
    gender          VARCHAR(20) CHECK (gender IN ('male', 'female', 'other')),
    phone           VARCHAR(20) UNIQUE NOT NULL,
    email           VARCHAR(200) UNIQUE,
    blood_type      VARCHAR(5) CHECK (blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB-','AB+', 'O+', 'O-')),
    allergies       TEXT,
    password_hash   VARCHAR(255) NOT NULL,  
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- TABLE 2: hospitals
-- ============================================================
CREATE TABLE hospitals (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    khis_code       VARCHAR (20) UNIQUE,  -- Kenya Health Information System facility code
    name            VARCHAR(200) NOT NULL,
    ownership       VARCHAR(50) NOT NULL CHECK (ownership IN ('public', 'private', 'faith_based', 'ngo')),
    facility_level  VARCHAR(50) NOT NULL CHECK (facility_level IN ('level_2', 'level_3', 'level_4', 'level_5', 'level_6')),
    type            VARCHAR(50) NOT NULL CHECK (type IN ('dispensary', 'health_centre', 'clinic', 'sub_county_hospital', 'county_hospital', 'national_referral_hospital', 'specialist_hospital')),
    county          VARCHAR(100) NOT NULL,
    sub_county      VARCHAR(100),
    address         TEXT,
    phone           VARCHAR(20),
    email           VARCHAR(200),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- TABLE 3: doctors
-- ============================================================
CREATE TABLE doctors (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hospital_id      UUID NOT NULL REFERENCES hospitals(id),
    full_name        VARCHAR(200) NOT NULL,
    specialisation   VARCHAR(200),
    licence_number   VARCHAR(100) UNIQUE,  
    phone            VARCHAR(20),
    email            VARCHAR(200) UNIQUE NOT NULL,
    password_hash    VARCHAR(255) NOT NULL,
    role             VARCHAR(50) NOT NULL CHECK (role IN ('doctor', 'pharmacist', 'nurse', 'admin')),
    is_active        BOOLEAN DEFAULT TRUE,
    created_at       TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- TABLE 4: appointments
-- ============================================================
CREATE TABLE appointments (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id       UUID NOT NULL REFERENCES patients(id),
    doctor_id        UUID NOT NULL REFERENCES doctors(id),
    hospital_id      UUID NOT NULL REFERENCES hospitals(id),
    scheduled_at     TIMESTAMP NOT NULL,
    status           VARCHAR(50) CHECK (status IN ('scheduled', 'checked_in', 'in_progress', 'completed', 'cancelled')),
    queue_number     VARCHAR(20), 
    reason           TEXT,                  -- why patient is coming
    notes            TEXT,                  -- doctor's pre-visit notes
    created_at       TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- TABLE 5: medical_records
-- diagnosis can later support ICD-10 code
-- ============================================================
CREATE TABLE medical_records (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id       UUID NOT NULL REFERENCES patients(id),
    doctor_id        UUID NOT NULL REFERENCES doctors(id),
    appointment_id   UUID REFERENCES appointments(id),
    hospital_id      UUID NOT NULL REFERENCES hospitals(id),
    diagnosis        TEXT NOT NULL,
    symptoms         TEXT,
    treatment_notes  TEXT,
    follow_up_date   DATE,
    recorded_at      TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- TABLE 6: prescriptions
-- Each prescription row = one drug in one visit
-- One medical record can have many prescriptions
-- ============================================================
CREATE TABLE prescriptions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    medical_record_id   UUID NOT NULL REFERENCES medical_records(id),
    patient_id          UUID NOT NULL REFERENCES patients(id),
    prescribed_by       UUID NOT NULL REFERENCES doctors(id),
    drug_name           VARCHAR(200) NOT NULL,
    generic_name        VARCHAR(200),       -- e.g. "Amoxicillin" vs brand "Amoxil"
    dosage              VARCHAR(100),       -- e.g. "500mg"
    frequency           VARCHAR(100),       -- e.g. "3 times daily"
    duration_days       INTEGER,
    route               VARCHAR(50) CHECK (route in ('oral', 'IV', 'IM', 'SC', 'intradermal','epidural', 'intraarticular', 'nebulized', 'inhalation', 'sublingual','buccal', 'transdermal', 'nasal', 'ophthalmic', 'otic', 'vaginal', 'rectal', 'topical')),
    instructions        TEXT,
    is_active           BOOLEAN DEFAULT TRUE,
    prescribed_at       TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- TABLE 7: audit_logs
-- Track access to patient records
-- Helps with accountability and security monitoring
-- Useful for compliance and auditing
-- ============================================================
CREATE TABLE audit_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id       UUID REFERENCES doctors(id),
    patient_id      UUID REFERENCES patients(id),
    action          VARCHAR(100) NOT NULL,  -- 'view_record', 'create_prescription', etc.
    resource        VARCHAR(100),           -- which table was accessed
    ip_address      VARCHAR(50),
    user_agent      TEXT,
    accessed_at     TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- INDEXES
-- Improves lookup speed for common searches
-- ============================================================
CREATE INDEX idx_patients_national_id    ON patients(national_id);
CREATE INDEX idx_patients_phone          ON patients(phone);
CREATE INDEX idx_appointments_patient    ON appointments(patient_id);
CREATE INDEX idx_appointments_doctor     ON appointments(doctor_id);
CREATE INDEX idx_appointments_scheduled  ON appointments(scheduled_at);
CREATE INDEX idx_medical_records_patient ON medical_records(patient_id);
CREATE INDEX idx_prescriptions_patient   ON prescriptions(patient_id);
CREATE INDEX idx_audit_logs_doctor       ON audit_logs(doctor_id);
CREATE INDEX idx_audit_logs_patient      ON audit_logs(patient_id);
CREATE INDEX idx_hospitals_county        ON hospitals(county);
CREATE INDEX idx_hospitals_sub_county    ON hospitals(sub_county);
CREATE INDEX idx_hospitals_ownership     ON hospitals(ownership);
CREATE INDEX idx_hospitals_level         ON hospitals(facility_level);


-- ============================================================
-- SEED DATA
-- ============================================================


-- ============================================================
-- HOSPITALS
-- ============================================================
INSERT INTO hospitals (khis_code, name, ownership, facility_level, type, county, sub_county, phone, email) VALUES

-- Nairobi — National referral and county
('13001', 'Kenyatta National Hospital',          'public',      'level_6', 'national_referral_hospital', 'Nairobi',       'Dagoretti North',   '+254202726300',  'info@knh.or.ke'),
('13002', 'Pumwani Maternity Hospital',           'public',      'level_5', 'county_hospital',            'Nairobi',       'Kamukunji',         '+254202210377',  NULL),
('13003', 'Mama Lucy Kibaki Hospital',            'public',      'level_4', 'sub_county_hospital',        'Nairobi',       'Embakasi East',     '+254202002764',  NULL),
('13004', 'Mathare Hospital',                     'public',      'level_4', 'sub_county_hospital',        'Nairobi',       'Mathare',           '+254202623340',  NULL),
('13005', 'Aga Khan University Hospital',         'private',     'level_6', 'specialist_hospital',        'Nairobi',       'Westlands',         '+254203662000',  'info@agakhanhospitals.org'),
('13006', 'MP Shah Hospital',                     'private',     'level_5', 'county_hospital',            'Nairobi',       'Parklands',         '+254204291000',  'info@mpshah.org'),
('13007', 'Nairobi Hospital',                     'private',     'level_5', 'county_hospital',            'Nairobi',       'Upper Hill',        '+254202845000',  'info@nairobihospital.org'),
('13008', 'Karen Hospital',                       'private',     'level_4', 'sub_county_hospital',        'Nairobi',       'Karen',             '+254206613000',  'info@karenhospital.org'),

-- Coast
('14001', 'Coast General Teaching Hospital',      'public',      'level_6', 'national_referral_hospital', 'Mombasa',       'Mombasa Central',   '+254412314201',  NULL),
('14002', 'Port Reitz District Hospital',         'public',      'level_4', 'sub_county_hospital',        'Mombasa',       'Kisauni',           '+254412012345',  NULL),

-- Rift Valley / Uasin Gishu
('22001', 'Moi Teaching and Referral Hospital',   'public',      'level_6', 'national_referral_hospital', 'Uasin Gishu',   'Eldoret CBD',       '+254532033471',  'info@mtrh.go.ke'),
('22002', 'Eldoret Hospital',                     'private',     'level_4', 'sub_county_hospital',        'Uasin Gishu',   'Eldoret CBD',       '+254722205305',  NULL),

-- Kiambu
('16001', 'Kiambu Level 5 Hospital',              'public',      'level_5', 'county_hospital',            'Kiambu',        'Kiambu Town',       '+254667520162',  NULL),
('16002', 'Kikuyu Mission Hospital',              'faith_based', 'level_4', 'sub_county_hospital',        'Kiambu',        'Kikuyu',            '+254720567890',  NULL),
('16003', 'Kijabe Hospital',                      'faith_based', 'level_5', 'county_hospital',            'Kiambu',        'Lari',              '+254205201000',  'info@kijabehospital.org'),

-- Kisumu
('18001', 'Jaramogi Oginga Odinga Teaching Hospital', 'public',  'level_6', 'national_referral_hospital', 'Kisumu',        'Kisumu Central',    '+254572021036',  NULL),
('18002', 'Kisumu County Hospital',               'public',      'level_5', 'county_hospital',            'Kisumu',        'Kisumu East',       '+254572022061',  NULL),

-- Nakuru
('20001', 'Nakuru Level 5 Hospital',              'public',      'level_5', 'county_hospital',            'Nakuru',        'Nakuru Town East',  '+254512212482',  NULL),

-- Kisii
('21001', 'Kisii Teaching and Referral Hospital', 'public',      'level_6', 'national_referral_hospital', 'Kisii',         'Kisii Central',     '+254208000000',  NULL),

-- Machakos
('23001', 'Machakos Level 5 Hospital',            'public',      'level_5', 'county_hospital',            'Machakos',      'Machakos Town',     '+254452020036',  NULL);


-- ============================================================
-- DOCTORS
-- ============================================================
INSERT INTO doctors (hospital_id, full_name, specialisation, licence_number, phone, email, password_hash, role) VALUES

(
    (SELECT id FROM hospitals WHERE khis_code = '13001'),
    'Dr. Amina Odhiambo', 'Internal Medicine', 'KMP-10234',
    '+254711000001', 'amina.odhiambo@knh.or.ke',
    '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae',
    'doctor'
),
(
    (SELECT id FROM hospitals WHERE khis_code = '13001'),
    'James Kariuki', 'Pharmacy', 'KPB-00412',
    '+254711000002', 'james.kariuki@knh.or.ke',
    '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae',
    'pharmacist'
),
(
    (SELECT id FROM hospitals WHERE khis_code = '13005'),
    'Dr. Priya Patel', 'Cardiology', 'KMP-20891',
    '+254711000003', 'priya.patel@agakhanhospitals.org',
    '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae',
    'doctor'
),
(
    (SELECT id FROM hospitals WHERE khis_code = '13006'),
    'Dr. Brian Mwangi', 'General Practice', 'KMP-31045',
    '+254711000004', 'brian.mwangi@mpshah.org',
    '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae',
    'doctor'
),
(
    (SELECT id FROM hospitals WHERE khis_code = '22001'),
    'Dr. Faith Chebet', 'Paediatrics', 'KMP-41230',
    '+254711000005', 'faith.chebet@mtrh.go.ke',
    '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae',
    'doctor'
),
(
    (SELECT id FROM hospitals WHERE khis_code = '14001'),
    'Nurse Grace Akinyi', 'Nursing', NULL,
    '+254711000006', 'grace.akinyi@coastgeneral.go.ke',
    '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae',
    'nurse'
),
(
    (SELECT id FROM hospitals WHERE khis_code = '16003'),
    'Dr. Samuel Njoroge', 'Surgery', 'KMP-52341',
    '+254711000007', 'samuel.njoroge@kijabehospital.org',
    '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae',
    'doctor'
),
(
    (SELECT id FROM hospitals WHERE khis_code = '18001'),
    'Dr. Otieno Omondi', 'Obstetrics and Gynaecology', 'KMP-63452',
    '+254711000008', 'otieno.omondi@jootrh.go.ke',
    '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae',
    'doctor'
),
(
    (SELECT id FROM hospitals WHERE khis_code = '13007'),
    'Dr. Catherine Waweru', 'Dermatology', 'KMP-74563',
    '+254711000009', 'catherine.waweru@nairobihospital.org',
    '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae',
    'doctor'
),
(
    (SELECT id FROM hospitals WHERE khis_code = '13001'),
    'Admin User KNH', NULL, NULL,
    '+254711000010', 'admin@knh.or.ke',
    '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae',
    'admin'
);


-- ============================================================
-- PATIENTS
-- ============================================================
INSERT INTO patients (national_id, full_name, date_of_birth, gender, phone, email, blood_type, allergies, password_hash) VALUES
('12345678', 'Wanjiku Kamau',      '1990-03-14', 'female', '+254722100001', 'wanjiku.kamau@gmail.com',    'O+',  'Penicillin',                  '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae'),
('23456789', 'Otieno Ochieng',     '1985-07-22', 'male',   '+254722100002', 'otieno.ochieng@gmail.com',   'A+',  NULL,                          '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae'),
('34567890', 'Fatuma Hassan',      '1978-11-05', 'female', '+254722100003', 'fatuma.hassan@gmail.com',    'B+',  'Sulfonamides, Aspirin',        '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae'),
('45678901', 'Kipchoge Ruto',      '1995-01-30', 'male',   '+254722100004', 'kipchoge.ruto@gmail.com',    'O-',  NULL,                          '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae'),
('56789012', 'Aisha Mombasa',      '2000-06-18', 'female', '+254722100005', 'aisha.mombasa@gmail.com',    'AB+', 'Ibuprofen',                   '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae'),
('67890123', 'Mwangi Njuguna',     '1972-09-09', 'male',   '+254722100006', 'mwangi.njuguna@gmail.com',   'A-',  'Latex',                       '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae'),
('78901234', 'Chebet Koech',       '1988-04-25', 'female', '+254722100007', 'chebet.koech@gmail.com',     'B-',  NULL,                          '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae'),
('89012345', 'Hassan Abdi',        '1965-12-01', 'male',   '+254722100008', 'hassan.abdi@gmail.com',      'O+',  'Codeine, Morphine',           '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae'),
('90123456', 'Njambi Gicheru',     '1993-08-14', 'female', '+254722100009', 'njambi.gicheru@gmail.com',   'AB-', 'Metronidazole',               '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae'),
('01234567', 'Baraka Mwamba',      '1980-02-28', 'male',   '+254722100010', 'baraka.mwamba@gmail.com',    'A+',  NULL,                          '$2b$12$Mo0Sxw/gHX922Hpze9e1TeyWOrZ6oBiUzxSqT5ly9S49zrZDY.1Ae');