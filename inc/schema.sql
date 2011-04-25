--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: book_raw; Type: TABLE; Schema: public; Owner: david; Tablespace: 
--

CREATE TABLE book_raw (
    book_raw_id integer NOT NULL,
    text text NOT NULL,
    parse_date timestamp without time zone DEFAULT now() NOT NULL,
    category character varying(20) NOT NULL
);


ALTER TABLE public.book_raw OWNER TO david;

--
-- Name: hash; Type: TABLE; Schema: public; Owner: david; Tablespace: 
--

CREATE TABLE hash (
    hash character varying(32) NOT NULL,
    experiment_id smallint NOT NULL,
    class_id smallint NOT NULL,
    count integer NOT NULL,
    text text,
    hash_id integer NOT NULL
);


ALTER TABLE public.hash OWNER TO david;

--
-- Name: hash_hash_id_seq; Type: SEQUENCE; Schema: public; Owner: david
--

CREATE SEQUENCE hash_hash_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hash_hash_id_seq OWNER TO david;

--
-- Name: hash_hash_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: david
--

ALTER SEQUENCE hash_hash_id_seq OWNED BY hash.hash_id;


--
-- Name: hash_id; Type: DEFAULT; Schema: public; Owner: david
--

ALTER TABLE hash ALTER COLUMN hash_id SET DEFAULT nextval('hash_hash_id_seq'::regclass);


--
-- Name: book_raw_pkey; Type: CONSTRAINT; Schema: public; Owner: david; Tablespace: 
--

ALTER TABLE ONLY book_raw
    ADD CONSTRAINT book_raw_pkey PRIMARY KEY (book_raw_id);


--
-- Name: hash_pkey; Type: CONSTRAINT; Schema: public; Owner: david; Tablespace: 
--

ALTER TABLE ONLY hash
    ADD CONSTRAINT hash_pkey PRIMARY KEY (hash_id);


--
-- Name: hash_unique; Type: INDEX; Schema: public; Owner: david; Tablespace: 
--

CREATE UNIQUE INDEX hash_unique ON hash USING btree (hash, experiment_id, class_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

