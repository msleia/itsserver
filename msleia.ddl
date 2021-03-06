create table SWORDS (
    id SERIAL PRIMARY KEY,
    userid TEXT,
    name TEXT,
    type TEXT,
    description TEXT,
    clues TEXT
);

create table FC_MASTER (
    id SERIAL PRIMARY KEY,
    userid TEXT,
    name TEXT,
    description TEXT
);

create table FC_WORDS (
    id SERIAL PRIMARY KEY,
    userid TEXT,
    flash_card_id INTEGER,
    sw_id INTEGER,
    od INTEGER
);

create table WORD_REPORT (
    id SERIAL PRIMARY KEY,
    userid TEXT,
    sw_id INTEGER,
    is_identified INTEGER
);
create table USER_PROF (
    id SERIAL PRIMARY KEY,
    name TEXT
);
create table FC_REPORT (
    id SERIAL PRIMARY KEY,
    userid TEXT,
    flash_card_id INTEGER,
    last_accessed TIMESTAMP DEFAULT NOW(),
    is_completed INTEGER
);

create table sent_repo (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);

create table sent_course (
    id SERIAL PRIMARY KEY,
    sent_card_id INTEGER,
    sent_id INTEGER,
    userid TEXT
);

create table sent_card (
    id SERIAL PRIMARY KEY,
    userid TEXT,
    name TEXT,
    description TEXT,
    is_completed INTEGER
);

create table reward (
    id SERIAL PRIMARY KEY,
    userid TEXT,
    message TEXT,
    exercise_count INTEGER,
    status INTEGER
);

create table exercise_report (
    id SERIAL PRIMARY KEY,
    userid TEXT,
    course_name TEXT,
    reward_qualified INTEGER,
    rewarded INTEGER,
    is_completed INTEGER
);

create table enc_msg (
    id SERIAL PRIMARY KEY,
    message TEXT
)