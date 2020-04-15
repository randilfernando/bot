CREATE TABLE public.responses
(
  id       serial PRIMARY KEY NOT NULL,
  intent   TEXT               NOT NULL,
  response TEXT
);

CREATE UNIQUE INDEX responses_intent_uindex
  ON public.responses (intent);