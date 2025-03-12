--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-03-09 23:27:06

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 32773)
-- Name: categories; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.categories (
    category text,
    category_id bigint
);


ALTER TABLE public.categories OWNER TO neondb_owner;

--
-- TOC entry 217 (class 1259 OID 32768)
-- Name: customers; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.customers (
    customer_id text,
    gender text,
    age bigint,
    name text
);


ALTER TABLE public.customers OWNER TO neondb_owner;

--
-- TOC entry 219 (class 1259 OID 32778)
-- Name: payment_methods; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.payment_methods (
    payment_method text,
    payment_id bigint
);


ALTER TABLE public.payment_methods OWNER TO neondb_owner;

--
-- TOC entry 221 (class 1259 OID 32788)
-- Name: sales; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.sales (
    invoice_no text,
    customer_id text,
    category_id bigint,
    quantity bigint,
    price double precision,
    payment_id bigint,
    invoice_date timestamp without time zone,
    mall_id bigint
);


ALTER TABLE public.sales OWNER TO neondb_owner;

--
-- TOC entry 220 (class 1259 OID 32783)
-- Name: shopping_malls; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.shopping_malls (
    shopping_mall text,
    mall_id bigint
);


ALTER TABLE public.shopping_malls OWNER TO neondb_owner;

--
-- TOC entry 2060 (class 826 OID 16392)
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- TOC entry 2059 (class 826 OID 16391)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON TABLES TO neon_superuser WITH GRANT OPTION;


-- Completed on 2025-03-09 23:27:12

--
-- PostgreSQL database dump complete
--

