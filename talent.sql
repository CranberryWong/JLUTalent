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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: articles; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE articles (
    aid integer NOT NULL,
    atitle character varying(60),
    acontent text,
    apubtime timestamp without time zone,
    achgtime timestamp without time zone,
    uaid integer,
    taid integer
);


ALTER TABLE public.articles OWNER TO cheesewong;

--
-- Name: articles_aid_seq; Type: SEQUENCE; Schema: public; Owner: cheesewong
--

CREATE SEQUENCE articles_aid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.articles_aid_seq OWNER TO cheesewong;

--
-- Name: articles_aid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cheesewong
--

ALTER SEQUENCE articles_aid_seq OWNED BY articles.aid;


--
-- Name: cities; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE cities (
    name character varying(80),
    location point
);


ALTER TABLE public.cities OWNER TO cheesewong;

--
-- Name: contacts; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE contacts (
    cid integer NOT NULL,
    cname character varying(35) NOT NULL,
    ccollege character varying(15) NOT NULL,
    ccemail character varying(30) NOT NULL,
    creason text,
    cresume character varying(100)
);


ALTER TABLE public.contacts OWNER TO cheesewong;

--
-- Name: contacts_cid_seq; Type: SEQUENCE; Schema: public; Owner: cheesewong
--

CREATE SEQUENCE contacts_cid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contacts_cid_seq OWNER TO cheesewong;

--
-- Name: contacts_cid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cheesewong
--

ALTER SEQUENCE contacts_cid_seq OWNED BY contacts.cid;


--
-- Name: inform; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE inform (
    iid integer NOT NULL,
    ititle character varying(60),
    iabstract character varying(200),
    iurl character varying(100),
    ipic character varying(100),
    icettime timestamp without time zone,
    ibtnview character varying(25)
);


ALTER TABLE public.inform OWNER TO cheesewong;

--
-- Name: inform_iid_seq; Type: SEQUENCE; Schema: public; Owner: cheesewong
--

CREATE SEQUENCE inform_iid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.inform_iid_seq OWNER TO cheesewong;

--
-- Name: inform_iid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cheesewong
--

ALTER SEQUENCE inform_iid_seq OWNED BY inform.iid;


--
-- Name: limits; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE limits (
    lid integer NOT NULL,
    lname character varying(20),
    lsuper boolean,
    ladmin boolean
);


ALTER TABLE public.limits OWNER TO cheesewong;

--
-- Name: limits_lid_seq; Type: SEQUENCE; Schema: public; Owner: cheesewong
--

CREATE SEQUENCE limits_lid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.limits_lid_seq OWNER TO cheesewong;

--
-- Name: limits_lid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cheesewong
--

ALTER SEQUENCE limits_lid_seq OWNED BY limits.lid;


--
-- Name: links; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE links (
    lkid integer NOT NULL,
    lkname character varying(30) NOT NULL,
    lkurl character varying(100) NOT NULL,
    lkdescribe text
);


ALTER TABLE public.links OWNER TO cheesewong;

--
-- Name: links_lkid_seq; Type: SEQUENCE; Schema: public; Owner: cheesewong
--

CREATE SEQUENCE links_lkid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.links_lkid_seq OWNER TO cheesewong;

--
-- Name: links_lkid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cheesewong
--

ALTER SEQUENCE links_lkid_seq OWNED BY links.lkid;


--
-- Name: meetinfo; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE meetinfo (
    mid integer NOT NULL,
    mtitle character varying(30) NOT NULL,
    mcontent text,
    mcettime timestamp without time zone
);


ALTER TABLE public.meetinfo OWNER TO cheesewong;

--
-- Name: meetinfo_mid_seq; Type: SEQUENCE; Schema: public; Owner: cheesewong
--

CREATE SEQUENCE meetinfo_mid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meetinfo_mid_seq OWNER TO cheesewong;

--
-- Name: meetinfo_mid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cheesewong
--

ALTER SEQUENCE meetinfo_mid_seq OWNED BY meetinfo.mid;


--
-- Name: weather; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE weather (
    city character varying(80),
    temp_lo integer,
    temp_hi integer,
    prcp real,
    date date
);


ALTER TABLE public.weather OWNER TO cheesewong;

--
-- Name: myview; Type: VIEW; Schema: public; Owner: cheesewong
--

CREATE VIEW myview AS
 SELECT weather.city,
    weather.temp_lo,
    weather.temp_hi,
    weather.prcp,
    weather.date,
    cities.location
   FROM weather,
    cities
  WHERE ((weather.city)::text = (cities.name)::text);


ALTER TABLE public.myview OWNER TO cheesewong;

--
-- Name: myview1; Type: VIEW; Schema: public; Owner: cheesewong
--

CREATE VIEW myview1 AS
 SELECT weather.city,
    weather.temp_lo,
    weather.temp_hi,
    weather.prcp,
    weather.date,
    cities.location
   FROM weather,
    cities
  WHERE ((weather.city)::text = (cities.name)::text);


ALTER TABLE public.myview1 OWNER TO cheesewong;

--
-- Name: news; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE news (
    nid integer NOT NULL,
    ntitle character varying(60),
    ncontent text,
    npubtime timestamp without time zone,
    nchgtime timestamp without time zone
);


ALTER TABLE public.news OWNER TO cheesewong;

--
-- Name: news_nid_seq; Type: SEQUENCE; Schema: public; Owner: cheesewong
--

CREATE SEQUENCE news_nid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.news_nid_seq OWNER TO cheesewong;

--
-- Name: news_nid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cheesewong
--

ALTER SEQUENCE news_nid_seq OWNED BY news.nid;


--
-- Name: pages; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE pages (
    pid integer NOT NULL,
    ptitle character varying(60) NOT NULL,
    pcontent text,
    ppubtime timestamp without time zone,
    pchgtime timestamp without time zone,
    ppic character varying(100)
);


ALTER TABLE public.pages OWNER TO cheesewong;

--
-- Name: pages_pid_seq; Type: SEQUENCE; Schema: public; Owner: cheesewong
--

CREATE SEQUENCE pages_pid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pages_pid_seq OWNER TO cheesewong;

--
-- Name: pages_pid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cheesewong
--

ALTER SEQUENCE pages_pid_seq OWNED BY pages.pid;


--
-- Name: types; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE types (
    tid integer NOT NULL,
    typename character varying(10) NOT NULL
);


ALTER TABLE public.types OWNER TO cheesewong;

--
-- Name: types_tid_seq; Type: SEQUENCE; Schema: public; Owner: cheesewong
--

CREATE SEQUENCE types_tid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.types_tid_seq OWNER TO cheesewong;

--
-- Name: types_tid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cheesewong
--

ALTER SEQUENCE types_tid_seq OWNED BY types.tid;


--
-- Name: upload; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE upload (
    fileid integer NOT NULL,
    filename character varying(50) NOT NULL,
    cettime timestamp without time zone,
    fileurl character varying(100) NOT NULL
);


ALTER TABLE public.upload OWNER TO cheesewong;

--
-- Name: upload_fileid_seq; Type: SEQUENCE; Schema: public; Owner: cheesewong
--

CREATE SEQUENCE upload_fileid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.upload_fileid_seq OWNER TO cheesewong;

--
-- Name: upload_fileid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cheesewong
--

ALTER SEQUENCE upload_fileid_seq OWNED BY upload.fileid;


--
-- Name: users; Type: TABLE; Schema: public; Owner: cheesewong; Tablespace: 
--

CREATE TABLE users (
    uid integer NOT NULL,
    username character varying(35),
    password character varying(35),
    uemail character varying(30),
    ubio text,
    ucheck boolean,
    ucollege character varying(30),
    ugrade character varying(10),
    udomain text,
    uavatar character varying(100),
    luid integer
);


ALTER TABLE public.users OWNER TO cheesewong;

--
-- Name: users_uid_seq; Type: SEQUENCE; Schema: public; Owner: cheesewong
--

CREATE SEQUENCE users_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_uid_seq OWNER TO cheesewong;

--
-- Name: users_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cheesewong
--

ALTER SEQUENCE users_uid_seq OWNED BY users.uid;


--
-- Name: aid; Type: DEFAULT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY articles ALTER COLUMN aid SET DEFAULT nextval('articles_aid_seq'::regclass);


--
-- Name: cid; Type: DEFAULT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY contacts ALTER COLUMN cid SET DEFAULT nextval('contacts_cid_seq'::regclass);


--
-- Name: iid; Type: DEFAULT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY inform ALTER COLUMN iid SET DEFAULT nextval('inform_iid_seq'::regclass);


--
-- Name: lid; Type: DEFAULT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY limits ALTER COLUMN lid SET DEFAULT nextval('limits_lid_seq'::regclass);


--
-- Name: lkid; Type: DEFAULT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY links ALTER COLUMN lkid SET DEFAULT nextval('links_lkid_seq'::regclass);


--
-- Name: mid; Type: DEFAULT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY meetinfo ALTER COLUMN mid SET DEFAULT nextval('meetinfo_mid_seq'::regclass);


--
-- Name: nid; Type: DEFAULT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY news ALTER COLUMN nid SET DEFAULT nextval('news_nid_seq'::regclass);


--
-- Name: pid; Type: DEFAULT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY pages ALTER COLUMN pid SET DEFAULT nextval('pages_pid_seq'::regclass);


--
-- Name: tid; Type: DEFAULT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY types ALTER COLUMN tid SET DEFAULT nextval('types_tid_seq'::regclass);


--
-- Name: fileid; Type: DEFAULT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY upload ALTER COLUMN fileid SET DEFAULT nextval('upload_fileid_seq'::regclass);


--
-- Name: uid; Type: DEFAULT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY users ALTER COLUMN uid SET DEFAULT nextval('users_uid_seq'::regclass);


--
-- Data for Name: articles; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY articles (aid, atitle, acontent, apubtime, achgtime, uaid, taid) FROM stdin;
2	第一篇	第一篇	2015-01-10 13:43:27.507587	2015-01-10 13:43:27.507809	1	1
3	第一篇	第二篇	2015-01-10 17:57:18.243303	2015-01-10 17:57:18.243492	1	1
4	第一篇	这是第一篇日志	2015-01-10 17:58:41.720047	2015-01-10 17:58:41.720065	1	1
9	I'm Fine	这是一个不能停留太久的世界啊a	2015-03-29 16:36:44.028328	2015-03-29 16:41:11.160314	5	1
10	test	<blockquote><p><br></p><p><a href="http://www.baidu.com" target="_blank">对Simditor的test</a></p><p><img alt="Image"><br></p><p><br></p></blockquote>	2015-05-22 13:15:19.630295	2015-05-22 13:15:19.630311	5	5
11	lalal	<p><img alt="3257f6a645cf4613f4eabda693d31fed_b.jpg.png" src="/static/articles/3257f6a645cf4613f4eabda693d31fed_b1432301264.jpg" data-image-size="375,375"><br></p><p>asdasdasd</p><p><img alt="4790141153661978147.jpg" src="/static/articles/47901411536619781471432301312.jpg" data-image-size="300,455"><br></p>	2015-05-22 21:08:05.023054	2015-05-22 21:28:34.113947	5	5
12	这是马克的第一篇文章	<p>asdasd</p><p><img alt="安卓壁纸_其他54d89312aa.jpg" src="/static/articles/安卓壁纸_其他54d89312aa1435470527.jpg" width="300" height="250"><br></p>	2015-06-28 13:48:52.851193	2015-06-28 15:19:29.619721	12	3
\.


--
-- Name: articles_aid_seq; Type: SEQUENCE SET; Schema: public; Owner: cheesewong
--

SELECT pg_catalog.setval('articles_aid_seq', 12, true);


--
-- Data for Name: cities; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY cities (name, location) FROM stdin;
san francisco	(-194,53)
\.


--
-- Data for Name: contacts; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY contacts (cid, cname, ccollege, ccemail, creason, cresume) FROM stdin;
7	wangchen	jiin university	i@wangchen0413.cn	like	/static/resume/王晨_产品实习11427184471.pdf
8	wangchen	JLU	i@wangchen0413.cn	like	/static/resume/王晨_产品实习11427969477.pdf
\.


--
-- Name: contacts_cid_seq; Type: SEQUENCE SET; Schema: public; Owner: cheesewong
--

SELECT pg_catalog.setval('contacts_cid_seq', 8, true);


--
-- Data for Name: inform; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY inform (iid, ititle, iabstract, iurl, ipic, icettime, ibtnview) FROM stdin;
2	Social Computing Group	Social Computing Group即将上线，快来参与测试吧:)		/static/inform/OS_X_Mavericks041425112520.jpg	2015-02-28 16:35:20.745368	Sign up
4	Web Design开课了！！	第一至十周，每周四，经信六阶，晚上6:30至8:50		/static/inform/slide11425272314.jpg	2015-03-02 12:58:34.44956	View Detail
1	Web Design开课了！！	第一至十周，每周四，经信六阶，晚上6:30至8:50		/static/inform/slide11425112225.jpg	2015-02-28 16:30:25.34993	View Detail
3	《大数据技术与应用》开课啦！！	每周二下午13：30——16：30，计算机楼A135，欢迎没有其他课程的同学们参加！全团队教师倾力打造，也是团队内部的一次培训课程。		/static/inform/Win101425112653.jpg	2015-02-28 16:37:33.663255	Let's go
\.


--
-- Name: inform_iid_seq; Type: SEQUENCE SET; Schema: public; Owner: cheesewong
--

SELECT pg_catalog.setval('inform_iid_seq', 4, true);


--
-- Data for Name: limits; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY limits (lid, lname, lsuper, ladmin) FROM stdin;
1	anonymous	f	f
2	admin	f	t
3	superadmin	t	t
\.


--
-- Name: limits_lid_seq; Type: SEQUENCE SET; Schema: public; Owner: cheesewong
--

SELECT pg_catalog.setval('limits_lid_seq', 3, true);


--
-- Data for Name: links; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY links (lkid, lkname, lkurl, lkdescribe) FROM stdin;
1	Github	http://www.github.com	our repository
\.


--
-- Name: links_lkid_seq; Type: SEQUENCE SET; Schema: public; Owner: cheesewong
--

SELECT pg_catalog.setval('links_lkid_seq', 1, true);


--
-- Data for Name: meetinfo; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY meetinfo (mid, mtitle, mcontent, mcettime) FROM stdin;
\.


--
-- Name: meetinfo_mid_seq; Type: SEQUENCE SET; Schema: public; Owner: cheesewong
--

SELECT pg_catalog.setval('meetinfo_mid_seq', 2, true);


--
-- Data for Name: news; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY news (nid, ntitle, ncontent, npubtime, nchgtime) FROM stdin;
\.


--
-- Name: news_nid_seq; Type: SEQUENCE SET; Schema: public; Owner: cheesewong
--

SELECT pg_catalog.setval('news_nid_seq', 1, false);


--
-- Data for Name: pages; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY pages (pid, ptitle, pcontent, ppubtime, pchgtime, ppic) FROM stdin;
3	Web Design	Web design encompasses many different skills and disciplines in the production and maintenance of websites. The different areas of web design include web graphic design; interface design; authoring, including standardised code and proprietary software; user experience design; and search engine optimization. Often many individuals will work in teams covering different aspects of the design process, although some designers will cover them all.[1] The term web design is normally used to describe the design process relating to the front-end (client side) design of a website including writing mark up. Web design partially overlaps web engineering in the broader scope of web development. Web designers are expected to have an awareness of usability and if their role involves creating mark up then they are also expected to be up to date with web accessibility guidelines.	2015-02-25 13:55:50.396471	2015-02-25 13:55:50.396488	\N
1	OPEN DATA	Open data is the idea that certain data should be freely available to everyone to use and republish as they wish, without restrictions from copyright, patentsor other mechanisms of control.[1] The goals of the open data movement are similar to those of other “Open” movements such as open source, open hardware, open content, and open access. The philosophy behind open data has been long established (for example in the Mertonian tradition of science), but the term “open data” itself is recent, gaining popularity with the rise of the Internet and World Wide Web and, especially, with the launch of open-data government initiatives such as Data.gov and Data.gov.uk.	2015-01-14 20:31:33.786131	2015-01-14 20:31:33.786151	\N
2	Gamification	Gamification is the use of game thinking and game mechanics[1] in non-game contexts to engage users in solving problems[2] and increase users’ self contributions.[3][4] Gamification has been studied and applied in several domains, with some of the main purposes being to engage (improve user engagement,[5] physical exercise,[6] return on investment, flow,[7][8] data quality, timeliness), teach (in classrooms, the public or at work[9]), entertain (enjoyment,[8] fan loyalty), measure[10] (for recruiting and employee evaluation), and to improve the perceived ease of use of information systems.[8][11] A review of research on gamification shows that a majority of studies on gamification find positive effects from gamification.[12] However, individual and contextual differences exist.	2015-02-25 13:54:25.413576	2015-03-29 18:05:49.694744	\N
7	test	This is a test page	2015-03-30 11:44:52.168066	2015-03-30 11:45:09.102702	/static/page/2015-01-09_18-38-491427687109.jpeg
\.


--
-- Name: pages_pid_seq; Type: SEQUENCE SET; Schema: public; Owner: cheesewong
--

SELECT pg_catalog.setval('pages_pid_seq', 7, true);


--
-- Data for Name: types; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY types (tid, typename) FROM stdin;
3	Algorithm
1	Design
4	Reading
5	Business
\.


--
-- Name: types_tid_seq; Type: SEQUENCE SET; Schema: public; Owner: cheesewong
--

SELECT pg_catalog.setval('types_tid_seq', 5, true);


--
-- Data for Name: upload; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY upload (fileid, filename, cettime, fileurl) FROM stdin;
1	66_100531094458_11421667298.jpg	2015-01-19 19:34:58.784017	/static/uploadfile/66_100531094458_11421667298.jpg
2	66_100531094458_11421669955.jpg	2015-01-19 20:19:15.415637	/Users/cheesewong/PycharmProjects/simple/cms/static/uploadfile/66_100531094458_11421669955.jpg
3	37A3893D@102BC5181421730171.E1125254	2015-01-20 13:02:52.015378	/Users/cheesewong/PycharmProjects/simple/cms/static/uploadfile/37A3893D@102BC5181421730171.E1125254
4	37A3893D@102BC5181421730636.E1125254	2015-01-20 13:10:36.716164	/Users/cheesewong/PycharmProjects/simple/cms/static/uploadfile/37A3893D@102BC5181421730636.E1125254
7	UDP程序.zip	2015-05-23 17:58:52.795101	/static/addon/UDP程序.zip
\.


--
-- Name: upload_fileid_seq; Type: SEQUENCE SET; Schema: public; Owner: cheesewong
--

SELECT pg_catalog.setval('upload_fileid_seq', 7, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY users (uid, username, password, uemail, ubio, ucheck, ucollege, ugrade, udomain, uavatar, luid) FROM stdin;
9	wwwwww	cb42e130d1471239a27fca6228094f0e	1102868398@qq.com		f					1
10	aaron	d4224c42dffa50efe85544c28f0c2e1c	heycheesecheese@gmail.com		f	Jilin University	2		/static/images/avatar-10.svg	1
11	pipi	202cb962ac59075b964b07152d234b70	1102868398@qq.com		f				/static/images/avatar-5.svg	1
13	sandburg	d4224c42dffa50efe85544c28f0c2e1c	i@wangchen0413.cn		t				/static/images/avatar-11.svg	1
14	王	7815696ecbf1c96e6894b779456d330e	i@wangchen0413.cn		f				/static/images/avatar-2.svg	1
15	wad	202cb962ac59075b964b07152d234b70	i@wangchen0413.cn		f				/static/images/avatar-2.svg	1
16	aaa	47bce5c74f589f4867dbd57e9ca9f808	1@2.x		f				/static/images/avatar-13.svg	1
5	wangchen	d4224c42dffa50efe85544c28f0c2e1c	i@wangchen0413.cn	lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man lazy man	t	Jilin University	Master	NLP	/static/avatar/3257f6a645cf4613f4eabda693d31fed_b1432275116.jpg	3
12	Mark Zuckerberg	d4224c42dffa50efe85544c28f0c2e1c	i@wangchen0413.cn		t				/static/images/avatar-9.svg	2
2	Aaron	psw	\N	在在在在在在在在在在在在在在在在在在在在在在在在在在在在	f	\N	Professor	\N	/static/images/avatar-07.svg	1
4	chen	a1a8887793acfc199182a649e905daab	\N	ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd	t	\N	Ph.D	\N	/static/images/avatar-01.svg	1
8	LiZhuang	202cb962ac59075b964b07152d234b70	i@q.c		t				/static/images/avatar-2.svg	1
7	BerryWong	d4224c42dffa50efe85544c28f0c2e1c	i@imchen.wang	i'm busy	f	CS	Master	Design	/static/images/avatar-9.svg	1
6	Cranberry	d4224c42dffa50efe85544c28f0c2e1c	523259548@qq.com		f				/static/avatar/IMG_02151426829603.JPG	1
3	username	psw	\N	cccccccccccccc	t	\N	Bachelor	\N	/static/images/avatar-10.svg	3
1	wang	a1a8887793acfc199182a649e905daab	\N	aaaaaaaaaaaaa	t		Guest Prof		/static/images/avatar-11.svg	2
\.


--
-- Name: users_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: cheesewong
--

SELECT pg_catalog.setval('users_uid_seq', 16, true);


--
-- Data for Name: weather; Type: TABLE DATA; Schema: public; Owner: cheesewong
--

COPY weather (city, temp_lo, temp_hi, prcp, date) FROM stdin;
san francisco	46	50	0.25	1994-11-27
hayward	37	54	0	1994-11-29
\.


--
-- Name: articles_pkey; Type: CONSTRAINT; Schema: public; Owner: cheesewong; Tablespace: 
--

ALTER TABLE ONLY articles
    ADD CONSTRAINT articles_pkey PRIMARY KEY (aid);


--
-- Name: contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: cheesewong; Tablespace: 
--

ALTER TABLE ONLY contacts
    ADD CONSTRAINT contacts_pkey PRIMARY KEY (cid);


--
-- Name: links_pkey; Type: CONSTRAINT; Schema: public; Owner: cheesewong; Tablespace: 
--

ALTER TABLE ONLY links
    ADD CONSTRAINT links_pkey PRIMARY KEY (lkid);


--
-- Name: meetinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: cheesewong; Tablespace: 
--

ALTER TABLE ONLY meetinfo
    ADD CONSTRAINT meetinfo_pkey PRIMARY KEY (mid);


--
-- Name: news_pkey; Type: CONSTRAINT; Schema: public; Owner: cheesewong; Tablespace: 
--

ALTER TABLE ONLY news
    ADD CONSTRAINT news_pkey PRIMARY KEY (nid);


--
-- Name: pages_pkey; Type: CONSTRAINT; Schema: public; Owner: cheesewong; Tablespace: 
--

ALTER TABLE ONLY pages
    ADD CONSTRAINT pages_pkey PRIMARY KEY (pid);


--
-- Name: pk_limits_users_no; Type: CONSTRAINT; Schema: public; Owner: cheesewong; Tablespace: 
--

ALTER TABLE ONLY limits
    ADD CONSTRAINT pk_limits_users_no PRIMARY KEY (lid);


--
-- Name: types_pkey; Type: CONSTRAINT; Schema: public; Owner: cheesewong; Tablespace: 
--

ALTER TABLE ONLY types
    ADD CONSTRAINT types_pkey PRIMARY KEY (tid);


--
-- Name: upload_pkey; Type: CONSTRAINT; Schema: public; Owner: cheesewong; Tablespace: 
--

ALTER TABLE ONLY upload
    ADD CONSTRAINT upload_pkey PRIMARY KEY (fileid);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: cheesewong; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uid);


--
-- Name: arti_type_fork; Type: FK CONSTRAINT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY articles
    ADD CONSTRAINT arti_type_fork FOREIGN KEY (taid) REFERENCES types(tid);


--
-- Name: articles_uaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY articles
    ADD CONSTRAINT articles_uaid_fkey FOREIGN KEY (uaid) REFERENCES users(uid);


--
-- Name: fk_limits; Type: FK CONSTRAINT; Schema: public; Owner: cheesewong
--

ALTER TABLE ONLY users
    ADD CONSTRAINT fk_limits FOREIGN KEY (luid) REFERENCES limits(lid);


--
-- Name: public; Type: ACL; Schema: -; Owner: cheesewong
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM cheesewong;
GRANT ALL ON SCHEMA public TO cheesewong;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

