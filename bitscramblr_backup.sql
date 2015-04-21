--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: nodes; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE nodes (
    id integer NOT NULL,
    address character varying,
    label character varying,
    role character varying,
    status character varying,
    balance double precision,
    used boolean,
    destination character varying,
    parent character varying,
    origin character varying,
    pending_amt double precision
);


--
-- Name: nodes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE nodes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: nodes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE nodes_id_seq OWNED BY nodes.id;


--
-- Name: txs; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE txs (
    id integer NOT NULL,
    parent character varying,
    destination character varying,
    amount double precision,
    received_inputs boolean,
    outputs_sent boolean,
    origin character varying,
    tx_hash character varying
);


--
-- Name: txs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE txs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: txs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE txs_id_seq OWNED BY txs.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY nodes ALTER COLUMN id SET DEFAULT nextval('nodes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY txs ALTER COLUMN id SET DEFAULT nextval('txs_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY alembic_version (version_num) FROM stdin;
45eae38bccea
\.


--
-- Data for Name: nodes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY nodes (id, address, label, role, status, balance, used, destination, parent, origin, pending_amt) FROM stdin;
2	18DawQ5KuahRm3gAUXrCsq7dN6Vf5oCtdT	SHUFFLING	shuffling	fresh	0.00197999999999999999	f	\N	17sAW4h4K65HAKSCauuQMpdKXsgGHBbz8P	1EqNq5nsMCH8rKWwvLzpbAXGVj2FeJjbiV	\N
3	1HJD7yY4EEid6LrLJMWSbNjx8zY2sb7eTL	SHUFFLING	shuffling	fresh	0.00197999999999999999	f	\N	17sAW4h4K65HAKSCauuQMpdKXsgGHBbz8P	1EqNq5nsMCH8rKWwvLzpbAXGVj2FeJjbiV	\N
4	1Mo4QkwoL85C8sY453KDFFCGm6qsGo9BgL	SHUFFLING	shuffling	fresh	0.00197999999999999999	f	\N	17sAW4h4K65HAKSCauuQMpdKXsgGHBbz8P	1EqNq5nsMCH8rKWwvLzpbAXGVj2FeJjbiV	\N
5	18v7oEE1goiTrCGeTkXcyvWVgkgNbZqBrL	SHUFFLING	shuffling	fresh	0.00197999999999999999	f	\N	17sAW4h4K65HAKSCauuQMpdKXsgGHBbz8P	1EqNq5nsMCH8rKWwvLzpbAXGVj2FeJjbiV	\N
6	1HSksroDsatpBbo4tgUniDo8h1N112wDqK	SHUFFLING	shuffling	fresh	0.00197999999999999999	f	\N	17sAW4h4K65HAKSCauuQMpdKXsgGHBbz8P	1EqNq5nsMCH8rKWwvLzpbAXGVj2FeJjbiV	\N
\.


--
-- Name: nodes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('nodes_id_seq', 11, true);


--
-- Data for Name: txs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY txs (id, parent, destination, amount, received_inputs, outputs_sent, origin, tx_hash) FROM stdin;
2	1AYth7c8BistgQRLV9cfWtLUmFRBkGw3L4	1GbAg3ULXaXQJQpLDP9zQxHfDWmDxrwfBo	0.0200000000000000004	t	f	1HasACSXrKs42u9ySoSEDRNSCHRSWPpYWT	\N
1	17sAW4h4K65HAKSCauuQMpdKXsgGHBbz8P	1GbAg3ULXaXQJQpLDP9zQxHfDWmDxrwfBo	0.0100000000000000002	t	t	1EqNq5nsMCH8rKWwvLzpbAXGVj2FeJjbiV	\N
\.


--
-- Name: txs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('txs_id_seq', 2, true);


--
-- Name: nodes_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY nodes
    ADD CONSTRAINT nodes_pkey PRIMARY KEY (id);


--
-- Name: txs_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY txs
    ADD CONSTRAINT txs_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM ehickox2012;
GRANT ALL ON SCHEMA public TO ehickox2012;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

