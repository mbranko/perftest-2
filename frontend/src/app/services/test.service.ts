import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { OdgovorUcenika, Pitanje, Test, TestUcenika } from '../models';

@Injectable({
  providedIn: 'root'
})
export class TestService {

  test: Test;

  constructor(private http: HttpClient) { }

  getTests(): Observable<Test[]> {
    return this.http.get<Test[]>('/api/testovi/');
  }

  getTest(id: number): Observable<Test> {
    return this.http.get<Test>(`/api/testovi/${id}/`);
  }

  fetchTest(id: number): Observable<Test> {
    if (this.test !== undefined) {
      return of(this.test);
    } else {
      return this.http.get<Test>(`/api/komplet-test/${id}/`);
    }
  }

  setTest(test: Test): void {
    this.test = test;
    this.test.pitanje_set.sort((a: Pitanje, b: Pitanje): number => {
        if (a.redni_broj < b.redni_broj) { return -1; }
        if (a.redni_broj > b.redni_broj) { return 1; }
        return 0;
      });
  }

  zapocniTest(id: number): Observable<TestUcenika> {
    return this.http.post<TestUcenika>(`/api/pocetak/`, { test: id });
  }

  posaljiOdgovor(testUcenika: number, pitanjeId: number, odgovor: string): Observable<any> {
    return this.http.post<any>(`/api/odgovor/`, {test_ucenika: testUcenika, pitanje: pitanjeId, odgovor});
  }

  getRezime(testUcenika: number): Observable<OdgovorUcenika[]> {
    return this.http.get<OdgovorUcenika[]>(`/api/rezime/${testUcenika}/`);
  }

  zavrsiTest(testUcenika: number): Observable<any> {
    return this.http.post<any>(`/api/kraj/`, {test_ucenika: testUcenika});
  }
}
