import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { Ucenik } from '../models';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class JwtService {

  ucenik: Ucenik = null;
  private ucenikLoggedInSource = new Subject<Ucenik>();
  ucenikLoggedIn = this.ucenikLoggedInSource.asObservable();

  constructor(private http: HttpClient) { }

  login(email: string, password: string): Observable<Ucenik> {
    return this.http.post<Ucenik>('/api/token-auth/', {username: email, password}).pipe(tap(res => {
      localStorage.setItem('token', res.token);
      localStorage.setItem('ucenik', JSON.stringify(res));
      this.ucenikLoggedInSource.next(res);
    }));
  }

  logout() {
    localStorage.removeItem('token');
  }

  public get name(): string  {
    if (this.ucenik === null) {
      const ucenikJson = localStorage.getItem('ucenik');
      if (ucenikJson === null) {
        return '';
      }
      this.ucenik = JSON.parse(ucenikJson);
    }
    return this.ucenik.firstName + ' ' + this.ucenik.lastName;
  }

  public get loggedIn(): boolean {
    return localStorage.getItem('token') !== null;
  }

}
