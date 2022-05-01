-- DROP SCHEMA boook_review;

CREATE SCHEMA boook_review AUTHORIZATION postgres;
-- boook_review."user" definition

-- Drop table

-- DROP TABLE boook_review."user";

CREATE TABLE boook_review."user" (
	id varchar(50) NOT NULL,
	full_name varchar(50) NOT NULL,
	email varchar(100) NOT NULL,
	"password" varchar(30) NOT NULL,
	dob timestamp NULL,
	created_by varchar(30) NOT NULL,
	creation_dttm timestamp NOT NULL,
	modified_by varchar(30) NOT NULL,
	modification_dttm timestamp NOT NULL,
	"version" numeric(5) NOT NULL,
	status bpchar(3) NOT NULL,
	verification_token varchar(30) NOT NULL,
	CONSTRAINT user_pk PRIMARY KEY (id)
);


-- boook_review.book definition

-- Drop table

-- DROP TABLE boook_review.book;

CREATE TABLE boook_review.book (
	id varchar(50) NOT NULL,
	"name" varchar(100) NOT NULL,
	description varchar(300) NULL,
	author varchar(50) NOT NULL,
	ratting int4 NOT NULL,
	created_by varchar(50) NOT NULL,
	creation_dttm timestamp NOT NULL,
	modified_by varchar(50) NOT NULL,
	modification_dttm timestamp NOT NULL,
	"version" numeric(5) NOT NULL,
	CONSTRAINT book_pk PRIMARY KEY (id),
	CONSTRAINT book_fk FOREIGN KEY (created_by) REFERENCES boook_review."user"(id),
	CONSTRAINT book_fk_1 FOREIGN KEY (modified_by) REFERENCES boook_review."user"(id)
);


-- boook_review.user_book definition

-- Drop table

-- DROP TABLE boook_review.user_book;

CREATE TABLE boook_review.user_book (
	user_id varchar(50) NOT NULL,
	book_id varchar(50) NOT NULL,
	ratting int4 NOT NULL,
	created_by varchar(50) NOT NULL,
	creation_dttm timestamp NOT NULL,
	modified_by varchar(50) NOT NULL,
	modification_dttm timestamp NOT NULL,
	"version" numeric(5) NOT NULL,
	CONSTRAINT user_book_pk PRIMARY KEY (user_id, book_id),
	CONSTRAINT user_book_fk FOREIGN KEY (user_id) REFERENCES boook_review."user"(id),
	CONSTRAINT user_book_fk_1 FOREIGN KEY (book_id) REFERENCES boook_review.book(id),
	CONSTRAINT user_book_fk_2 FOREIGN KEY (created_by) REFERENCES boook_review."user"(id),
	CONSTRAINT user_book_fk_3 FOREIGN KEY (modified_by) REFERENCES boook_review."user"(id)
);
