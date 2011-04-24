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
    count integer NOT NULL
);


ALTER TABLE public.hash OWNER TO david;

--
-- Name: book_raw_pkey; Type: CONSTRAINT; Schema: public; Owner: david; Tablespace: 
--

ALTER TABLE ONLY book_raw
    ADD CONSTRAINT book_raw_pkey PRIMARY KEY (book_raw_id);


--
-- Name: hash_pkey; Type: CONSTRAINT; Schema: public; Owner: david; Tablespace: 
--

ALTER TABLE ONLY hash
    ADD CONSTRAINT hash_pkey PRIMARY KEY (experiment_id, hash, class_id);


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

