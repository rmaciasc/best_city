CREATE DATABASE metabaseappdb;
CREATE SCHEMA IF NOT EXISTS "raw";
CREATE SCHEMA IF NOT EXISTS staging;
CREATE TABLE IF NOT EXISTS "raw".submissions (
    submission_id character varying(7) COLLATE pg_catalog."default" NOT NULL,
    subreddit character varying(100) COLLATE pg_catalog."default" NOT NULL,
    date_utc date NOT NULL,
    title character varying(300) COLLATE pg_catalog."default" NOT NULL,
    upvote_ratio numeric(3, 0) NOT NULL,
    CONSTRAINT submissions_pkey PRIMARY KEY (submission_id)
);
CREATE TABLE IF NOT EXISTS "raw".comments (
    submission_id character varying(7) COLLATE pg_catalog."default" NOT NULL,
    comment_id character varying(7) COLLATE pg_catalog."default" NOT NULL,
    comment_tier character varying(7) COLLATE pg_catalog."default" NOT NULL,
    parent_id character varying(7) COLLATE pg_catalog."default" NOT NULL,
    date_utc date NOT NULL,
    comment character varying(30000) COLLATE pg_catalog."default" NOT NULL,
    is_moderator boolean NOT NULL,
    is_author boolean NOT NULL,
    score integer NOT NULL,
    CONSTRAINT comments_pkey PRIMARY KEY (comment_id),
    CONSTRAINT submissions_submission_id_fk FOREIGN KEY (submission_id) REFERENCES "raw".submissions (submission_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS staging.submissions (
    submission_id character varying(7) COLLATE pg_catalog."default" NOT NULL,
    subreddit character varying(100) COLLATE pg_catalog."default" NOT NULL,
    date_utc date NOT NULL,
    title character varying(300) COLLATE pg_catalog."default" NOT NULL,
    upvote_ratio numeric(3, 0) NOT NULL,
    title_sentiment numeric(3, 0) NOT NULL,
    CONSTRAINT submissions_pkey PRIMARY KEY (submission_id)
);
CREATE TABLE IF NOT EXISTS "raw".jobs (
    date_utc date NOT NULL,
    keyword character varying(30) COLLATE pg_catalog."default" NOT NULL,
    city character varying(20) COLLATE pg_catalog."default" NOT NULL,
    jobs_qty integer NOT NULL
);
CREATE TABLE IF NOT EXISTS staging.comments (
    submission_id character varying(7) COLLATE pg_catalog."default" NOT NULL,
    comment_id character varying(7) COLLATE pg_catalog."default" NOT NULL,
    comment_tier character varying(7) COLLATE pg_catalog."default" NOT NULL,
    parent_id character varying(7) COLLATE pg_catalog."default" NOT NULL,
    date_utc date NOT NULL,
    comment character varying(30000) COLLATE pg_catalog."default" NOT NULL,
    is_author boolean NOT NULL,
    score double precision NOT NULL,
    comment_sentiment numeric NOT NULL,
    bad_words character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT comments_pkey PRIMARY KEY (comment_id),
    CONSTRAINT submissions_submission_id_fk FOREIGN KEY (submission_id) REFERENCES staging.submissions (submission_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS staging.jobs (
    date_utc date NOT NULL,
    keyword character varying(30) COLLATE pg_catalog."default" NOT NULL,
    city character varying(20) COLLATE pg_catalog."default" NOT NULL,
    jobs_qty integer NOT NULL
);