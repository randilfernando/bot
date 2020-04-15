CREATE TABLE public.response
(
  id       serial PRIMARY KEY NOT NULL,
  intent   TEXT               NOT NULL,
  response TEXT
);
CREATE UNIQUE INDEX response_id_uindex
  ON public.response (id);
CREATE UNIQUE INDEX response_intent_uindex
  ON public.response (intent);