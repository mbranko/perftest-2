import { Component, OnInit } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Router } from '@angular/router';
import { Observable, Subscription } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { JwtService } from '../../services/jwt.service';
import { TestService } from '../../services/test.service';
import { Test } from '../../models';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit {

  testovi: Test[];
  subscription: Subscription;
  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

  constructor(
      private breakpointObserver: BreakpointObserver,
      private router: Router,
      private jwtService: JwtService,
      private testService: TestService) {
    this.subscription = this.jwtService.ucenikLoggedIn.subscribe(ucenik => {
      this.loadTests();
    });
  }

  ngOnInit(): void {
    this.loadTests();
  }

  loggedIn(): boolean {
    return this.jwtService.loggedIn;
  }

  logout() {
    this.jwtService.logout();
    this.testovi = [];
    this.router.navigate(['/login']);
  }

  name() {
    return this.jwtService.name;
  }

  loadTests(): void {
    this.testService.getTests().subscribe(data => {
      this.testovi = data;
    }, error => {
      if (error.status === 401) {
        this.router.navigate(['/login']);
      }
    });
  }
}
