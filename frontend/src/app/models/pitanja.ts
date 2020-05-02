export interface User {
  email: string;
  firstName: string;
  lastName: string;
}

export interface Ucenik extends User {
  id: number;
  skola: number;
  token: string;
}

export interface Odgovor {
  id: number;
  redni_broj: number;
  tekst: string;
}

export interface Pitanje {
  id: number;
  redni_broj: number;
  tip: string;
  tekst: string;
  odgovor_set: Odgovor[];
}

export interface Test {
  id: number;
  naziv: string;
  datum_vazenja: Date;
  pitanje_set?: Pitanje[];
}

export interface OdgovorUcenika {
  id: number;
  test_ucenika: number;
  pitanje: number;
  odgovor: string;
}

export interface TestUcenika {
  test_ucenika: number;
  odgovori?: OdgovorUcenika[];
}

